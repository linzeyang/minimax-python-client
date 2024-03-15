"""embedding.py"""

from http import HTTPStatus
from typing import List, Union

import httpx

from minimax_client.entities.embedding import Response as ResponseEntity


class Embedding:
    """Embedding interface"""

    client: httpx.Client
    url_path: str = "embeddings"

    def __init__(self, http_client: httpx.Client) -> None:
        self.client = http_client

    def create(
        self,
        *,
        input: Union[str, List[str]],
        model: str = "embo-01",
        target: str = "db",
    ) -> ResponseEntity:
        """
        Create embeddings for the given input text(s).

        Args:
            input (str | list[str]): The input text(s) to embed.
            model (str, optional): The model to use. For now only embo-01 is available.
                Defaults to "embo-01".
            target (str, optional): The target scenario to use the embedding(s).
                Can be either "db" or "query". Defaults to "db".

        Returns:
            ResponseEntity: The response from the API.
        """
        if isinstance(input, str):
            input = [input]

        resp = self.client.post(
            url=self.url_path, json={"texts": input, "model": model, "type": target}
        )

        return self._build_response(resp=resp)

    def _build_response(self, resp: httpx.Response) -> ResponseEntity:
        """
        Builds an Embeddings response from an HTTP response

        Args:
            resp (httpx.Response): The HTTP response

        Raises:
            Exception: If the HTTP response is not OK or if parsing the response fails

        Returns:
            ResponseEntity: The Embeddings response
        """
        if resp.status_code != HTTPStatus.OK:
            raise Exception(f"status: {resp.status_code}; {resp.text}")

        try:
            response_entity = ResponseEntity(**resp.json())
        except Exception as e:
            raise Exception(f"Failed to parse response: {e}")  # noqa: B904

        return response_entity


class AsyncEmbedding(Embedding):
    """Asynchronous Embedding interface"""

    client: httpx.AsyncClient

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self.client = http_client

    async def create(
        self,
        *,
        input: Union[str, List[str]],
        model: str = "embo-01",
        target: str = "db",
    ) -> ResponseEntity:
        """
        Create embeddings for the given input text(s).

        Args:
            input (str | list[str]): The input text(s) to embed.
            model (str, optional): The model to use. For now only embo-01 is available.
                Defaults to "embo-01".
            target (str, optional): The target scenario to use the embedding(s).
                Can be either "db" or "query". Defaults to "db".

        Returns:
            ResponseEntity: The response from the API.
        """
        if isinstance(input, str):
            input = [input]

        resp = await self.client.post(
            url=self.url_path, json={"texts": input, "model": model, "type": target}
        )

        return self._build_response(resp=resp)
