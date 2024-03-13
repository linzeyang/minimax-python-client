"""chat_completion.py"""

from typing import Optional

from pydantic import BaseModel


class ChoiceMessageToolCallFunction(BaseModel):
    """Chat Completion Choice Message ToolCall Function"""

    name: str
    arguments: str


class ChoiceMessageToolCall(BaseModel):
    """Chat Completion Choice Message ToolCall"""

    id: str
    type: str
    function: ChoiceMessageToolCallFunction


class ChoiceMessage(BaseModel):
    """Chat Completion Choice Message"""

    role: str
    content: Optional[str] = None
    tool_calls: Optional[list[ChoiceMessageToolCall]] = None


class Choice(BaseModel):
    """Chat Completion Choice"""

    index: int
    message: Optional[ChoiceMessage] = None
    delta: Optional[ChoiceMessage] = None
    finish_reason: Optional[str] = None


class Usage(BaseModel):
    """Chat Completion Response Usage"""

    total_tokens: int


class BaseResp(BaseModel):
    """Chat Completion Response Base Response"""

    status_code: int
    status_msg: str


class Response(BaseModel):
    """Chat Completion Response"""

    id: str
    choices: list[Choice]
    created: int
    model: str
    object: str
    usage: Optional[Usage] = None
    base_resp: Optional[BaseResp] = None
