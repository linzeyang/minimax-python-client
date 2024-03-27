"""fine_tuning.py"""

from typing import List, Literal, Optional

from pydantic import BaseModel, NonNegativeInt, PositiveFloat, PositiveInt

from minimax_client.entities.common import BareResponse


class HyperParameters(BaseModel):
    """Fine Tuning Hyper Parameters"""

    batch_size: Optional[PositiveInt] = None
    learning_rate_multiplier: Optional[PositiveFloat] = None
    n_epochs: Optional[PositiveInt] = None


class FineTuningJob(BaseModel):
    """Fine Tuning Job"""

    id: str
    created_at: PositiveInt
    fine_tuned_model: str
    hyperparameters: Optional[HyperParameters] = None
    model: str
    object: Literal["finetune.job"]
    organization_id: str
    result_files: List[str]
    status: str
    training_file: NonNegativeInt
    validation_file: NonNegativeInt


class FineTuningJobCreateResponse(BareResponse):
    """Fine Tuning Job Create Response"""

    finetune_job: FineTuningJob


class FineTuningJobListResponse(BareResponse):
    """Fine Tuning Job List Response"""

    job_list: List[FineTuningJob] = []
    has_more: bool


class FineTuningJobEvent(BaseModel):
    """Fine Tuning Job Event"""

    id: str
    created_at: PositiveInt
    level: str
    message: str
    object: str


class FineTuningJobEventListResponse(BareResponse):
    """Fine Tuning Job Event List Response"""

    event_list: List[FineTuningJobEvent] = []
    has_more: bool


class FineTuningModel(BaseModel):
    """Fine Tuning Model"""

    id: str
    created_at: PositiveInt
    object: Literal["finetune.model"]
    base_model: Literal["abab5.5-chat-240119", "abab5.5s-chat-240123"]


class FineTuningModelListResponse(BareResponse):
    """Fine Tuning Model List Response"""

    model_list: List[FineTuningModel] = []


class FineTuningModelRetrieveResponse(BareResponse):
    """Fine Tuning Model Retrieve Response"""

    model: FineTuningModel
