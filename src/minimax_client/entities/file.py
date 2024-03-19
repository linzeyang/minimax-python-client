"""file.py"""

from typing import List, Optional

from pydantic import BaseModel

from minimax_client.entities.common import BaseResp


class File(BaseModel):
    """
    File entity

    purpose:
        retrieval -> pdf, docx, txt
        fine-tune -> jsonl
        voice_clone -> mp3, m4a, wav
        assistants -> refer to official documents
        role-recognition -> json, txt(with json content)
    """

    file_id: int
    bytes: int
    created_at: int
    filename: str
    purpose: str
    download_url: Optional[str] = None


class FileCreateResponse(BaseModel):
    """File Create Response"""

    file: File
    base_resp: BaseResp


class FileListResponse(BaseModel):
    """File List Response"""

    files: List[File]
    base_resp: BaseResp


class FileRetriveResponse(BaseModel):
    """File Retrieve Response"""

    file: File
    base_resp: BaseResp


class FileRetrieveContentResponse(BaseModel):
    """File Retrieve Content Response"""

    content: bytes  # to be confirmed
    base_resp: BaseResp


class FileDeleteResponse(BaseModel):
    """File Delete Response"""

    file_id: int
    base_resp: BaseResp
