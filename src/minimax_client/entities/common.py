"""common.py"""

from pydantic import BaseModel


class BaseResp(BaseModel):
    """Base Response"""

    status_code: int
    status_msg: str
