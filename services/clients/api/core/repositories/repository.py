from fastapi import Depends

from api.core.database import AsyncSession, get_async_session


class Repository:
    _session: AsyncSession = Depends(get_async_session)
