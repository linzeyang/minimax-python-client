"""file.py"""

from typing import List, Optional

from pydantic import BaseModel, NonNegativeInt

from minimax_client.entities.common import BareResponse


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

    file_id: NonNegativeInt
    bytes: NonNegativeInt
    created_at: int
    filename: str
    purpose: str
    download_url: Optional[str] = None


class FileCreateResponse(BareResponse):
    """File Create Response"""

    file: File


class FileListResponse(BareResponse):
    """File List Response"""

    files: List[File]


class FileRetriveResponse(BareResponse):
    """File Retrieve Response"""

    file: File


class FileRetrieveContentResponse(BareResponse):
    """File Retrieve Content Response"""

    content: bytes  # to be confirmed


class FileDeleteResponse(BareResponse):
    """File Delete Response"""

    file_id: NonNegativeInt
