"""fine_tuning.py"""

from typing import Dict, Literal, Optional, Union

import httpx

from minimax_client.entities.common import BareResponse
from minimax_client.entities.fine_tuning import (
    FineTuningJobCreateResponse,
    FineTuningJobEventListResponse,
    FineTuningJobListResponse,
    FineTuningModelListResponse,
    FineTuningModelRetrieveResponse,
)
from minimax_client.interfaces.base import BaseAsyncInterface, BaseSyncInterface


class FineTuningJob(BaseSyncInterface):
    """Synchronous Fine Tuning Jobs interface"""

    url_path = ""

    def create(
        self,
        *,
        model: Literal["abab5.5-chat-240119", "abab5.5s-chat-240123"],
        training_file: int,
        validation_file: Optional[int] = None,
        hyperparameters: Optional[Dict[str, Union[int, float]]] = None,
        suffix: Optional[str] = None,
    ) -> FineTuningJobCreateResponse:
        """
        Create a new fine tuning job

        Args:
            model (Literal["abab5.5-chat-240119", "abab5.5s-chat-240123"]):
                The model to fine tune
            training_file (int): The ID of the training file
            validation_file (Optional[int], optional): The ID of the validation file.
                Defaults to None.
            hyperparameters (Optional[Dict[str, Union[int, float]]], optional):
                The hyperparameters to fine tune. Defaults to None.
            suffix (Optional[str], optional): The suffix to use for the fine tuning job.
                Defaults to None.

        Returns:
            FineTuningJobCreateResponse: The created fine tuning job
        """
        json_body = {
            "model": model,
            "training_file": training_file,
        }

        if validation_file:
            json_body["validation_file"] = validation_file

        if hyperparameters:
            json_body["hyperparameters"] = hyperparameters

        if suffix:
            json_body["suffix"] = suffix

        resp = self.client.post(url="create_finetune_job", json=json_body)

        return FineTuningJobCreateResponse(**resp.json())

    def list(
        self, limit: int, after: Optional[str] = None
    ) -> FineTuningJobListResponse:
        """
        List all fine tuning jobs

        Args:
            limit (int): The number of fine tuning jobs to return
            after (Optional[str], optional):
                The ID of the fine tuning job to start after. Defaults to None.

        Returns:
            FineTuningJobListResponse: The list of fine tuning jobs
        """
        json_body: Dict[str, Union[int, str]] = {"limit": limit}

        if after:
            json_body["after"] = after

        resp = self.client.post(url="list_finetune_job", json=json_body)

        return FineTuningJobListResponse(**resp.json())

    def retrieve(self, fine_tuning_job_id: str) -> FineTuningJobCreateResponse:
        """
        Retrieve a fine tuning job

        Args:
            fine_tuning_job_id (str): The ID of the fine tuning job to retrieve

        Returns:
            FineTuningJobCreateResponse: The retrieved fine tuning job
        """
        json_body = {"fine_tuning_job_id": fine_tuning_job_id}

        resp = self.client.post(url="retrieve_finetune_job", json=json_body)

        return FineTuningJobCreateResponse(**resp.json())

    def cancel(self, fine_tuning_job_id: str) -> BareResponse:
        """
        Cancel a fine tuning job

        Args:
            fine_tuning_job_id (str): The ID of the fine tuning job to cancel

        Returns:
            BareResponse: The response from the API
        """
        json_body = {"fine_tuning_job_id": fine_tuning_job_id}

        resp = self.client.post(url="delete_finetune_job", json=json_body)

        return BareResponse(**resp.json())

    def list_events(
        self, fine_tuning_job_id: str, limit: int, after: Optional[str] = None
    ) -> FineTuningJobEventListResponse:
        """
        List events for a fine tuning job

        Args:
            fine_tuning_job_id (str): The ID of the fine tuning job
            limit (int): The number of events to return
            after (Optional[str], optional):
                The ID of the event to start after. Defaults to None.

        Returns:
            FineTuningJobEventListResponse: The list of events
        """
        json_body = {"fine_tuning_job_id": fine_tuning_job_id, "limit": limit}

        if after:
            json_body["after"] = after

        resp = self.client.post(url="list_finetune_event", json=json_body)

        return FineTuningJobEventListResponse(**resp.json())


