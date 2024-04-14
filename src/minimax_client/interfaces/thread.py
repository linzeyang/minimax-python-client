"""thread.py"""

from typing import Any, Dict, List, Literal, Optional

import httpx

from minimax_client.entities.thread import (
    MessageCreateResponse,
    MessageListResponse,
    MessageRetrieveResponse,
    RunCancelResponse,
    RunCreateResponse,
    RunListResponse,
    RunRetrieveResponse,
    RunSubmitToolOutputsResponse,
    RunUpdateResponse,
    ThreadCreateResponse,
    ThreadRetrieveResponse,
    ThreadUpdateResponse,
)
from minimax_client.interfaces.base import BaseAsyncInterface, BaseSyncInterface


class Messages(BaseSyncInterface):
    """Synchronous Messages interface"""

    url_path = "threads/messages"

    def create(
        self,
        thread_id: str,
        content: str,
        role: Literal["user", "assistant"],
        file_ids: Optional[List[str]] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> MessageCreateResponse:
        """
        Create a new message

        Args:
            thread_id (str): The ID of the thread to create the message in
            content (str): The content of the message
            role (str): The role of the message
            file_ids (Optional[List[str]], optional):
                The IDs of the files attached to the message. Defaults to None.
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the message. Defaults to None.

        Returns:
            MessageCreateResponse: The response from the API
        """
        json_body: Dict[str, Any] = {
            "thread_id": thread_id,
            "content": content,
            "role": role,
        }

        if file_ids:
            json_body["file_ids"] = file_ids

        if metadata:
            json_body["metadata"] = metadata

        resp = self.client.post(url=f"{self.url_path}/add", json=json_body)

        return MessageCreateResponse(**resp.json())

    def retrieve(self, message_id: str, thread_id: str) -> MessageRetrieveResponse:
        """
        Retrieve general info of the given message

        Args:
            message_id (str): The ID of the message to retrieve
            thread_id (str): The ID of the thread the message belongs to

        Returns:
            MessageRetrieveResponse: The response from the API
        """
        resp = self.client.get(
            url=f"{self.url_path}/retrieve",
            params={"message_id": message_id, "thread_id": thread_id},
        )

        return MessageRetrieveResponse(**resp.json())

    def list(
        self,
        thread_id: str,
        limit: int = 20,
        order: Literal["asc", "desc"] = "desc",
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> MessageListResponse:
        """
        List all messages in the given thread

        Args:
            thread_id (str): The ID of the thread to list messages from

        Returns:
            MessageListResponse: The response from the API
        """
        params = {"thread_id": thread_id, "limit": limit, "order": order}

        if after:
            params["after"] = after

        if before:
            params["before"] = before

        resp = self.client.get(url=f"{self.url_path}/list", params=params)

        return MessageListResponse(**resp.json())


class AsyncMessages(BaseAsyncInterface, Messages):
    """Asynchronous Messages interface"""

    async def create(
        self,
        thread_id: str,
        content: str,
        role: Literal["user", "assistant"],
        file_ids: Optional[List[str]] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> MessageCreateResponse:
        """
        Create a new message

        Args:
            thread_id (str): The ID of the thread to create the message in
            content (str): The content of the message
            role (str): The role of the message
            file_ids (Optional[List[str]], optional):
                The IDs of the files attached to the message. Defaults to None.
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the message. Defaults to None.

        Returns:
            MessageCreateResponse: The response from the API
        """
        json_body: Dict[str, Any] = {
            "thread_id": thread_id,
            "content": content,
            "role": role,
        }

        if file_ids:
            json_body["file_ids"] = file_ids

        if metadata:
            json_body["metadata"] = metadata

        resp = await self.client.post(url=f"{self.url_path}/add", json=json_body)

        return MessageCreateResponse(**resp.json())

    async def retrieve(
        self, message_id: str, thread_id: str
    ) -> MessageRetrieveResponse:
        """
        Retrieve general info of the given message

        Args:
            message_id (str): The ID of the message to retrieve
            thread_id (str): The ID of the thread the message belongs to

        Returns:
            MessageRetrieveResponse: The response from the API
        """
        resp = await self.client.get(
            url=f"{self.url_path}/retrieve",
            params={"message_id": message_id, "thread_id": thread_id},
        )

        return MessageRetrieveResponse(**resp.json())

    async def list(
        self,
        thread_id: str,
        limit: int = 20,
        order: Literal["asc", "desc"] = "desc",
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> MessageListResponse:
        """
        List all messages in the given thread

        Args:
            thread_id (str): The ID of the thread to list messages from

        Returns:
            MessageListResponse: The response from the API
        """
        params = {"thread_id": thread_id, "limit": limit, "order": order}

        if after:
            params["after"] = after

        if before:
            params["before"] = before

        resp = await self.client.get(url=f"{self.url_path}/list", params=params)

        return MessageListResponse(**resp.json())


class Runs(BaseSyncInterface):
    """Synchronous Run interface"""

    url_path = "threads/run"

    def create(
        self,
        thread_id: str,
        assistant_id: str,
        instructions: Optional[str] = None,
        model: Optional[
            Literal[
                "abab6-chat",
                "abab5.5-chat",
                "abab5.5-chat-240131",
                "abab5.5s-chat",
                "abab5.5s-chat-240123",
            ]
        ] = None,
        tools: Optional[List] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> RunCreateResponse:
        """
        Create a non-stream run

        Args:
            thread_id (str): The ID of the thread to create the run for
            assistant_id (str): The ID of the assistant to run
            instructions (Optional[str], optional):
                The instructions of the run. Defaults to None.
            model (
                Optional[
                    Literal[
                        "abab6-chat", "abab5.5-chat", "abab5.5-chat-240131",
                        "abab5.5s-chat", "abab5.5s-chat-240123"
                    ]
                ],
                optional
            ):
                The model to use for the run. Defaults to None.
            tools (Optional[List], optional):
                The tools to use for the run. Defaults to None.
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the run. Defaults to None.

        Returns:
            RunCreateResponse: The response from the API
        """
        json_body: Dict[str, Any] = {
            "thread_id": thread_id,
            "assistant_id": assistant_id,
        }

        if instructions:
            json_body["instructions"] = instructions

        if model:
            json_body["model"] = model

        if tools:
            json_body["tools"] = tools

        if metadata:
            json_body["metadata"] = metadata

        resp = self.client.post(url=f"{self.url_path}/create", json=json_body)

        return RunCreateResponse(**resp.json())

    def retrieve(self, run_id: str, thread_id: str) -> RunRetrieveResponse:
        """
        Retrieve general info of the given run

        Args:
            run_id (str): The ID of the run to retrieve
            thread_id (str): The ID of the thread the run belongs to

        Returns:
            RunRetrieveResponse: The response from the API
        """
        resp = self.client.get(
            url=f"{self.url_path}/retrieve",
            params={"run_id": run_id, "thread_id": thread_id},
        )

        return RunRetrieveResponse(**resp.json())

    def list(
        self,
        thread_id: str,
        limit: int = 20,
        order: Literal["asc", "desc"] = "desc",
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> RunListResponse:
        """
        List all runs in the given thread

        Args:
            thread_id (str): The ID of the thread to list runs from
            limit (int, optional): The maximum number of runs to return. Defaults to 20.
            order (Literal["asc", "desc"], optional):
                The order of the list. Defaults to "desc".
            after (Optional[str], optional):
                The ID of the run to start from. Defaults to None.
            before (Optional[str], optional):
                The ID of the run to end at. Defaults to None.

        Returns:
            RunListResponse: The response from the API
        """
        params = {"thread_id": thread_id, "limit": limit, "order": order}

        if after:
            params["after"] = after

        if before:
            params["before"] = before

        resp = self.client.get(url=f"{self.url_path}/list", params=params)

        return RunListResponse(**resp.json())

    def update(
        self, run_id: str, thread_id: str, metadata: Optional[Dict[str, str]] = None
    ) -> RunUpdateResponse:
        """
        Update general info of the given run

        Args:
            run_id (str): The ID of the run to update
            thread_id (str): The ID of the thread the run belongs to
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the run. Defaults to None.

        Returns:
            RunUpdateResponse: The response from the API
        """
        json_body: Dict[str, Any] = {
            "run_id": run_id,
            "thread_id": thread_id,
        }

        if metadata:
            json_body["metadata"] = metadata

        resp = self.client.post(url=f"{self.url_path}/modify", json=json_body)

        return RunUpdateResponse(**resp.json())

    def cancel(self, run_id: str, thread_id: str) -> RunCancelResponse:
        """
        Cancel an existing run

        Args:
            run_id (str): The ID of the run to cancel
            thread_id (str): The ID of the thread the run belongs to

        Returns:
            RunCancelResponse: The response from the API
        """
        json_body = {
            "run_id": run_id,
            "thread_id": thread_id,
        }

        resp = self.client.post(url=f"{self.url_path}/cancel", json=json_body)

        return RunCancelResponse(**resp.json())

    def submit_tool_outputs(
        self, run_id: str, thread_id: str, tool_outputs: List[Dict[str, str]]
    ) -> RunSubmitToolOutputsResponse:
        """
        Submit the outputs of tools to the given run

        Args:
            run_id (str): The ID of the run to submit
            thread_id (str): The ID of the thread the run belongs to
            tool_outputs (List[Dict[str, str]]): The outputs of the tools

        Returns:
            RunSubmitToolOutputsResponse: The response from the API
        """
        json_body = {
            "run_id": run_id,
            "thread_id": thread_id,
            "tool_outputs": tool_outputs,
        }

        resp = self.client.post(
            url=f"{self.url_path}/submit_tool_outputs", json=json_body
        )

        return RunSubmitToolOutputsResponse(**resp.json())


class AsyncRuns(BaseAsyncInterface, Runs):
    """Asynchronous Run interface"""

    async def create(
        self,
        thread_id: str,
        assistant_id: str,
        instructions: Optional[str] = None,
        model: Optional[
            Literal[
                "abab6-chat",
                "abab5.5-chat",
                "abab5.5-chat-240131",
                "abab5.5s-chat",
                "abab5.5s-chat-240123",
            ]
        ] = None,
        tools: Optional[List] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> RunCreateResponse:
        """
        Create a non-stream run

        Args:
            thread_id (str): The ID of the thread to create the run for
            assistant_id (str): The ID of the assistant to run
            instructions (Optional[str], optional):
                The instructions of the run. Defaults to None.
            model (
                Optional[
                    Literal[
                        "abab6-chat", "abab5.5-chat", "abab5.5-chat-240131",
                        "abab5.5s-chat", "abab5.5s-chat-240123"
                    ]
                ],
                optional
            ):
                The model to use for the run. Defaults to None.
            tools (Optional[List], optional):
                The tools to use for the run. Defaults to None.
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the run. Defaults to None.

        Returns:
            RunCreateResponse: The response from the API
        """
        json_body: Dict[str, Any] = {
            "thread_id": thread_id,
            "assistant_id": assistant_id,
        }

        if instructions:
            json_body["instructions"] = instructions

        if model:
            json_body["model"] = model

        if tools:
            json_body["tools"] = tools

        if metadata:
            json_body["metadata"] = metadata

        resp = await self.client.post(url=f"{self.url_path}/create", json=json_body)

        return RunCreateResponse(**resp.json())

    async def retrieve(self, run_id: str, thread_id: str) -> RunRetrieveResponse:
        """
        Retrieve general info of the given run

        Args:
            run_id (str): The ID of the run to retrieve
            thread_id (str): The ID of the thread the run belongs to

        Returns:
            RunRetrieveResponse: The response from the API
        """
        resp = await self.client.get(
            url=f"{self.url_path}/retrieve",
            params={"run_id": run_id, "thread_id": thread_id},
        )

        return RunRetrieveResponse(**resp.json())

    async def list(
        self,
        thread_id: str,
        limit: int = 20,
        order: Literal["asc", "desc"] = "desc",
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> RunListResponse:
        """
        List all runs in the given thread

        Args:
            thread_id (str): The ID of the thread to list runs from
            limit (int, optional): The maximum number of runs to return. Defaults to 20.
            order (Literal["asc", "desc"], optional):
                The order of the list. Defaults to "desc".
            after (Optional[str], optional):
                The ID of the run to start from. Defaults to None.
            before (Optional[str], optional):
                The ID of the run to end at. Defaults to None.

        Returns:
            RunListResponse: The response from the API
        """
        params = {"thread_id": thread_id, "limit": limit, "order": order}

        if after:
            params["after"] = after

        if before:
            params["before"] = before

        resp = await self.client.get(url=f"{self.url_path}/list", params=params)

        return RunListResponse(**resp.json())

    async def update(
        self, run_id: str, thread_id: str, metadata: Optional[Dict[str, str]] = None
    ) -> RunUpdateResponse:
        """
        Update general info of the given run

        Args:
            run_id (str): The ID of the run to update
            thread_id (str): The ID of the thread the run belongs to
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the run. Defaults to None.

        Returns:
            RunUpdateResponse: The response from the API
        """
        json_body: Dict[str, Any] = {
            "run_id": run_id,
            "thread_id": thread_id,
        }

        if metadata:
            json_body["metadata"] = metadata

        resp = await self.client.post(url=f"{self.url_path}/modify", json=json_body)

        return RunUpdateResponse(**resp.json())

    async def cancel(self, run_id: str, thread_id: str) -> RunCancelResponse:
        """
        Cancel an existing run

        Args:
            run_id (str): The ID of the run to cancel
            thread_id (str): The ID of the thread the run belongs to

        Returns:
            RunCancelResponse: The response from the API
        """
        json_body = {
            "run_id": run_id,
            "thread_id": thread_id,
        }

        resp = await self.client.post(url=f"{self.url_path}/cancel", json=json_body)

        return RunCancelResponse(**resp.json())

    async def submit_tool_outputs(
        self, run_id: str, thread_id: str, tool_outputs: List[Dict[str, str]]
    ) -> RunSubmitToolOutputsResponse:
        """
        Submit the outputs of tools to the given run

        Args:
            run_id (str): The ID of the run to submit
            thread_id (str): The ID of the thread the run belongs to
            tool_outputs (List[Dict[str, str]]): The outputs of the tools

        Returns:
            RunSubmitToolOutputsResponse: The response from the API
        """
        json_body = {
            "run_id": run_id,
            "thread_id": thread_id,
            "tool_outputs": tool_outputs,
        }

        resp = await self.client.post(
            url=f"{self.url_path}/submit_tool_outputs", json=json_body
        )

        return RunSubmitToolOutputsResponse(**resp.json())


class Threads(BaseSyncInterface):
    """Synchronous Threads interface"""

    url_path = "threads"
    messages: Messages
    runs: Runs

    def __init__(self, http_client: httpx.Client) -> None:
        super().__init__(http_client=http_client)
        self.messages = Messages(http_client=http_client)
        self.runs = Runs(http_client=http_client)

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

    messages: AsyncMessages
    runs: AsyncRuns

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        super().__init__(http_client=http_client)
        self.messages = AsyncMessages(http_client=http_client)
        self.runs = AsyncRuns(http_client=http_client)

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
