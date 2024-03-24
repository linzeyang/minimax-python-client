"""file.py"""

from pathlib import Path
from typing import Literal, Union

from minimax_client.entities.file import (
    FileCreateResponse,
    FileDeleteResponse,
    FileListResponse,
    FileRetrieveContentResponse,
    FileRetriveResponse,
)
from minimax_client.interfaces.base import BaseAsyncInterface, BaseSyncInterface


class Files(BaseSyncInterface):
    """Synchronous Files interface"""

    url_path: str = "files"

    def create(
        self,
        filepath: Union[str, Path],
        *,
        purpose: Literal[
            "retrieval",
            "fine-tune",
            "fine-tune-result",
            "voice_clone",
            "assistants",
            "role-recognition",
        ] = "retrieval",
    ) -> FileCreateResponse:
        """Upload a file

        Args:
            filepath (Union[str, Path]): The path to the file to upload
            purpose (Literal[
                "retrieval",
                "fine-tune",
                "fine-tune-result",
                "voice_clone",
                "assistants",
                "role-recognition"
            ], optional): The purpose of the file. Defaults to "retrieval".

        Raises:
            FileNotFoundError: If the file does not exist or is not a file

        Returns:
            FileCreateResponse: The response from the API
        """
        if isinstance(filepath, str):
            filepath = Path(filepath)

        if not filepath.exists() or not filepath.is_file():
            raise FileNotFoundError(f"{filepath} does not exist or is not a file")

        with filepath.open("rb") as file:
            resp = self.client.post(
                url=f"{self.url_path}/upload",
                files={"file": file},
                data={"purpose": purpose},
            )

        return FileCreateResponse(**resp.json())

    def list(
        self,
        purpose: Literal[
            "retrieval",
            "fine-tune",
            "fine-tune-result",
            "voice_clone",
            "assistants",
            "role-recognition",
        ] = "retrieval",
    ) -> FileListResponse:
        """Get the list of files under given purpose

        Args:
            purpose (Literal[
                "retrieval",
                "fine-tune",
                "fine-tune-result",
                "voice_clone",
                "assistants",
                "role-recognition"
            ], optional): The purpose of the files to list. Defaults to "retrieval".

        Returns:
            FileListResponse: The response from the API
        """
        resp = self.client.get(url=f"{self.url_path}/list", params={"purpose": purpose})

        return FileListResponse(**resp.json())

    def retrieve(self, file_id: int) -> FileRetriveResponse:
        """Retrieve general info of the given file

        Args:
            file_id (int): The ID of the file to retrieve

        Returns:
            FileRetriveResponse: The response from the API
        """
        resp = self.client.get(
            url=f"{self.url_path}/retrieve", params={"file_id": file_id}
        )

        return FileRetriveResponse(**resp.json())

    def content(self, file_id: int) -> FileRetrieveContentResponse:
        """Retrieve the content of the given file

        Args:
            file_id (int): The ID of the file to retrieve the content of

        Returns:
            FileRetrieveContentResponse: The response from the API
        """
        # TODO: clarify

        resp = self.client.get(
            url=f"{self.url_path}/retrieve_content",
            params={"file_id": file_id},
        )

        return FileRetrieveContentResponse(**resp.json())

    def delete(self, file_id: int) -> FileDeleteResponse:
        """Delete a file

        Args:
            file_id (int): The ID of the file to delete

        Returns:
            FileDeleteResponse: The response from the API
        """
        resp = self.client.post(f"{self.url_path}/delete", json={"file_id": file_id})

        return FileDeleteResponse(**resp.json())


class AsyncFiles(BaseAsyncInterface, Files):
    """Asynchronous Files interface"""

    async def create(
        self,
        filepath: Union[str, Path],
        *,
        purpose: Literal[
            "retrieval",
            "fine-tune",
            "fine-tune-result",
            "voice_clone",
            "assistants",
            "role-recognition",
        ] = "retrieval",
    ) -> FileCreateResponse:
        """Upload a file

        Args:
            filepath (Union[str, Path]): The path to the file to upload
            purpose (Literal[
                "retrieval",
                "fine-tune",
                "fine-tune-result",
                "voice_clone",
                "assistants",
                "role-recognition"
            ], optional): The purpose of the file. Defaults to "retrieval".

        Raises:
            FileNotFoundError: If the file does not exist or is not a file

        Returns:
            FileCreateResponse: The response from the API
        """
        if isinstance(filepath, str):
            filepath = Path(filepath)

        if not filepath.exists() or not filepath.is_file():
            raise FileNotFoundError(f"{filepath} does not exist or is not a file")

        with filepath.open("rb") as file:
            resp = await self.client.post(
                url=f"{self.url_path}/upload",
                files={"file": file},
                data={"purpose": purpose},
            )

        return FileCreateResponse(**resp.json())

    async def list(
        self,
        purpose: Literal[
            "retrieval",
            "fine-tune",
            "fine-tune-result",
            "voice_clone",
            "assistants",
            "role-recognition",
        ] = "retrieval",
    ) -> FileListResponse:
        """Get the list of files under given purpose

        Args:
            purpose (Literal[
                "retrieval",
                "fine-tune",
                "fine-tune-result",
                "voice_clone",
                "assistants",
                "role-recognition"
            ], optional): The purpose of the files to list. Defaults to "retrieval".

        Returns:
            FileListResponse: The response from the API
        """
        resp = await self.client.get(
            url=f"{self.url_path}/list", params={"purpose": purpose}
        )

        return FileListResponse(**resp.json())

    async def retrieve(self, file_id: int) -> FileRetriveResponse:
        """Retrieve general info of the given file

        Args:
            file_id (int): The ID of the file to retrieve

        Returns:
            FileRetriveResponse: The response from the API
        """
        resp = await self.client.get(
            url=f"{self.url_path}/retrieve", params={"file_id": file_id}
        )

        return FileRetriveResponse(**resp.json())

    async def content(self, file_id: int) -> FileRetrieveContentResponse:
        """Retrieve the content of the given file

        Args:
            file_id (int): The ID of the file to retrieve the content of

        Returns:
            FileRetrieveContentResponse: The response from the API
        """
        # TODO: clarify

        resp = await self.client.get(
            url=f"{self.url_path}/retrieve_content",
            params={"file_id": file_id},
        )

        return FileRetrieveContentResponse(**resp.json())  # to be confirmed

    async def delete(self, file_id: int) -> FileDeleteResponse:
        """Delete a file

        Args:
            file_id (int): The ID of the file to delete

        Returns:
            FileDeleteResponse: The response from the API
        """
        resp = await self.client.post(
            f"{self.url_path}/delete", json={"file_id": file_id}
        )

        return FileDeleteResponse(**resp.json())
