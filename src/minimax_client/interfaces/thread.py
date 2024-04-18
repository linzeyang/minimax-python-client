"""thread.py"""

import json
from typing import Any, AsyncGenerator, Dict, Generator, List, Literal, Optional, Union

import httpx

from minimax_client.entities.thread import (
    MessageCreateResponse,
    MessageListResponse,
    MessageRetrieveResponse,
    RunCancelResponse,
    RunCreateResponse,
    RunListResponse,
    RunRetrieveResponse,
    RunStepListResponse,
    RunStepRetrieveResponse,
    RunSubmitToolOutputsResponse,
    RunUpdateResponse,
    StreamedRunMessageResponse,
    StreamedRunResponse,
    StreamedRunStepResponse,
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


class RunSteps(BaseSyncInterface):
    """Synchronous Run Steps interface"""

    url_path = "threads/run_steps"

    def retrieve(
        self, step_id: str, thread_id: str, run_id: str
    ) -> RunStepRetrieveResponse:
        """
        Retrieve general info of the given run step

        Args:
            step_id (str): The ID of the run step to retrieve
            thread_id (str): The ID of the thread the run belongs to
            run_id (str): The ID of the run the step belongs to

        Returns:
            RunStepRetrieveResponse: The response from the API
        """
        params = {"step_id": step_id, "thread_id": thread_id, "run_id": run_id}

        resp = self.client.get(url=f"{self.url_path}/retrieve", params=params)

        return RunStepRetrieveResponse(**resp.json())

    def list(
        self,
        run_id: str,
        thread_id: str,
        limit: int = 20,
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> RunStepListResponse:
        """
        Retrive all run steps of the given run

        Args:
            run_id (str): The ID of the run to list steps from
            thread_id (str): The ID of the thread the run belongs to
            limit (int):
                The maximum number of steps to return. Defaults to 20.
            after (Optional[str]):
                The ID of the step to start after. Defaults to None.
            before (Optional[str]):
                The ID of the step to end before. Defaults to None.

        Returns:
            RunStepListResponse: The response from the API
        """
        params = {
            "run_id": run_id,
            "thread_id": thread_id,
            "limit": limit,
        }

        if after:
            params["after"] = after

        if before:
            params["before"] = before

        resp = self.client.get(url=f"{self.url_path}/list", params=params)

        return RunStepListResponse(**resp.json())


class AsyncRunSteps(BaseAsyncInterface, RunSteps):
    """Asynchronous Run Steps interface"""

    async def retrieve(
        self, step_id: str, thread_id: str, run_id: str
    ) -> RunStepRetrieveResponse:
        """
        Retrieve general info of the given run step

        Args:
            step_id (str): The ID of the run step to retrieve
            thread_id (str): The ID of the thread the run belongs to
            run_id (str): The ID of the run the step belongs to

        Returns:
            RunStepRetrieveResponse: The response from the API
        """
        params = {"step_id": step_id, "thread_id": thread_id, "run_id": run_id}

        resp = await self.client.get(url=f"{self.url_path}/retrieve", params=params)

        return RunStepRetrieveResponse(**resp.json())

    async def list(
        self,
        run_id: str,
        thread_id: str,
        limit: int = 20,
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> RunStepListResponse:
        """
        Retrive all run steps of the given run

        Args:
            run_id (str): The ID of the run to list steps from
            thread_id (str): The ID of the thread the run belongs to
            limit (int):
                The maximum number of steps to return. Defaults to 20.
            after (Optional[str]):
                The ID of the step to start after. Defaults to None.
            before (Optional[str]):
                The ID of the step to end before. Defaults to None.

        Returns:
            RunStepListResponse: The response from the API
        """
        params = {
            "run_id": run_id,
            "thread_id": thread_id,
            "limit": limit,
        }

        if after:
            params["after"] = after

        if before:
            params["before"] = before

        resp = await self.client.get(url=f"{self.url_path}/list", params=params)

        return RunStepListResponse(**resp.json())


class Runs(BaseSyncInterface):
    """Synchronous Run interface"""

    url_path = "threads/run"
    steps: RunSteps

    def __init__(self, http_client: httpx.Client) -> None:
        super().__init__(http_client=http_client)
        self.steps = RunSteps(http_client=http_client)

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
        tools: Optional[List[Dict[str, Union[str, Dict]]]] = None,
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
            tools (Optional[List[Dict[str, Union[str, Dict]]]], optional):
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

    def stream(  # noqa: C901
        self,
        *,
        stream_mode: Literal[1, 2],
        thread_id: str,
        assistant_id: str,
        messages: List[Dict[str, Union[int, str, List[str], Dict]]],
        model: Optional[
            Literal[
                "abab6-chat",
                "abab5.5-chat",
                "abab5.5-chat-240131",
                "abab5.5s-chat",
                "abab5.5s-chat-240123",
            ]
        ] = None,
        t2a_option: Optional[Dict[str, str]] = None,
        instructions: Optional[str] = None,
        tools: Optional[List[Dict[str, Union[str, Dict]]]] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Generator[
        Union[StreamedRunMessageResponse, StreamedRunStepResponse, StreamedRunResponse],
        None,
        None,
    ]:
        """
        Create a stream run

        Args:
            stream_mode (Literal[1, 2]):
                The stream mode to use.
                1 for TEXT_STREAM,
                2 for TEXT_AND_AUDIO_STREAM (In this mode, the input could be audio)
            thread_id (str): The ID of the thread to create the run for
            assistant_id (str): The ID of the assistant to run
            messages (List[Dict[str, Union[int, str, List[str], Dict]]]):
                The messages to use for the run
            model (
                Optional[
                    Literal[
                        "abab6-chat", "abab5.5-chat", "abab5.5-chat-240131",
                        "abab5.5s-chat", "abab5.5s-chat-240123"
                    ]
                ]
            ):
                The model to use for the run.
                If not specified (ie. None), the model of the assistant will be used.
            t2a_option (Optional[Dict[str, str]], optional):
                T2A option to use for the run. Defaults to None.
            instructions (Optional[str], optional):
                The instructions of the run. Defaults to None.
            tools (Optional[List[Dict[str, Union[str, Dict]]]], optional):
                The tools to use for the run. Defaults to None.
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the run. Defaults to None.

        Returns:
            Generator[Union[
                StreamedRunMessageResponse, StreamedRunStepResponse, StreamedRunResponse
            ], None, None]: The response from the API
        """
        json_body = {
            "stream": stream_mode,
            "thread_id": thread_id,
            "assistant_id": assistant_id,
            "messages": messages,
        }

        if model:
            json_body["model"] = model

        if t2a_option:
            json_body["t2a_option"] = t2a_option

        if instructions:
            json_body["instructions"] = instructions

        if tools:
            json_body["tools"] = tools

        if metadata:
            json_body["metadata"] = metadata

        with self.client.stream(
            method="post", url=f"{self.url_path}/create_stream", json=json_body
        ) as resp:
            for data_text in resp.iter_text():
                if not data_text.startswith("data:"):
                    continue

                data_json = json.loads(data_text.split("data: ", 2)[1])

                if not data_json.get("data"):
                    continue

                if (object_tag := data_json["data"]["object"]) == "run":
                    yield StreamedRunResponse(**data_json)
                elif object_tag == "message":
                    yield StreamedRunMessageResponse(**data_json)
                elif object_tag == "run step":
                    yield StreamedRunStepResponse(**data_json)

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
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> RunListResponse:
        """
        List all runs in the given thread

        Args:
            thread_id (str): The ID of the thread to list runs from
            limit (int, optional): The maximum number of runs to return. Defaults to 20.
            after (Optional[str], optional):
                The ID of the run to start from. Defaults to None.
            before (Optional[str], optional):
                The ID of the run to end at. Defaults to None.

        Returns:
            RunListResponse: The response from the API
        """
        params = {"thread_id": thread_id, "limit": limit}

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

    steps: AsyncRunSteps

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        super().__init__(http_client=http_client)
        self.steps = AsyncRunSteps(http_client=http_client)

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
        tools: Optional[List[Dict[str, Union[str, Dict]]]] = None,
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
            tools (Optional[List[Dict[str, Union[str, Dict]]]], optional):
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

    async def stream(  # noqa: C901
        self,
        *,
        stream_mode: Literal[1, 2],
        thread_id: str,
        assistant_id: str,
        messages: List[Dict[str, Union[int, str, List[str], Dict]]],
        model: Optional[
            Literal[
                "abab6-chat",
                "abab5.5-chat",
                "abab5.5-chat-240131",
                "abab5.5s-chat",
                "abab5.5s-chat-240123",
            ]
        ] = None,
        t2a_option: Optional[Dict[str, str]] = None,
        instructions: Optional[str] = None,
        tools: Optional[List[Dict[str, Union[str, Dict]]]] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> AsyncGenerator[
        Union[StreamedRunMessageResponse, StreamedRunStepResponse, StreamedRunResponse],
        None,
    ]:
        """
        Create a stream run

        Args:
            stream_mode (Literal[1, 2]):
                The stream mode to use.
                1 for TEXT_STREAM,
                2 for TEXT_AND_AUDIO_STREAM (In this mode, the input could be audio)
            thread_id (str): The ID of the thread to create the run for
            assistant_id (str): The ID of the assistant to run
            messages (List[Dict[str, Union[int, str, List[str], Dict]]]):
                The messages to use for the run
            model (
                Optional[
                    Literal[
                        "abab6-chat", "abab5.5-chat", "abab5.5-chat-240131",
                        "abab5.5s-chat", "abab5.5s-chat-240123"
                    ]
                ]
            ):
                The model to use for the run.
                If not specified (ie. None), the model of the assistant will be used.
            t2a_option (Optional[Dict[str, str]], optional):
                T2A option to use for the run. Defaults to None.
            instructions (Optional[str], optional):
                The instructions of the run. Defaults to None.
            tools (Optional[List[Dict[str, Union[str, Dict]]]], optional):
                The tools to use for the run. Defaults to None.
            metadata (Optional[Dict[str, str]], optional):
                The metadata of the run. Defaults to None.

        Returns:
            AsyncGenerator[Union[
                StreamedRunMessageResponse, StreamedRunStepResponse, StreamedRunResponse
            ], None]: The response from the API
        """
        json_body = {
            "stream": stream_mode,
            "thread_id": thread_id,
            "assistant_id": assistant_id,
            "messages": messages,
        }

        if model:
            json_body["model"] = model

        if t2a_option:
            json_body["t2a_option"] = t2a_option

        if instructions:
            json_body["instructions"] = instructions

        if tools:
            json_body["tools"] = tools

        if metadata:
            json_body["metadata"] = metadata

        async with self.client.stream(
            method="post", url=f"{self.url_path}/create_stream", json=json_body
        ) as resp:
            for data_text in resp.iter_text():
                if not data_text.startswith("data:"):
                    continue

                data_json = json.loads(data_text.split("data: ", 2)[1])

                if not data_json.get("data"):
                    continue

                if (object_tag := data_json["data"]["object"]) == "run":
                    yield StreamedRunResponse(**data_json)
                elif object_tag == "message":
                    yield StreamedRunMessageResponse(**data_json)
                elif object_tag == "run step":
                    yield StreamedRunStepResponse(**data_json)

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
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> RunListResponse:
        """
        List all runs in the given thread

        Args:
            thread_id (str): The ID of the thread to list runs from
            limit (int, optional): The maximum number of runs to return. Defaults to 20.
            after (Optional[str], optional):
                The ID of the run to start from. Defaults to None.
            before (Optional[str], optional):
                The ID of the run to end at. Defaults to None.

        Returns:
            RunListResponse: The response from the API
        """
        params = {"thread_id": thread_id, "limit": limit}

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
