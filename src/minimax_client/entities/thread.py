"""thread.py"""

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, HttpUrl, NonNegativeInt

from minimax_client.entities.assistant import AssistantTool
from minimax_client.entities.common import BareResponse


class Thread(BaseModel):
    """Thread"""

    id: str
    object: Literal["thread"]
    created_at: NonNegativeInt
    metadata: Dict[str, str] = {}
    updated_at: Optional[NonNegativeInt] = None


class ThreadCreateResponse(BareResponse, Thread):
    """Thread Create Response"""


class ThreadRetrieveResponse(BareResponse, Thread):
    """Thread Retrieve Response"""


class ThreadUpdateResponse(BareResponse):
    """Thread Update Response"""

    thread: Thread


class MessageTextContentAnnotationFileCitation(BaseModel):
    """Message Text Content Annotation File Citation"""

    file_id: str
    quote: str


class MessageTextContentAnnotationWebCitation(BaseModel):
    """Message Text Content Annotation Web Citation"""

    url: HttpUrl
    quote: str


class MessageTextContentAnnotation(BaseModel):
    """Message Text Content Annotation"""

    type: str
    text: str
    start_index: NonNegativeInt
    end_index: NonNegativeInt
    file_citation: Optional[MessageTextContentAnnotationFileCitation] = None
    web_citation: Optional[MessageTextContentAnnotationWebCitation] = None


class MessageTextContent(BaseModel):
    """Message Text Content"""

    value: str
    annotations: List[MessageTextContentAnnotation] = []


class MessageImageFile(BaseModel):
    """Message Image File"""

    file_id: str


class MessageContent(BaseModel):
    """Message Content"""

    type: str
    text: Optional[MessageTextContent] = None
    image_file: Optional[MessageImageFile] = None


class Message(BaseModel):
    """Message"""

    id: str
    object: Literal["message"]
    created_at: NonNegativeInt
    thread_id: str
    role: str
    content: List[MessageContent] = []
    file_ids: Optional[List[str]] = None
    assistant_id: str
    run_id: str
    metadata: Dict[str, str] = {}
    updated_at: Optional[NonNegativeInt] = None


class MessageCreateResponse(BareResponse, Message):
    """Message Create Response"""


class MessageRetrieveResponse(BareResponse, Message):
    """Message Retrieve Response"""


class MessageListResponse(BareResponse):
    """Message List Response"""

    object: Literal["list"]
    data: List[Message]
    first_id: str
    last_id: str


class RunError(BaseModel):
    """Run Error"""

    code: str
    message: str


class Run(BaseModel):
    """Run"""

    id: str
    object: Literal["run"]
    created_at: NonNegativeInt
    assistant_id: str
    thread_id: str
    status: str
    started_at: Optional[NonNegativeInt] = None
    expires_at: Optional[NonNegativeInt] = None
    cancelled_at: Optional[NonNegativeInt] = None
    failed_at: Optional[NonNegativeInt] = None
    completed_at: Optional[NonNegativeInt] = None
    updated_at: Optional[NonNegativeInt] = None
    last_error: Optional[RunError] = None
    model: Literal[
        "abab6-chat",
        "abab5.5-chat",
        "abab5.5-chat-240131",
        "abab5.5s-chat",
        "abab5.5s-chat-240123",
    ]
    t2a_option: Optional[Dict[str, str]] = None
    instructions: str
    tools: List[AssistantTool] = []
    file_ids: List[str] = []
    metadata: Dict[str, str] = {}


class RunCreateResponse(BareResponse, Run):
    """Run Create Response"""


class RunRetrieveResponse(BareResponse, Run):
    """Run Retrieve Response"""


class RunListResponse(BareResponse):
    """Run List Response"""

    object: Literal["list"]
    data: List[Run]


class RunUpdateResponse(BareResponse):
    """Run Update Response"""

    run: Run


class RunCancelResponse(BareResponse):
    """Run Cancel Response"""

    run: Run


class RunSubmitToolOutputsResponse(BareResponse, Run):
    """Run Submit Tool Outputs Response"""
