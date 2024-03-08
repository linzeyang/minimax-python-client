"""client.py"""

import asyncio
import json
import os
from http import HTTPStatus
from typing import Any, AsyncGenerator, Generator, Optional, Union

import httpx
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel

BASE_URL = "https://api.minimax.chat/v1"


class ChatCompletionChoiceMessage(BaseModel):
    role: str
    content: str


class ChatCompletionChoice(BaseModel):
    index: int
    message: Optional[ChatCompletionChoiceMessage] = None
    delta: Optional[ChatCompletionChoiceMessage] = None
    finish_reason: Optional[str] = None


class ChatCompletionResponse(BaseModel):
    id: str
    choices: list[ChatCompletionChoice]
    created: int
    model: str
    object: str
    usage: Optional[dict[str, int]] = None
    base_resp: Optional[dict[str, Any]] = None


class Completions:
    """Completions interface"""

    client: httpx.Client
    url_path: str = "text/chatcompletion_v2"

    def __init__(self, http_client: httpx.Client) -> None:
        self.client = http_client

    def create(
        self,
        *,
        messages: list[dict[str, Union[str, list[dict[str, Any]]]]],
        model: str = "abab5.5s-chat",
        max_tokens: int = 256,
        temperature: float = 0.9,
        top_p: float = 0.95,
        stream: bool = False,
        tool_choice: str = "auto",
        tools: Optional[list[dict[str, dict[str, str]]]] = None,
    ) -> Union[ChatCompletionResponse, Generator]:
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
            return self._build_response(resp)

        return self._build_stream_response(json_body=json_body)

    def _build_response(self, resp: httpx.Response) -> ChatCompletionResponse:
        if resp.status_code != HTTPStatus.OK:
            raise Exception(f"status: {resp.status_code}; {resp.text}")

        try:
            chat_response = ChatCompletionResponse(**resp.json())
        except Exception as e:
            raise Exception(f"Failed to parse response: {e}")  # noqa: B904

        return chat_response

    def _build_stream_response(self, json_body: dict) -> Generator:
        with self.client.stream(
            method="post", url=self.url_path, json=json_body
        ) as resp:
            if resp.status_code != HTTPStatus.OK:
                raise Exception(f"status: {resp.status_code}; {resp.text}")

            for data in resp.iter_text():
                json_body = json.loads(data.split("data: ", 2)[1])

                yield ChatCompletionResponse(**json_body)

                if "finish_reason" in json_body["choices"][0]:
                    break


class AsyncCompletions(Completions):
    """Async completions interface"""

    client: httpx.AsyncClient

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self.client = http_client

    async def create(
        self,
        *,
        messages: list[dict[str, Union[str, list[dict[str, Any]]]]],
        model: str = "abab5.5s-chat",
        max_tokens: int = 256,
        temperature: float = 0.9,
        top_p: float = 0.95,
        stream: bool = False,
        tool_choice: str = "auto",
        tools: Optional[list[dict[str, dict[str, str]]]] = None,
    ) -> Union[ChatCompletionResponse, AsyncGenerator]:
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
            return self._build_response(resp)

        return self._build_stream_response(json_body=json_body)

    async def _build_stream_response(self, json_body: dict) -> AsyncGenerator:
        async with self.client.stream(
            method="post", url=self.url_path, json=json_body
        ) as resp:
            if resp.status_code != HTTPStatus.OK:
                raise Exception(f"status: {resp.status_code}; {resp.text}")

            async for data in resp.aiter_text():
                json_body = json.loads(data.split("data: ", 2)[1])

                yield ChatCompletionResponse(**json_body)

                if "finish_reason" in json_body["choices"][0]:
                    break


class Chat:
    """Chat interface"""

    client: httpx.Client
    completions: Completions

    def __init__(self, http_client: httpx.Client) -> None:
        self.client = http_client
        self.completions = Completions(self.client)


class AsyncChat:
    """Async chat interface"""

    client: httpx.AsyncClient
    completions: AsyncCompletions

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self.client = http_client
        self.completions = AsyncCompletions(self.client)


class BaseMiniMaxClient:
    """MiniMax client base class"""

    api_key: str

    def __init__(self, api_key: str | None = None) -> None:
        if not api_key:
            api_key = self._get_api_key_from_env()

        self.api_key = api_key
        self.http_client = self._get_http_client()

    def _get_api_key_from_env(self) -> str:
        env_file = find_dotenv()

        if env_file:
            load_dotenv(env_file)

        api_key = os.getenv("MINIMAX_API_KEY")

        if not api_key:
            raise ValueError("A valid MiniMax api key must be provided!")

        return api_key

    def _get_http_client(self):
        raise NotImplementedError


class MiniMax(BaseMiniMaxClient):
    """MiniMax client"""

    http_client: httpx.Client
    chat: Chat

    def __init__(self, api_key: str | None = None) -> None:
        super().__init__(api_key)
        self.chat = Chat(self.http_client)

    def __del__(self):
        if not self.http_client.is_closed:
            self.http_client.close()

    def _get_http_client(self) -> httpx.Client:
        return httpx.Client(
            base_url=BASE_URL, headers={"Authorization": f"Bearer {self.api_key}"}
        )


class AsyncMiniMax(BaseMiniMaxClient):
    """MiniMax async client"""

    http_client: httpx.AsyncClient
    chat: AsyncChat

    def __init__(self, api_key: str | None = None) -> None:
        super().__init__(api_key)
        self.chat = AsyncChat(self.http_client)

    def __del__(self):
        async def __del_client():
            if not self.http_client.is_closed:
                await self.http_client.aclose()

        asyncio.create_task(__del_client())

    def _get_http_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=BASE_URL, headers={"Authorization": f"Bearer {self.api_key}"}
        )
