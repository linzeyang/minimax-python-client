"""fine_tuning.py"""

from typing import List, Literal, Optional

from pydantic import BaseModel, NonNegativeInt, PositiveFloat, PositiveInt

from minimax_client.entities.common import BaseResp


class HyperParameters(BaseModel):
    """Fine Tuning Hyper Parameters"""

    batch_size: PositiveInt
    learning_rate_multiplier: PositiveFloat
    n_epochs: PositiveInt


class FineTuningJob(BaseModel):
    """Fine Tuning Job"""

    id: str
    created_at: PositiveInt
    fine_tuned_model: Literal["abab5.5-chat-240119", "abab5.5s-chat-240123"]
    result_files: list[str]
    status: str
    training_file: NonNegativeInt
    validation_file: Optional[NonNegativeInt] = None
    tokens_count: NonNegativeInt
    hyperparameters: Optional[HyperParameters] = None


class FineTuningJobCreateResponse(BaseModel):
    """Fine Tuning Job Create Response"""

    finetune_job: FineTuningJob
    base_resp: BaseResp


class FineTuningJobListResponse(BaseModel):
    """Fine Tuning Job List Response"""

    finetune_jobs: List[FineTuningJob] = []  # to be confirmed
    has_more: bool
    base_resp: BaseResp


class FineTuningJobEvent(BaseModel):
    """Fine Tuning Job Event"""

    id: str
    created_at: PositiveInt
    level: str
    message: str
    object: str


class FineTuningJobEventListResponse(BaseModel):
    """Fine Tuning Job Event List Response"""

    event_list: List[FineTuningJobEvent] = []
    has_more: bool
    base_resp: BaseResp


class FineTuningModel(BaseModel):
    """Fine Tuning Model"""

    model_id: str
    created_at: PositiveInt
    object: str
    base_model: str


class FineTuningModelListResponse(BaseModel):
    """Fine Tuning Model List Response"""

    models: list[FineTuningModel] = []
    base_resp: BaseResp


class FineTuningModelRetrieveResponse(BaseModel):
    """Fine Tuning Model Retrieve Response"""

    model: FineTuningModel
    base_resp: BaseResp
