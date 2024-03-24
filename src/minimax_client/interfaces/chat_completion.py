"""chat_completion.py"""

import json
from http import HTTPStatus
from typing import Any, AsyncGenerator, Dict, Generator, List, Optional, Union

import httpx

from minimax_client.entities.chat_completion import ChatCompletionResponse
from minimax_client.interfaces.base import BaseAsyncInterface, BaseSyncInterface


class ChatCompletions(BaseSyncInterface):
    """Synchronous Chat Completions interface"""

    url_path: str = "text/chatcompletion_v2"

    def create(
        self,
        *,
        messages: List[Dict[str, Union[str, List[Dict[str, Any]]]]],
        model: str = "abab5.5s-chat",
        max_tokens: int = 256,
        temperature: float = 0.9,
        top_p: float = 0.95,
        stream: bool = False,
        tool_choice: str = "auto",
        tools: Optional[List[Dict[str, Union[str, Dict[str, str]]]]] = None,
    ) -> Union[ChatCompletionResponse, Generator[ChatCompletionResponse, None, None]]:
        """
        Create a new chat completion request.

        Requests can be sent in or not in stream by setting the "stream" parameter.
        Streaming requests return a generator that yields ResponseEntities,
        while non-streaming requests return a single ResponseEntity.

        Args:
            messages (list[dict[str, Union[str, list[dict[str, Any]]]]]):
                The messages to generate responses to
            model (str, optional):
                The chatbot model to use. Defaults to "abab5.5s-chat".
            max_tokens (int, optional):
                The maximum number of tokens to generate. Defaults to 256.
            temperature (float, optional):
                The temperature of the chatbot's responses. Defaults to 0.9.
            top_p (float, optional):
                The top_p of the chatbot's responses. Defaults to 0.95.
            stream (bool, optional):
                Whether to stream the responses or not. Defaults to False.
            tool_choice (str, optional):
                The tool choice mode. Defaults to "auto".
            tools (Optional[list[dict[str, Union[str, dict[str, str]]]]], optional):
                The tools to use. Defaults to None.

        Returns:
            ChatCompletionResponse | Generator[ChatCompletionResponse, None, None]:
                The response from the API or a generator of responses
        """
        json_body = {
            "messages": messages,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            "tool_choice": tool_choice,
            "tools": tools if tools else [],
        }

        if not stream:
            resp = self.client.post(url=self.url_path, json=json_body)
            return self._build_response(resp=resp)

        return self._build_stream_response(json_body=json_body)

    def _build_response(self, resp: httpx.Response) -> ChatCompletionResponse:
        """
        Builds a Chat Completion response from an HTTP response

        Args:
            resp (httpx.Response): The HTTP response

        Raises:
            Exception: If the HTTP response is not OK or if parsing the response fails

        Returns:
            ChatCompletionResponse: The response from the API
        """
        if resp.status_code != HTTPStatus.OK:
            raise Exception(f"status: {resp.status_code}; {resp.text}")

        try:
            chat_response = ChatCompletionResponse(**resp.json())
        except Exception as e:
            raise Exception(f"Failed to parse response: {e}")  # noqa: B904

        return chat_response

    def _build_stream_response(
        self, json_body: Dict[str, Any]
    ) -> Generator[ChatCompletionResponse, None, None]:
        """
        Builds a stream of Chat Completion responses from an HTTP response

        Args:
            json_body (dict): The JSON body of the request

        Yields:
            ChatCompletionResponse: The response from the API
        """
        with self.client.stream(
            method="post", url=self.url_path, json=json_body
        ) as resp:
            if resp.status_code != HTTPStatus.OK:
                raise Exception(f"status: {resp.status_code}; {resp.text}")

            for data in resp.iter_text():
                json_body = json.loads(data.split("data: ", 2)[1])

                yield ChatCompletionResponse(**json_body)

                # If the stream is finished, break out of the loop
                if "finish_reason" in json_body["choices"][0]:
                    break


class AsyncChatCompletions(BaseAsyncInterface, ChatCompletions):
    """Asynchronous Chat Completions interface"""

    async def create(
        self,
        *,
        messages: List[Dict[str, Union[str, List[Dict[str, Any]]]]],
        model: str = "abab5.5s-chat",
        max_tokens: int = 256,
        temperature: float = 0.9,
        top_p: float = 0.95,
        stream: bool = False,
        tool_choice: str = "auto",
        tools: Optional[List[Dict[str, Union[str, Dict[str, str]]]]] = None,
    ) -> Union[ChatCompletionResponse, AsyncGenerator[ChatCompletionResponse, None]]:
        """
        Create a new chat completion for the given messages.

        Args:
            messages (list[dict[str, Union[str, list[dict[str, Any]]]]]):
                The messages to generate responses to
            model (str, optional):
                The chatbot model to use. Defaults to "abab5.5s-chat".
            max_tokens (int, optional):
                The maximum number of tokens to generate. Defaults to 256.
            temperature (float, optional):
                The temperature of the chatbot's responses. Defaults to 0.9.
            top_p (float, optional):
                The top_p of the chatbot's responses. Defaults to 0.95.
            stream (bool, optional):
                Whether to stream the responses or not. Defaults to False.
            tool_choice (str, optional):
                The tool choice mode. Defaults to "auto".
            tools (Optional[list[dict[str, Union[str, dict[str, str]]]]], optional):
                The tools to use. Defaults to None.

        Returns:
            ChatCompletionResponse | AsyncGenerator[ChatCompletionResponse, None]:
                The response from the API or a generator of responses
        """
        json_body = {
            "messages": messages,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            "tool_choice": tool_choice,
            "tools": tools if tools else [],
        }

        if not stream:
            resp = await self.client.post(url=self.url_path, json=json_body)
            return self._build_response(resp=resp)

        return self._build_stream_response(json_body=json_body)

    async def _build_stream_response(
        self, json_body: Dict[str, Any]
    ) -> AsyncGenerator[ChatCompletionResponse, None]:
        """
        Builds a stream of Chat Completion responses from an HTTP response

        Args:
            json_body (dict): The JSON body of the request

        Yields:
            ChatCompletionResponse: The response from the API
        """
        async with self.client.stream(
            method="post", url=self.url_path, json=json_body
        ) as resp:
            if resp.status_code != HTTPStatus.OK:
                raise Exception(f"status: {resp.status_code}; {resp.text}")

            async for data in resp.aiter_text():
                json_body = json.loads(data.split("data: ", 2)[1])

                yield ChatCompletionResponse(**json_body)

                # If the stream is finished, break out of the loop
                if "finish_reason" in json_body["choices"][0]:
                    break


class Chat:
    """Synchronous Chat interface"""

    completions: ChatCompletions

    def __init__(self, http_client: httpx.Client) -> None:
        """
        Initializes the Chat interface

        Args:
            http_client (httpx.Client): The HTTP client to use
        """
        self.completions = ChatCompletions(http_client=http_client)


class AsyncChat:
    """Asynchronous Chat interface"""

    completions: AsyncChatCompletions

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        """
        Initializes the AsyncChat interface

        Args:
            http_client (httpx.AsyncClient): The HTTP client to use
        """
        self.completions = AsyncChatCompletions(http_client=http_client)
