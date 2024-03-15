"""embedding.py"""

from typing import List

from pydantic import BaseModel

from minimax_client.entities.common import BaseResp


class Response(BaseModel):
    """Embeddings Response"""

    vectors: List[List[float]]
    total_tokens: int
    base_resp: BaseResp
