"""thread.py"""

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, HttpUrl, NonNegativeInt

from minimax_client.entities.assistant import AssistantTool
from minimax_client.entities.chat_completion import ChoiceMessageToolCall
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
    metadata: Optional[Dict[str, str]] = None
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


class RunRequiredActionSubmitToolOutputs(BaseModel):
    """Run Required Action Submit Tool Outputs"""

    tool_calls: List[ChoiceMessageToolCall]


class RunRequiredAction(BaseModel):
    """Run Required Action"""

    type: Literal["submit_tool_outputs", ""]
    submit_tool_outputs: Optional[RunRequiredActionSubmitToolOutputs] = None


class Run(BaseModel):
    """Run"""

    id: str
    object: Literal["thread.run"]
    created_at: NonNegativeInt
    assistant_id: str
    thread_id: str
    status: Literal[
        "queued",
        "started",
        "in_progress",
        "requires_action",
        "completed",
        "expired",
        "cancelled",
        "failed",
    ]
    started_at: NonNegativeInt
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
    metadata: Optional[Dict[str, str]] = None
    required_action: Optional[RunRequiredAction] = None


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

    run: Optional[Run] = None


class RunSubmitToolOutputsResponse(BareResponse, Run):
    """Run Submit Tool Outputs Response"""


class RunStepDetailMessageCreation(BaseModel):
    """Run Step Detail Message Creation"""

    message_id: str


class RunStepDetailToolCallCodeInterpreterOutput(BaseModel):
    """Run Step Detail Tool Call Code Interpreter Output"""

    type: str
    logs: Optional[str] = None


class RunStepDetailToolCallCodeInterpreter(BaseModel):
    """Run Step Detail Tool Call Code Interpreter"""

    input: str
    outputs: List[RunStepDetailToolCallCodeInterpreterOutput]


class RunStepDetailToolCallWebSearch(BaseModel):
    """Run Step Detail Tool Call Web Search"""

    query: str = ""
    outputs: str = ""
    name: str = ""
    arguments: str = ""


class RunStepDetailToolCallRetrieval(BaseModel):
    """Run Step Detail Tool Call Retrieval"""

    query: str
    outputs: str


class RunStepDetailToolCallFuntion(BaseModel):
    """Run Step Detail Tool Call Function"""

    name: str
    arguments: str
    output: str


class RunStepDetailToolCall(BaseModel):
    """Run Step Detail Tool Call"""

    id: str
    type: Literal["code_interpreter", "web_search", "retrieval", "function"]
    code_interpreter: Optional[RunStepDetailToolCallCodeInterpreter] = None
    web_search: Optional[RunStepDetailToolCallWebSearch] = None
    retrieval: Optional[RunStepDetailToolCallRetrieval] = None
    function: Optional[RunStepDetailToolCallFuntion] = None


class RunStepDetail(BaseModel):
    """Run Step Detail"""

    type: Literal["message_creation", "tool_calls"]
    message_creation: Optional[RunStepDetailMessageCreation] = None
    tool_calls: Optional[List[RunStepDetailToolCall]] = None


class RunStep(BaseModel):
    """Run Step"""

    id: str
    object: Literal["thread.run.step"]
    run_id: str
    assistant_id: str
    thread_id: str
    type: Literal["message_creation", "tool_calls"]
    status: str
    created_at: NonNegativeInt
    expired_at: Optional[NonNegativeInt] = None
    cancelled_at: Optional[NonNegativeInt] = None
    failed_at: Optional[NonNegativeInt] = None
    completed_at: Optional[NonNegativeInt] = None
    last_error: Optional[RunError] = None
    step_details: RunStepDetail
    base_resp: Dict


class RunStepRetrieveResponse(BareResponse, RunStep):
    """Run Step Retrieve response"""


class RunStepListResponse(BareResponse):
    """Run Step List response"""

    object: Literal["list"]
    data: List[RunStep]
