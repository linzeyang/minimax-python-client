"""common.py"""

from pydantic import BaseModel, NonNegativeInt


class BaseResp(BaseModel):
    """Base Response

    status_code:
        1000: Unknown Error
        1001: Timeout
        1002: RPM limit reached
        1004: Authorization Failure
        1008: Balance Insufficient
        1013: Internal Service Error
        1026: Input incorrect
        1027: Output incorrect
        1039: TPM limit reached
        2013: Input format info incorrect
    """

    status_code: NonNegativeInt
    status_msg: str


class BareResponse(BaseModel):
    """Bare Response with only 'base_resp'"""

    base_resp: BaseResp
