"""chat_completion.py"""

from typing import List, Literal, Optional

from pydantic import BaseModel, NonNegativeInt

from minimax_client.entities.common import BareResponse


class ChoiceMessageToolCallFunction(BaseModel):
    """Chat Completion Choice Message ToolCall Function"""

    name: str
    arguments: str


class ChoiceMessageToolCall(BaseModel):
    """Chat Completion Choice Message ToolCall"""

    id: str
    type: Literal["function"]
    function: ChoiceMessageToolCallFunction


class ChoiceMessage(BaseModel):
    """Chat Completion Choice Message"""

    role: Literal["assistant", "user", "system", "tool"]
    content: Optional[str] = None
    tool_calls: Optional[List[ChoiceMessageToolCall]] = None


class Choice(BaseModel):
    """Chat Completion Choice"""

    index: NonNegativeInt
    message: Optional[ChoiceMessage] = None
    delta: Optional[ChoiceMessage] = None
    finish_reason: Optional[Literal["length", "stop", "tool_calls"]] = None


class Usage(BaseModel):
    """Chat Completion Response Usage"""

    total_tokens: NonNegativeInt


class ChatCompletionResponse(BareResponse):
    """Chat Completion Response"""

    id: str
    choices: List[Choice]
    created: int
    model: Literal["abab5.5s-chat", "abab5.5-chat", "abab6-chat"]
    object: Literal["chat.completion", "chat.completion.chunk"]
    usage: Optional[Usage] = None
