"""thread.py"""

from typing import Dict, Literal, Optional

from pydantic import BaseModel, NonNegativeInt

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
