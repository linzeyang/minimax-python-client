"""client.py"""

import asyncio
import os

import httpx
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel

BASE_URL = "https://api.minimax.chat/v1"


class ChatCompletionMessage(BaseModel):
    role: str
    content: str


class ChatCompletionChoice(BaseModel):
    message: ChatCompletionMessage
    index: int
    finish_reason: str


class ChatCompletionResponse(BaseModel):
    id: str
    choices: list[ChatCompletionChoice]
    created: int
    model: str
    object: str
    usage: dict[str, int]
    base_resp: dict


class Completions:
    """Completions interface"""

    client: httpx.Client
    url_path: str = "text/chatcompletion_v2"

    def __init__(self, http_client) -> None:
        self.client = http_client

    def create(
        self,
        *,
        messages: list[dict[str, str]],
        model: str = "abab5.5s-chat",
        max_tokens: int = 256,
        temperature: float = 0.9,
        top_p: float = 0.95,
        stream: bool = False,
    ) -> ChatCompletionResponse:
        resp = self.client.post(
            url=self.url_path,
            json={
                "messages": messages,
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "stream": stream,
                "tool_choice": "none",
            },
        )

        return self._build_response(resp)

    def _build_response(self, resp) -> ChatCompletionResponse:
        status_code = resp.status_code

        if status_code != 200:
            raise Exception(f"status: {status_code}; {resp.text}")

        resp_body = resp.json()

        try:
            chat_response = ChatCompletionResponse(**resp_body)
        except Exception as e:
            raise Exception(f"Failed to parse response: {e}")  # noqa: B904

        return chat_response


class AsyncCompletions(Completions):
    """Async completions interface"""

    client: httpx.AsyncClient

    async def create(
        self,
        *,
        messages: list[dict[str, str]],
        model: str = "abab5.5s-chat",
        max_tokens: int = 256,
        temperature: float = 0.9,
        top_p: float = 0.95,
        stream: bool = False,
    ) -> ChatCompletionResponse:
        resp = await self.client.post(
            url=self.url_path,
            json={
                "messages": messages,
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "stream": stream,
                "tool_choice": "none",
            },
        )

        return self._build_response(resp)


class Chat:
    """Chat interface"""

    client: httpx.Client
    completions: Completions

    def __init__(self, http_client: httpx.Client) -> None:
        self.client = http_client
        self.completions = Completions(self.client)


class AsyncChat:
    """Asnc chat interface"""

    client: httpx.AsyncClient
    completions: AsyncCompletions

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self.client = http_client
        self.completions = AsyncCompletions(self.client)


class MiniMax:
    """MiniMax client"""

    api_key: str
    http_client: httpx.Client
    chat: Chat

    def __init__(self, api_key: str | None = None) -> None:
        if api_key is None:
            api_key = self._get_api_key_from_env()

        self.api_key = api_key
        self.http_client = self._get_http_client()
        self.chat = Chat(self.http_client)

    def __del__(self):
        if not self.http_client.is_closed:
            self.http_client.close()

    def _get_api_key_from_env(self) -> str:
        env_file = find_dotenv()

        if env_file:
            load_dotenv(env_file)

        api_key = os.getenv("MINIMAX_API_KEY")

        if not api_key:
            raise ValueError("A valid MiniMax api key must be provided!")

        return api_key

    def _get_http_client(self) -> httpx.Client:
        return httpx.Client(
            base_url=BASE_URL, headers={"Authorization": f"Bearer {self.api_key}"}
        )


class AsyncMiniMax(MiniMax):
    http_client: httpx.AsyncClient
    chat: AsyncChat

    def __init__(self, api_key: str | None = None) -> None:
        super().__init__(api_key)
        self.chat = AsyncChat(self.http_client)

    def _get_http_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=BASE_URL, headers={"Authorization": f"Bearer {self.api_key}"}
        )

    def __del__(self):
        async def __del_client():
            if not self.http_client.is_closed:
                await self.http_client.aclose()

        asyncio.create_task(__del_client())
