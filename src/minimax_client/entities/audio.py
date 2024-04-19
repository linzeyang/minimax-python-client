"""audio.py"""

from typing import Literal, Optional

from pydantic import BaseModel, HttpUrl, NonNegativeFloat, NonNegativeInt

from minimax_client.entities.common import BareResponse


class AudioSpeechErrorResponse(BareResponse):
    """Audio Speech Response"""

    trace_id: str


class AudioSpeechExtraInfo(BaseModel):
    """Audio Speech Extra Info"""

    audio_length: NonNegativeInt
    audio_sample_rate: NonNegativeInt
    audio_size: NonNegativeInt
    bitrate: NonNegativeInt
    word_count: NonNegativeInt
    invisible_character_ratio: NonNegativeFloat
    usage_characters: NonNegativeInt


class AudioSpeechProResponse(BareResponse):
    """Audio Speech Pro Response"""

    trace_id: str
    audio_file: Optional[HttpUrl] = None
    subtitle_file: Optional[HttpUrl] = None
    extra_info: Optional[AudioSpeechExtraInfo] = None


class AudioSpeechLargeResponse(BareResponse):
    """Audio Speech Large Response"""

    task_id: int
    task_token: str
    file_id: int
    usage_characters: NonNegativeInt


class AudioSpeechLargeStatusResponse(BareResponse):
    """Audio Speech Large Status Response"""

    status: Literal["Processing", "Success", "Failed", "Expired", ""]


class AudioSpeechStreamChunk(BaseModel):
    """Audio Speech Stream Chunk"""

    audio: str  # HEX encoded
    status: Literal[1, 2]
    ced: str


class AudioSpeechStreamResponse(BareResponse):
    """Audio Speech Stream Response"""

    trace_id: str
    data: AudioSpeechStreamChunk
    extra_info: Optional[AudioSpeechExtraInfo] = None


class VoiceCloningResponse(BareResponse):
    """Voice Cloning Response"""

    input_sensitive: bool
    input_sensitive_type: int
