
from api.core.database import get_async_session


class Repository:

    def __init__(self):
        self._async_session = get_async_session()
