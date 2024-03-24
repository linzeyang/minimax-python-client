"""embedding.py"""

from typing import List

from pydantic import BaseModel, NonNegativeInt

from minimax_client.entities.common import BaseResp


class EmbeddingResponse(BaseModel):
    """Embeddings Response"""

    vectors: List[List[float]]
    total_tokens: NonNegativeInt
    base_resp: BaseResp
