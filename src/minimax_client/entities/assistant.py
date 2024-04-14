"""assistant.py"""

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, PositiveInt

from minimax_client.entities.common import BareResponse


class AssistantToolFunctionParameters(BaseModel):
    """Assistant Tool Function Parameters"""

    type: Literal["object"]
    required: List[str]
    properties: Dict[str, Dict]


class AssistantToolFunction(BaseModel):
    """Assistant Tool Function"""

    description: str
    name: str
    parameters: Optional[AssistantToolFunctionParameters] = None


class AssistantTool(BaseModel):
    """Assistant Tool"""

    type: Literal["code_interpreter", "retrieval", "function", "web_search"]
    function: Optional[AssistantToolFunction] = None


class AssistantT2AOption(BaseModel):
    """Assistant T2A Option"""

    model: str
    voice_id: str
    format: Literal["mp3", "flac", "pcm"] = "mp3"


class Assistant(BaseModel):
    """Assistant"""

    id: str
    object: Literal["assistant"]
    created_at: PositiveInt
    updated_at: Optional[PositiveInt] = None
    name: str
    description: str
    model: Literal[
        "abab6-chat",
        "abab5.5-chat",
        "abab5.5-chat-240131",
        "abab5.5s-chat",
        "abab5.5s-chat-240123",
    ]
    instructions: str
    tools: List[AssistantTool] = []
    file_ids: List[str] = []
    metadata: Dict = {}
    rolemeta: Dict
    status: str
    t2a_option: Optional[AssistantT2AOption] = None


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


class AssistantFile(BaseModel):
    """Assistant File"""

    id: str
    object: Literal["assistant.file"]
    created_at: PositiveInt
    assistant_id: str


class AssistantFileCreateResponse(BareResponse, AssistantFile):
    """Assistant File Create Response"""


class AssistantFileRetrieveResponse(BareResponse, AssistantFile):
    """Assistant File Retrieve Response"""


class AssistantFileListResponse(BareResponse):
    """Assistant File List Response"""

    object: Literal["list"]
    data: List[AssistantFile]


class AssistantFileDeleteResponse(BareResponse):
    """Assistant File Delete Response"""

    file_id: str
