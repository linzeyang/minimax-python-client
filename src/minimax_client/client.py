"""client.py"""

import asyncio
import os
from typing import Optional

import httpx
from dotenv import find_dotenv, load_dotenv

from minimax_client.interfaces.assistant import Assistant, AsyncAssistant
from minimax_client.interfaces.chat_completion import AsyncChat, Chat
from minimax_client.interfaces.embedding import AsyncEmbedding, Embedding
from minimax_client.interfaces.file import AsyncFiles, Files
from minimax_client.interfaces.fine_tuning import (
    AsyncFineTuning,
    AsyncModel,
    FineTuning,
    Model,
)

BASE_URL = "https://api.minimax.chat/v1"


class BaseMiniMaxClient:
    """MiniMax client base class"""

    api_key: str
    group_id: str
    timeout: float

    def __init__(
        self,
        api_key: Optional[str] = None,
        group_id: Optional[str] = None,
        timeout: float = 60,
    ) -> None:
        if not api_key:
            api_key = self._get_api_key_from_env()

        if not group_id:
            group_id = os.getenv("MINIMAX_GROUP_ID", "")

        self.api_key = api_key
        self.group_id = group_id
        self.timeout = timeout
        self.http_client = self._get_http_client()

    def _get_api_key_from_env(self) -> str:
        """
        Retrieves the MiniMax API key from the environment.

        First it tries to find a `.env` file in the current
        directory or any of its parent directories. If such a file is found,
        it loads the environment variables from it.

        Then, it retrieves the `MINIMAX_API_KEY` environment variable. If it
        contains a valid API key, it returns it. Otherwise, it raises a
        `ValueError`.

        Returns:
            str: The MiniMax API key.
        """
        env_file = find_dotenv()

        if env_file:
            load_dotenv(dotenv_path=env_file)

        api_key = os.getenv("MINIMAX_API_KEY")

        if not api_key:
            raise ValueError("A valid MiniMax API key must be provided!")

        return api_key

    def _get_http_client(self):
        raise NotImplementedError


class MiniMax(BaseMiniMaxClient):
    """MiniMax client"""

    http_client: httpx.Client
    assistants: Assistant
    chat: Chat
    embeddings: Embedding
    files: Files
    fine_tuning: FineTuning
    model: Model

    def __init__(self, *, api_key: Optional[str] = None, timeout: float = 60) -> None:
        super().__init__(api_key=api_key, timeout=timeout)
        self.assistants = Assistant(http_client=self.http_client)
        self.chat = Chat(http_client=self.http_client)
        self.embeddings = Embedding(http_client=self.http_client)
        self.files = Files(http_client=self.http_client)
        self.fine_tuning = FineTuning(http_client=self.http_client)
        self.model = Model(http_client=self.http_client)

    def __del__(self) -> None:
        """Closes the HTTP client if it is not already closed."""
        if hasattr(self, "http_client") and not self.http_client.is_closed:
            self.http_client.close()

    def _get_http_client(self) -> httpx.Client:
        """
        Returns a synchronous HTTP client with the base URL and authentication
        header configured.

        The client is configured to send requests to the MiniMax API with the
        provided API key.

        Returns:
            httpx.Client: The synchronous HTTP client.
        """
        return httpx.Client(
            base_url=BASE_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=self.timeout,
        )


class AsyncMiniMax(BaseMiniMaxClient):
    """MiniMax async client"""

    http_client: httpx.AsyncClient
    assistants: AsyncAssistant
    chat: AsyncChat
    embeddings: AsyncEmbedding
    files: AsyncFiles
    fine_tuning: AsyncFineTuning
    model: AsyncModel

    def __init__(self, *, api_key: Optional[str] = None, timeout: float = 60) -> None:
        super().__init__(api_key=api_key, timeout=timeout)
        self.assistants = AsyncAssistant(http_client=self.http_client)
        self.chat = AsyncChat(http_client=self.http_client)
        self.embeddings = AsyncEmbedding(http_client=self.http_client)
        self.files = AsyncFiles(http_client=self.http_client)
        self.fine_tuning = AsyncFineTuning(http_client=self.http_client)
        self.model = AsyncModel(http_client=self.http_client)

    def __del__(self) -> None:
        async def __del_client() -> None:
            """
            Closes the async HTTP client if it is not already closed.

            This coroutine is called when the AsyncMiniMax instance is garbage
            collected. It asynchronously closes the HTTP client if it is not
            already closed.
            """
            if hasattr(self, "http_client") and not self.http_client.is_closed:
                await self.http_client.aclose()

        # Create a task to close the HTTP client. This task is scheduled to run
        # asyncio's event loop, but it does not block the interpreter from
        # exiting.
        asyncio.create_task(__del_client())

    def _get_http_client(self) -> httpx.AsyncClient:
        """
        Returns a new asynchronous HTTP client with the base URL and
        authentication header configured.

        The client is configured to send requests to the MiniMax API with the
        provided API key.

        Returns:
            httpx.AsyncClient: The asynchronous HTTP client.
        """
        return httpx.AsyncClient(
            base_url=BASE_URL,
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=self.timeout,
        )
