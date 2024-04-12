"""thread.py"""

from typing import Any, Dict, Optional

from minimax_client.entities.thread import (
    ThreadCreateResponse,
    ThreadRetrieveResponse,
    ThreadUpdateResponse,
)
from minimax_client.interfaces.base import BaseAsyncInterface, BaseSyncInterface


class Threads(BaseSyncInterface):
    """Synchronous Threads interface"""

    url_path = "threads"

    def create(self, metadata: Optional[Dict[str, str]] = None) -> ThreadCreateResponse:
        """
        Create a new thread

        Args:
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the thread. Defaults to None.

        Returns:
            ThreadCreateResponse: The created thread
        """
        json_body = {}

        if metadata:
            json_body["metadata"] = metadata

        resp = self.client.post(f"{self.url_path}/create", json=json_body)

        return ThreadCreateResponse(**resp.json())

    def retrieve(self, thread_id: str) -> ThreadRetrieveResponse:
        """
        Retrieve general info of the given thread

        Args:
            thread_id (str): The ID of the thread to retrieve

        Returns:
            ThreadRetrieveResponse: The response from the API
        """
        resp = self.client.get(
            f"{self.url_path}/retrieve", params={"thread_id": thread_id}
        )

        return ThreadRetrieveResponse(**resp.json())

    def update(
        self, thread_id: str, metadata: Optional[Dict[str, str]] = None
    ) -> ThreadUpdateResponse:
        """
        Update general info of the given thread

        Args:
            thread_id (str): The ID of the thread to update
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the thread. Defaults to None.

        Returns:
            ThreadUpdateResponse: The updated thread
        """
        json_body: Dict[str, Any] = {"id": thread_id}

        if metadata:
            json_body["metadata"] = metadata

        resp = self.client.post(f"{self.url_path}/modify", json=json_body)

        return ThreadUpdateResponse(**resp.json())


class AsyncThreads(BaseAsyncInterface, Threads):
    """Asynchronous Threads interface"""

    async def create(
        self, metadata: Optional[Dict[str, str]] = None
    ) -> ThreadCreateResponse:
        """
        Create a new thread

        Args:
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the thread. Defaults to None.

        Returns:
            ThreadCreateResponse: The created thread
        """
        json_body = {}

        if metadata:
            json_body["metadata"] = metadata

        resp = await self.client.post(f"{self.url_path}/create", json=json_body)

        return ThreadCreateResponse(**resp.json())

    async def retrieve(self, thread_id: str) -> ThreadRetrieveResponse:
        """
        Retrieve general info of the given thread

        Args:
            thread_id (str): The ID of the thread to retrieve

        Returns:
            ThreadRetrieveResponse: The response from the API
        """
        resp = await self.client.get(
            f"{self.url_path}/retrieve", params={"thread_id": thread_id}
        )

        return ThreadRetrieveResponse(**resp.json())

    async def update(
        self, thread_id: str, metadata: Optional[Dict[str, str]] = None
    ) -> ThreadUpdateResponse:
        """
        Update general info of the given thread

        Args:
            thread_id (str): The ID of the thread to update
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the thread. Defaults to None.

        Returns:
            ThreadUpdateResponse: The updated thread
        """
        json_body: Dict[str, Any] = {"id": thread_id}

        if metadata:
            json_body["metadata"] = metadata

        resp = await self.client.post(f"{self.url_path}/modify", json=json_body)

        return ThreadUpdateResponse(**resp.json())
