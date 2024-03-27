"""embedding.py"""

from typing import List

from pydantic import NonNegativeInt

from minimax_client.entities.common import BareResponse


class EmbeddingResponse(BareResponse):
    """Embeddings Response"""

    vectors: List[List[float]]
    total_tokens: NonNegativeInt
