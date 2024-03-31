"""assistant.py"""

from typing import Any, Dict, List, Literal, Optional, Union

from minimax_client.entities.assistant import (
    AssistantCreateResponse,
    AssistantDeleteResponse,
    AssistantListResponse,
    AssistantRetrieveResponse,
    AssistantUpdateResponse,
)
from minimax_client.interfaces.base import BaseAsyncInterface, BaseSyncInterface


class Assistant(BaseSyncInterface):
    """Synchronous Assistants interface"""

    url_path = "assistants"

    def create(
        self,
        *,
        model: Literal[
            "abab6-chat",
            "abab5.5-chat",
            "abab5.5s-chat",
            "abab5.5-chat-240131",
            "abab5.5s-chat-240123",
        ],
        name: Optional[str] = None,
        instructions: Optional[str] = None,
        description: Optional[str] = None,
        tools: Optional[List[Dict[str, Union[str, Dict]]]] = None,
        file_ids: Optional[List[str]] = None,
        rolemeta: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, str]] = None,
        t2a_option: Optional[Dict[str, str]] = None,
    ) -> AssistantCreateResponse:
        """
        Create a new assistant

        Args:
            model (Literal["abab6-chat", "abab5.5-chat", "abab5.5s-chat",
                "abab5.5-chat-240131", "abab5.5s-chat-240123"]):
                The model to use for the assistant
            name (Optional[str], optional): The name of the assistant. Defaults to None.
            instructions (Optional[str], optional):
                The instructions for the assistant. Defaults to None.
            description (Optional[str], optional):
                The description of the assistant. Defaults to None.
            tools (Optional[List[Dict[str, Union[str, Dict]]]], optional):
                The tools to use for the assistant. Defaults to None.
            file_ids (Optional[List[str]], optional):
                The file IDs to use for the assistant. Defaults to None.
            rolemeta (Optional[Dict[str, str]], optional):
                The rolemeta to use for the assistant. Defaults to None.
            metadata (Optional[Dict[str, str]], optional):
                The metadata to use for the assistant. Defaults to None.
            t2a_option (Optional[Dict[str, str]], optional):
                The t2a_option to use for the assistant. Defaults to None.

        Returns:
            AssistantCreateResponse:
                The response of the API containing the created assistant
        """
        json_body: Dict[str, Any] = {"model": model}

        if name:
            json_body["name"] = name
        if instructions:
            json_body["instructions"] = instructions
        if description:
            json_body["description"] = description
        if tools:
            json_body["tools"] = tools
        if file_ids:
            json_body["file_ids"] = file_ids
        if rolemeta:
            json_body["rolemeta"] = rolemeta
        if metadata:
            json_body["metadata"] = metadata
        if t2a_option:
            json_body["t2a_option"] = t2a_option

        resp = self.client.post(url=f"{self.url_path}/create", json=json_body)

        return AssistantCreateResponse(**resp.json())

    def retrieve(self, assistant_id: str) -> AssistantRetrieveResponse:
        """
        Retrieve an assistant

        Args:
            assistant_id (str): The ID of the assistant to retrieve

        Returns:
            Assistant: The response of the API containing the retrieved assistant
        """
        resp = self.client.get(
            url=f"{self.url_path}/retrieve", params={"assistant_id": assistant_id}
        )

        return AssistantRetrieveResponse(**resp.json())

    def update(
        self,
        assistant_id: str,
        *,
        model: Literal[
            "abab6-chat",
            "abab5.5-chat",
            "abab5.5s-chat",
            "abab5.5-chat-240131",
            "abab5.5s-chat-240123",
        ],
        name: str,
        instructions: str,
        description: Optional[str] = None,
        tools: Optional[List[Dict[str, Union[str, Dict]]]] = None,
        file_ids: Optional[List[str]] = None,
        rolemeta: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, str]] = None,
        t2a_option: Optional[Dict[str, str]] = None,
    ) -> AssistantUpdateResponse:
        """
        Update an assistant

        Args:
            assistant_id (str): The ID of the assistant to update
            model (Literal["abab6-chat", "abab5.5-chat", "abab5.5s-chat",
                "abab5.5-chat-240131", "abab5.5s-chat-240123"]):
                The model to use for the assistant
            name (str): The name of the assistant
            instructions (str): The instructions for the assistant
            description (Optional[str], optional):
                The description of the assistant. Defaults to None.
            tools (Optional[List[Dict[str, Union[str, Dict]]]], optional):
                The tools to use for the assistant. Defaults to None.
            file_ids (Optional[List[str]], optional):
                The file IDs to use for the assistant. Defaults to None.
            rolemeta (Optional[Dict[str, str]], optional):
                The rolemeta to use for the assistant. Defaults to None.
            metadata (Optional[Dict[str, str]], optional):
                The metadata to use for the assistant. Defaults to None.
            t2a_option (Optional[Dict[str, str]], optional):
                The t2a_option to use for the assistant. Defaults to None.

        Returns:
            AssistantUpdateResponse:
                The response of the API containing the updated assistant
        """
        json_body: Dict[str, Any] = {
            "id": assistant_id,
            "model": model,
            "name": name,
            "instructions": instructions,
        }

        if description:
            json_body["description"] = description
        if tools:
            json_body["tools"] = tools
        if file_ids:
            json_body["file_ids"] = file_ids
        if rolemeta:
            json_body["rolemeta"] = rolemeta
        if metadata:
            json_body["metadata"] = metadata
        if t2a_option:
            json_body["t2a_option"] = t2a_option

        resp = self.client.post(url=f"{self.url_path}/modify", json=json_body)

        return AssistantUpdateResponse(**resp.json())

    def delete(self, assistant_id: str) -> AssistantDeleteResponse:
        """
        Delete an assistant

        Args:
            assistant_id (str): The ID of the assistant to delete

        Returns:
            AssistantDeleteResponse: The response from the API
        """
        resp = self.client.post(
            url=f"{self.url_path}/delete", json={"assistant_id": assistant_id}
        )

        return AssistantDeleteResponse(**resp.json())

    def list(
        self,
        limit: int = 20,
        order: Literal["asc", "desc"] = "desc",
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> AssistantListResponse:
        """
        List all assistants

        Args:
            limit (int): The number of assistants to return. Defaults to 20.
            order (str):
                The order of the list, could be "asc" or "desc". Defaults to "desc".
            after (Optional[str], optional):
                The ID of the assistant to start after. Defaults to None.
            before (Optional[str], optional):
                The ID of the assistant to end before. Defaults to None.

        Returns:
            AssistantListResponse:
                The response from the API containing the list of assistants
        """
        params = {"limit": limit, "order": order}

        if after:
            params["after"] = after
        if before:
            params["before"] = before

        resp = self.client.get(url=f"{self.url_path}/list", params=params)

        return AssistantListResponse(**resp.json())


class AsyncAssistant(BaseAsyncInterface, Assistant):
    """Asynchronous Assistants interface"""

    async def create(
        self,
        *,
        model: Literal[
            "abab6-chat",
            "abab5.5-chat",
            "abab5.5s-chat",
            "abab5.5-chat-240131",
            "abab5.5s-chat-240123",
        ],
        name: Optional[str] = None,
        instructions: Optional[str] = None,
        description: Optional[str] = None,
        tools: Optional[List[Dict[str, Union[str, Dict]]]] = None,
        file_ids: Optional[List[str]] = None,
        rolemeta: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, str]] = None,
        t2a_option: Optional[Dict[str, str]] = None,
    ) -> AssistantCreateResponse:
        """
        Create a new assistant

        Args:
            model (Literal["abab6-chat", "abab5.5-chat", "abab5.5s-chat",
                "abab5.5-chat-240131", "abab5.5s-chat-240123"]):
                The model to use for the assistant
            name (Optional[str], optional): The name of the assistant. Defaults to None.
            instructions (Optional[str], optional):
                The instructions for the assistant. Defaults to None.
            description (Optional[str], optional):
                The description of the assistant. Defaults to None.
            tools (Optional[List[Dict[str, Union[str, Dict]]]], optional):
                The tools to use for the assistant. Defaults to None.
            file_ids (Optional[List[str]], optional):
                The file IDs to use for the assistant. Defaults to None.
            rolemeta (Optional[Dict[str, str]], optional):
                The rolemeta to use for the assistant. Defaults to None.
            metadata (Optional[Dict[str, str]], optional):
                The metadata to use for the assistant. Defaults to None.
            t2a_option (Optional[Dict[str, str]], optional):
                The t2a_option to use for the assistant. Defaults to None.

        Returns:
            AssistantCreateResponse:
                The response of the API containing the created assistant
        """
        json_body: Dict[str, Any] = {"model": model}

        if name:
            json_body["name"] = name
        if instructions:
            json_body["instructions"] = instructions
        if description:
            json_body["description"] = description
        if tools:
            json_body["tools"] = tools
        if file_ids:
            json_body["file_ids"] = file_ids
        if rolemeta:
            json_body["rolemeta"] = rolemeta
        if metadata:
            json_body["metadata"] = metadata
        if t2a_option:
            json_body["t2a_option"] = t2a_option

        resp = await self.client.post(url=f"{self.url_path}/create", json=json_body)

        return AssistantCreateResponse(**resp.json())

    async def retrieve(self, assistant_id: str) -> AssistantRetrieveResponse:
        """
        Retrieve an assistant

        Args:
            assistant_id (str): The ID of the assistant to retrieve

        Returns:
            Assistant: The response of the API containing the retrieved assistant
        """
        resp = await self.client.get(
            url=f"{self.url_path}/retrieve", params={"assistant_id": assistant_id}
        )

        return AssistantRetrieveResponse(**resp.json())

    async def update(
        self,
        assistant_id: str,
        *,
        model: Literal[
            "abab6-chat",
            "abab5.5-chat",
            "abab5.5s-chat",
            "abab5.5-chat-240131",
            "abab5.5s-chat-240123",
        ],
        name: str,
        instructions: str,
        description: Optional[str] = None,
        tools: Optional[List[Dict[str, Union[str, Dict]]]] = None,
        file_ids: Optional[List[str]] = None,
        rolemeta: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, str]] = None,
        t2a_option: Optional[Dict[str, str]] = None,
    ) -> AssistantUpdateResponse:
        """
        Update an assistant

        Args:
            assistant_id (str): The ID of the assistant to update
            model (Literal["abab6-chat", "abab5.5-chat", "abab5.5s-chat",
                "abab5.5-chat-240131", "abab5.5s-chat-240123"]):
                The model to use for the assistant
            name (str): The name of the assistant
            instructions (str): The instructions for the assistant
            description (Optional[str], optional):
                The description of the assistant. Defaults to None.
            tools (Optional[List[Dict[str, Union[str, Dict]]]], optional):
                The tools to use for the assistant. Defaults to None.
            file_ids (Optional[List[str]], optional):
                The file IDs to use for the assistant. Defaults to None.
            rolemeta (Optional[Dict[str, str]], optional):
                The rolemeta to use for the assistant. Defaults to None.
            metadata (Optional[Dict[str, str]], optional):
                The metadata to use for the assistant. Defaults to None.
            t2a_option (Optional[Dict[str, str]], optional):
                The t2a_option to use for the assistant. Defaults to None.

        Returns:
            AssistantUpdateResponse:
                The response of the API containing the updated assistant
        """
        json_body: Dict[str, Any] = {
            "id": assistant_id,
            "model": model,
            "name": name,
            "instructions": instructions,
        }

        if description:
            json_body["description"] = description
        if tools:
            json_body["tools"] = tools
        if file_ids:
            json_body["file_ids"] = file_ids
        if rolemeta:
            json_body["rolemeta"] = rolemeta
        if metadata:
            json_body["metadata"] = metadata
        if t2a_option:
            json_body["t2a_option"] = t2a_option

        resp = await self.client.post(url=f"{self.url_path}/modify", json=json_body)

        return AssistantUpdateResponse(**resp.json())

    async def delete(self, assistant_id: str) -> AssistantDeleteResponse:
        """
        Delete an assistant

        Args:
            assistant_id (str): The ID of the assistant to delete

        Returns:
            AssistantDeleteResponse: The response from the API
        """
        resp = await self.client.post(
            url=f"{self.url_path}/delete", json={"assistant_id": assistant_id}
        )

        return AssistantDeleteResponse(**resp.json())

    async def list(
        self,
        limit: int = 20,
        order: Literal["asc", "desc"] = "desc",
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> AssistantListResponse:
        """
        List all assistants

        Args:
            limit (int): The number of assistants to return. Defaults to 20.
            order (str):
                The order of the list, could be "asc" or "desc". Defaults to "desc".
            after (Optional[str], optional):
                The ID of the assistant to start after. Defaults to None.
            before (Optional[str], optional):
                The ID of the assistant to end before. Defaults to None.

        Returns:
            AssistantListResponse:
                The response from the API containing the list of assistants
        """
        params = {"limit": limit, "order": order}

        if after:
            params["after"] = after
        if before:
            params["before"] = before

        resp = await self.client.get(url=f"{self.url_path}/list", params=params)

        return AssistantListResponse(**resp.json())