class AsyncFineTuningJob(BaseAsyncInterface, FineTuningJob):
    """Asynchronous Fine Tuning Jobs interface"""

    async def create(
        self,
        *,
        model: Literal["abab5.5-chat-240119", "abab5.5s-chat-240123"],
        training_file: int,
        validation_file: Optional[int] = None,
        hyperparameters: Optional[Dict[str, Union[int, float]]] = None,
        suffix: Optional[str] = None,
    ) -> FineTuningJobCreateResponse:
        """
        Create a new fine tuning job

        Args:
            model (Literal["abab5.5-chat-240119", "abab5.5s-chat-240123"]):
                The model to fine tune
            training_file (int): The ID of the training file
            validation_file (Optional[int], optional): The ID of the validation file.
                Defaults to None.
            hyperparameters (Optional[Dict[str, Union[int, float]]], optional):
                The hyperparameters to fine tune. Defaults to None.
            suffix (Optional[str], optional): The suffix to use for the fine tuning job.
                Defaults to None.

        Returns:
            FineTuningJobCreateResponse: The created fine tuning job
        """
        json_body = {
            "model": model,
            "training_file": training_file,
        }

        if validation_file:
            json_body["validation_file"] = validation_file

        if hyperparameters:
            json_body["hyperparameters"] = hyperparameters

        if suffix:
            json_body["suffix"] = suffix

        resp = await self.client.post(url="create_finetune_job", json=json_body)

        return FineTuningJobCreateResponse(**resp.json())

    async def list(
        self, limit: int, after: Optional[str] = None
    ) -> FineTuningJobListResponse:
        """
        List all fine tuning jobs

        Args:
            limit (int): The number of fine tuning jobs to return
            after (Optional[str], optional):
                The ID of the fine tuning job to start after. Defaults to None.

        Returns:
            FineTuningJobListResponse: The list of fine tuning jobs
        """
        json_body: Dict[str, Union[int, str]] = {"limit": limit}

        if after:
            json_body["after"] = after

        resp = await self.client.post(url="list_finetune_job", json=json_body)

        return FineTuningJobListResponse(**resp.json())

    async def retrieve(self, fine_tuning_job_id: str) -> FineTuningJobCreateResponse:
        """
        Retrieve a fine tuning job

        Args:
            fine_tuning_job_id (str): The ID of the fine tuning job to retrieve

        Returns:
            FineTuningJobCreateResponse: The retrieved fine tuning job
        """
        json_body = {"fine_tuning_job_id": fine_tuning_job_id}

        resp = await self.client.post(url="retrieve_finetune_job", json=json_body)

        return FineTuningJobCreateResponse(**resp.json())

    async def cancel(self, fine_tuning_job_id: str) -> BareResponse:
        """
        Cancel a fine tuning job

        Args:
            fine_tuning_job_id (str): The ID of the fine tuning job to cancel

        Returns:
            BareResponse: The response from the API
        """
        json_body = {"fine_tuning_job_id": fine_tuning_job_id}

        resp = await self.client.post(url="delete_finetune_job", json=json_body)

        return BareResponse(**resp.json())

    async def list_events(
        self, fine_tuning_job_id: str, limit: int, after: Optional[str] = None
    ) -> FineTuningJobEventListResponse:
        """
        List events for a fine tuning job

        Args:
            fine_tuning_job_id (str): The ID of the fine tuning job
            limit (int): The number of events to return
            after (Optional[str], optional):
                The ID of the event to start after. Defaults to None.

        Returns:
            FineTuningJobEventListResponse: The list of events
        """
        json_body = {"fine_tuning_job_id": fine_tuning_job_id, "limit": limit}

        if after:
            json_body["after"] = after

        resp = await self.client.post(url="list_finetune_event", json=json_body)

        return FineTuningJobEventListResponse(**resp.json())


class FineTuning:
    """Synchronous Fine Tuning interface"""

    jobs: FineTuningJob

    def __init__(self, http_client: httpx.Client) -> None:
        self.jobs = FineTuningJob(http_client=http_client)


class AsyncFineTuning:
    """Asynchronous Fine Tuning interface"""

    jobs: AsyncFineTuningJob

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self.jobs = AsyncFineTuningJob(http_client=http_client)


class Model(BaseSyncInterface):
    """Synchronous Model interface"""

    url_path = ""

    def list(self) -> FineTuningModelListResponse:
        """
        List all fine tuning models

        Returns:
            FineTuningModelListResponse: The list of fine tuning models
        """
        resp = self.client.post(url="list_finetune_model")

        return FineTuningModelListResponse(**resp.json())

    def retrieve(self, model: str) -> FineTuningModelRetrieveResponse:
        """
        Retrieve a fine tuning model

        Args:
            model (str): The ID of the fine tuning model to retrieve

        Returns:
            FineTuningModelRetrieveResponse: The retrieved fine tuning model
        """
        json_body = {"model_id": model}

        resp = self.client.post(url="retrieve_finetune_model", json=json_body)

        return FineTuningModelRetrieveResponse(**resp.json())

    def delete(self, model: str) -> BareResponse:
        """
        Delete a fine tuning model

        Args:
            model (str): The ID of the fine tuning model to delete

        Returns:
            BareResponse: The response from the API
        """
        json_body = {"model_id": model}

        resp = self.client.post(url="delete_finetune_model", json=json_body)

        return BareResponse(**resp.json())


class AsyncModel(BaseAsyncInterface, Model):
    """Asynchronous Model interface"""

    async def list(self) -> FineTuningModelListResponse:
        """
        List all fine tuning models

        Returns:
            FineTuningModelListResponse: The list of fine tuning models
        """
        resp = await self.client.post(url="list_finetune_model")

        return FineTuningModelListResponse(**resp.json())

    async def retrieve(self, model: str) -> FineTuningModelRetrieveResponse:
        """
        Retrieve a fine tuning model

        Args:
            model (str): The ID of the fine tuning model to retrieve

        Returns:
            FineTuningModelRetrieveResponse: The retrieved fine tuning model
        """
        json_body = {"model_id": model}

        resp = await self.client.post(url="retrieve_finetune_model", json=json_body)

        return FineTuningModelRetrieveResponse(**resp.json())

    async def delete(self, model: str) -> BareResponse:
        """
        Delete a fine tuning model

        Args:
            model (str): The ID of the fine tuning model to delete

        Returns:
            BareResponse: The response from the API
        """
        json_body = {"model_id": model}

        resp = await self.client.post(url="delete_finetune_model", json=json_body)

        return BareResponse(**resp.json())
