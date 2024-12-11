from __future__ import annotations

from dataclasses import dataclass
import json
from typing import List, TypeVar


APIConfigParameter = TypeVar('APIConfigParameter', bound=str)


@dataclass
class ServiceApiRouteMapper:
    tags: List = None
    get_all: str = None
    get_by: str = None
    create: str = None
    update: str = None
    delete: str = None

    @classmethod
    def load_from_apiconfig(cls, apiconfig_mapper: APIConfigParameter) -> ServiceApiRouteMapper:
        routes_config = json.loads(apiconfig_mapper)
        return cls(
            tags=routes_config['gateway_tags'],
            get_all=routes_config['get_all'],
            get_by=routes_config['get_by'],
            create=routes_config['create'],
            update=routes_config['update'],
            delete=routes_config['delete']
        )
