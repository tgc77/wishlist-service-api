from sqlmodel import SQLModel

from sqlmodel.ext.asyncio.session import AsyncSession

from api.core.entities.access_credentials import AccessCredentialsEntity
from api.core.repositories.access_credentials import AccessCredentialsRepository
from api.core.entities.client import ClientEntity
from api.core.repositories.client import ClientRepository
from api.core.logger import logger
from api.core.database import async_engine, sessionmaker


async def create_database_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        print("MySQL database models created")

    await dispatch_database_populate_models()


async def dispatch_database_populate_models():

    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as _session:
        try:
            session: AsyncSession = _session

            client_repository = ClientRepository(session)

            admin = await client_repository.create(
                ClientEntity(name="API Admin", email="api.admin@luizalabs.com.br")
            )
            client = await client_repository.create(
                ClientEntity(name="API Client", email="api.client@luizalabs.com.br")
            )
            admin_credentials = AccessCredentialsEntity(
                client_id=admin.id,
                email="api.admin@luizalabs.com.br",
                username="api.admin",
                password="api.admin",
                active=True,
                scope="admin"
            )
            client_credentials = AccessCredentialsEntity(
                client_id=client.id,
                email="api.client@luizalabs.com.br",
                username="api.client",
                password="api.client",
                active=True,
                scope="client"
            )

            access_credentials_repository = AccessCredentialsRepository(session)
            await access_credentials_repository.register(admin_credentials)
            await access_credentials_repository.register(client_credentials)

        except Exception as ex:
            logger.error("Oops! Could not create essentials_clients")
