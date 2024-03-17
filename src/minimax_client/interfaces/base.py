"""base.py"""

import httpx


class BaseInterface:
    """Base interface"""

    url_path: str


class BaseSyncInterface(BaseInterface):
    """Base Synchronous interface"""

    client: httpx.Client

    def __init__(self, http_client: httpx.Client) -> None:
        self.client = http_client


class BaseAsyncInterface(BaseInterface):
    """Base Asynchronous interface"""

    client: httpx.AsyncClient

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self.client = http_client
