"""assistant.py"""

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, PositiveInt

from minimax_client.entities.common import BareResponse


class AssistantToolFunction(BaseModel):
    """Assistant Tool Function"""

    description: str
    name: str
    parameters: Optional[Dict] = None


class AssistantTool(BaseModel):
    """Assistant Tool"""

    type: Literal["function", "code_interpreter", "web_search", "retrieval"]
    function: Optional[AssistantToolFunction] = None


class Assistant(BaseModel):
    """Assistant"""

    id: str
    object: Literal["assistant"]
    created_at: PositiveInt
    name: str
    description: str
    model: Literal[
        "abab6-chat",
        "abab5.5-chat",
        "abab5.5s-chat",
        "abab5.5-chat-240131",
        "abab5.5s-chat-240123",
    ]
    instructions: str
    tools: List[AssistantTool] = []
    file_ids: List[str] = []
    metadata: Dict = {}
    rolemeta: Dict
    status: str


class AssistantCreateResponse(BareResponse, Assistant):
    """Assistant Create Response"""


class AssistantRetrieveResponse(BareResponse, Assistant):
    """Assistant Retrieve Response"""


class AssistantUpdateResponse(BareResponse):
    """Assistant Update Response"""

    assistant: Assistant


class AssistantDeleteResponse(BareResponse):
    """Assistant Delete Response"""

    id: str
    object: Literal["assistant.deleted"]
    deleted: bool


class AssistantListResponse(BareResponse):
    """Assistant List Response"""

    object: Literal["list"]
    data: List[Assistant]
    has_more: bool
    first_id: str
    last_id: str
