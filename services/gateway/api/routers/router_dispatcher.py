from __future__ import annotations

import zlib
from base64 import urlsafe_b64encode as b64enc
from typing import Dict, List, Optional, Tuple, Mapping, TypeVar
from dataclasses import dataclass, field

import json
import re

from fastapi import APIRouter, Request, FastAPI
import httpx
from pydantic import BaseModel

from api.core.settings import APIConfig
from api.core.logger import logger
from api.core.response import APIGatwayProviderResponse
from api.core.utils import ipdb_set_trace

APIConfigParameter = TypeVar('APIConfigParameter', bound=str)


class ServiceRouteParameters:

    def __init__(
        self,
        service_router: ServiceApiRouter,
        route_path: str,
        auth_header: Optional[Dict] = None,
        dispatched_data: Optional[BaseModel] = None,
        quey_params: Optional[BaseModel] = None,
        **params
    ):
        self._service_router = service_router
        self._route_path = route_path
        self.auth_header = auth_header
        self.dispatched_data = dispatched_data
        self.quey_params = quey_params
        self.params = params

    def get_service_route_path(self) -> str:
        return self._service_router.get_service_route_path(
            route_path=self._route_path,
            **self.params
        )

    def get_service_router(self) -> ServiceApiRouter:
        return self._service_router


class APIRouteMapper(Mapping):

    def __init__(self) -> None:
        self._routes = {}
        self._gateway_route = None

    def __call__(self) -> ServiceRouteParameters:
        return self._routes[self._gateway_route]

    def get_params(self) -> Dict[str, str]:
        return self.__call__().params

    def __getitem__(self, gateway_route: str) -> ServiceRouteParameters:
        return self._routes[gateway_route]

    def __setitem__(self, gateway_route: str, service_route: ServiceRouteParameters):
        self._gateway_route = gateway_route
        self._routes[gateway_route] = service_route

    def __iter__(self):
        return iter(self._routes)

    def __len__(self):
        return len(self._routes)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._routes})"

    def __str__(self):
        return str(self._routes)

    def keys(self) -> List[str]:
        _keys = []
        for key, _ in self._routes.items():
            _keys.append(key)
        return _keys


# TODO: In the future perhaps link mapped routes dynamically
# @dataclass
# class RouteActions:
#     get_all: str = None
#     get_by: str = None
#     review: str = None
#     create: str = None
#     update: str = None
#     delete: Dict[str, str] = field(default_factory={})


@dataclass
class GatewayApiRouter:
    _prefix: str = None
    _tags: List = None
    # _route_actions: RouteActions = field(default_factory=RouteActions())
    get_all: str = None
    get_by: str = None
    review: str = None
    create: str = None
    update: str = None
    delete: Dict[str, str] = field(default_factory={})

    @classmethod
    def get_action_route_params(cls, action: str) -> Tuple[str]:
        action_param = cls.__dict__.get(action)
        regex = r"\{(\w+)\}"
        params = re.findall(regex, action_param)
        return tuple(params)

    @classmethod
    def load_from_apiconfig(cls, apiconfig_mapper: APIConfigParameter) -> GatewayApiRouter:
        routes_config = json.loads(apiconfig_mapper)
        return cls(
            _prefix=routes_config['gateway_prefix'],
            _tags=routes_config['gateway_tags'],
            get_all=routes_config.get('get_all'),
            get_by=routes_config.get('get_by'),
            review=routes_config.get('review'),
            create=routes_config.get('create'),
            update=routes_config.get('update'),
            delete=routes_config.get('delete')
        )


@dataclass
class ServiceApiRouter:
    gateway_router: GatewayApiRouter = None
    service_url: str = None
    service_route_prefix: Optional[str] = ""
    _router_pattern: str = "{service_url}{service_route_prefix}"
    _routes: APIRouteMapper = field(default_factory=lambda: APIRouteMapper())

    def __post_init__(self):
        self._initialize_api_route_mapper()

    def _initialize_api_route_mapper(self):
        for action, route in self.gateway_router.__dict__.items():
            if action.startswith('_') or route is None:
                continue

            gateway_route = self.gateway_router.__dict__.get(action)

            if isinstance(gateway_route, dict):
                for _action, _route in gateway_route.items():
                    self._routes[_action] = ServiceRouteParameters(
                        service_router=self,
                        route_path=_route
                    )
            else:
                self._routes[route] = ServiceRouteParameters(
                    service_router=self,
                    route_path=route
                )

    def get_route_parameters_mapper(self, action: str) -> ServiceRouteParameters:
        return self._routes[action]

    def get_service_route_path(self, route_path: str, **params) -> str:
        params.update({
            'service_url': self.service_url.rstrip('/'),
            'service_route_prefix': self.service_route_prefix
        })
        the_route = self._router_pattern + route_path
        return the_route.format(**params)

    def get_app_api_router(self) -> APIRouter:
        return APIRouter(
            prefix=self.gateway_router._prefix,
            tags=self.gateway_router._tags
        )


class RequestRouterDispatcher:

    def __init__(self, request: Request) -> None:
        self._request = request
        self._api_request: httpx.AsyncClient = request.app.api_request
        current_user_encoded = str(self._request.app.state.current_user).encode('utf-8')
        x_auth_data = b64enc(zlib.compress(current_user_encoded, 9))
        self._auth_header = {
            'X-auth-data': x_auth_data
        }

    async def get(
        self,
        parameters: ServiceRouteParameters
    ) -> APIGatwayProviderResponse:
        try:
            route_path = parameters.get_service_route_path()
            self._auth_header.update(parameters.auth_header)
            response = await self._api_request.get(
                route_path,
                headers=self._auth_header,
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Got response with success")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )

    async def get_by(
        self,
        parameters: ServiceRouteParameters
    ) -> APIGatwayProviderResponse:
        try:
            route_path = parameters.get_service_route_path()
            self._auth_header.update(parameters.auth_header)
            query_params = parameters.quey_params
            response = await self._api_request.get(
                route_path,
                headers=self._auth_header,
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT,
                params=query_params
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Got response with success")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )

    async def create(
        self,
        parameters: ServiceRouteParameters
    ) -> APIGatwayProviderResponse:
        try:
            route_path = parameters.get_service_route_path()
            self._auth_header.update(parameters.auth_header)
            create_data = parameters.dispatched_data
            new_client = type(create_data).model_validate(create_data)
            response = await self._api_request.post(
                route_path,
                json=new_client.model_dump(),
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT,
                headers=self._auth_header
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Got response with success")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )

    async def update(
        self,
        parameters: ServiceRouteParameters
    ):
        try:
            route_path = parameters.get_service_route_path()
            self._auth_header.update(parameters.auth_header)
            update_data = parameters.dispatched_data
            client_data = type(update_data).model_validate(update_data)
            response = await self._api_request.patch(
                route_path,
                json=client_data.model_dump(),
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT,
                headers=self._auth_header
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Got response with success")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )

    async def delete(
        self,
        parameters: ServiceRouteParameters
    ):
        try:
            route_path = parameters.get_service_route_path()
            self._auth_header.update(parameters.auth_header)
            response = await self._api_request.delete(
                route_path,
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT,
                headers=self._auth_header
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Got response with success")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )


class APIServiceRouterManager:

    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self._service_routers: Dict[str, ServiceApiRouter] = {}

    def register_api_service_router(self, service_router: ServiceApiRouter):
        self._service_routers[service_router.gateway_router.prefix] = service_router

    async def dispatch_router(self):
        pass
