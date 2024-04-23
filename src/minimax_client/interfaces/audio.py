"""audio.py"""

import json
from pathlib import Path
from typing import AsyncGenerator, Dict, Generator, List, Literal, Optional, Union

from minimax_client.entities.audio import (
    AudioSpeechErrorResponse,
    AudioSpeechLargeResponse,
    AudioSpeechLargeStatusResponse,
    AudioSpeechProResponse,
    AudioSpeechStreamResponse,
    VoiceCloningResponse,
)
from minimax_client.interfaces.base import BaseAsyncInterface, BaseSyncInterface


class Audio(BaseSyncInterface):
    """Synchronous Audio (T2A) interface"""

    url_path = ""

    def speech(
        self,
        *,
        text: str,
        model: Literal["speech-01", "speech-02"],
        voice_id: Optional[str] = None,
        timber_weights: Optional[List[Dict[str, Union[str, int]]]] = None,
        speed: float = 1.0,
        vol: float = 1.0,
        output_format: Literal["mp3", "wav", "pcm", "flac", "aac"] = "mp3",
        pitch: int = 0,
        char_to_pitch: Optional[List[str]] = None,
    ) -> Union[AudioSpeechErrorResponse, bytes]:
        """
        Text to Speech. Maximum characters to synthesize: 500

        Args:
            text (str): The text to synthesize. Should be < 500 characters.
            model (Literal["speech-01", "speech-02"]):
                The model to use.
                "speech-01" is suited in Chinese cases;
                "speech-02" supports Chinese, English, CN/EN mix, Japanese and Korean.
            voice_id (Optional[str], optional):
                The ID of the voice to use. eg. "male-qn-qingse", "female-shaonv"
                Could be one of preset IDs from MiniMax, or one out of voice cloning.
            timber_weights (Optional[List[Dict[str, Union[str, int]]]], optional):
                Weights info of mixture of voices.
                If `timber_weights` is specified, `voice_id` will be ignored.
                Defaults to None.
            speed (float):
                The speed of the synthesized voice. Should be in range [0.5, 2].
                Defaults to 1.0.
            vol (float):
                The volume of the synthesized voice. Should be in range (0, 10].
                Defaults to 1.0.
            output_format (Literal["mp3", "wav", "pcm", "flac", "aac"]):
                The output format of the synthesized voice. Defaults to "mp3".
            pitch (int):
                The pitch of the synthesized voice. Should be in range [-12, 12].
                Defaults to 0 (which means the original pitch).
            char_to_pitch (Optional[List[str]], optional):
                List of rules to replace tones/symbols. One string per rule.
                eg. "燕少飞/(yan4)(shao3)(fei1)", "omg/oh my god", "=/等于"
                Defaults to None.

        Returns:
            Union[AudioSpeechErrorResponse, bytes]: The response from the API
        """
        json_body = {
            "text": text,
            "model": model,
            "speed": speed,
            "vol": vol,
            "output_format": output_format,
            "pitch": pitch,
        }

        if timber_weights:
            json_body["timber_weights"] = timber_weights
        elif voice_id:
            json_body["voice_id"] = voice_id

        if char_to_pitch:
            json_body["char_to_pitch"] = char_to_pitch

        resp = self.client.post(url="text_to_speech", json=json_body)

        if resp.headers["Content-Type"] != "audio/mpeg":
            return AudioSpeechErrorResponse(**resp.json())

        return resp.content

    def speech_pro(
        self,
        *,
        text: str,
        model: Literal["speech-01", "speech-02"],
        voice_id: Optional[str] = None,
        timber_weights: Optional[List[Dict[str, Union[str, int]]]] = None,
        speed: float = 1.0,
        vol: float = 1.0,
        output_format: Literal["mp3", "wav", "pcm", "flac", "aac"] = "mp3",
        pitch: int = 0,
        audio_sample_rate: Literal[16_000, 24_000, 32_000] = 32_000,
        bitrate: Literal[32_000, 64_000, 128_000] = 128_000,
        char_to_pitch: Optional[List[str]] = None,
    ) -> AudioSpeechProResponse:
        """
        Text to Speech Pro. Maximum characters to synthesize: 50,000

        Args:
            text (str): The text to synthesize. Should be < 50,000 characters.
            model (Literal["speech-01", "speech-02"]):
                The model to use.
                "speech-01" is suited in Chinese cases;
                "speech-02" supports Chinese, English, CN/EN mix, Japanese and Korean.
            voice_id (Optional[str], optional):
                The ID of the voice to use. eg. "male-qn-qingse", "female-shaonv"
                Could be one of preset IDs from MiniMax, or one out of voice cloning.
            timber_weights (Optional[List[Dict[str, Union[str, int]]]], optional):
                Weights info of mixture of voices.
                If `timber_weights` is specified, `voice_id` will be ignored.
                Defaults to None.
            speed (float):
                The speed of the synthesized voice. Should be in range [0.5, 2].
                Defaults to 1.0.
            vol (float):
                The volume of the synthesized voice. Should be in range (0, 10].
                Defaults to 1.0.
            output_format (Literal["mp3", "wav", "pcm", "flac", "aac"]):
                The output format of the synthesized voice. Defaults to "mp3".
            pitch (int):
                The pitch of the synthesized voice. Should be in range [-12, 12].
                Defaults to 0 (which means the original pitch).
            audio_sample_rate (Literal[16_000, 24_000, 32_000]):
                The sample rate of the synthesized voice. Defaults to 32,000.
            bitrate (Literal[32_000, 64_000, 128_000]):
                The bitrate of the synthesized voice. Defaults to 128,000.
            char_to_pitch (Optional[List[str]], optional):
                List of rules to replace tones/symbols. One string per rule.
                eg. "燕少飞/(yan4)(shao3)(fei1)", "omg/oh my god", "=/等于"
                Defaults to None.

        Returns:
            AudoSpeechProResponse: The response from the API
        """
        json_body = {
            "text": text,
            "model": model,
            "speed": speed,
            "vol": vol,
            "output_format": output_format,
            "pitch": pitch,
            "audio_sample_rate": audio_sample_rate,
            "bitrate": bitrate,
        }

        if timber_weights:
            json_body["timber_weights"] = timber_weights
        elif voice_id:
            json_body["voice_id"] = voice_id

        if char_to_pitch:
            json_body["char_to_pitch"] = char_to_pitch

        resp = self.client.post(url="t2a_pro", json=json_body)

        return AudioSpeechProResponse(**resp.json())

    def speech_large(
        self,
        *,
        file_path: Union[str, Path],
        model: Literal["speech-01"],
        voice_id: str,
        speed: float = 1.0,
        vol: float = 1.0,
        output_format: Literal["mp3", "wav", "pcm", "flac", "aac"] = "mp3",
        pitch: int = 0,
        audio_sample_rate: Literal[16_000, 24_000] = 24_000,
        bitrate: Literal[32_900, 64_900, 128_900] = 64_900,
        char_to_pitch: Optional[List[str]] = None,
    ) -> AudioSpeechLargeResponse:
        """
        Text to Speech Large. Maximum characters to synthesize: 10,000,000
        Asynchronous request

        Args:
            file_path (Union[str, Path]):
                The path to a single (local) zip file containing the text to synthesize.
                The zip file should only contain txt or json files.
                The text inside should be < 10,000,000 characters.
            model (Literal["speech-01"]):
                The model to use. Only `speech-01` is supported.
            voice_id (Optional[str], optional):
                The ID of the voice to use. eg. "male-qn-qingse", "female-shaonv"
                Could be one of preset IDs from MiniMax, or one out of voice cloning.
            speed (float):
                The speed of the synthesized voice. Should be in range [0.5, 2].
                Defaults to 1.0.
            vol (float):
                The volume of the synthesized voice. Should be in range (0, 10].
                Defaults to 1.0.
            output_format (Literal["mp3", "wav", "pcm", "flac", "aac"]):
                The output format of the synthesized voice. Defaults to "mp3".
            pitch (int):
                The pitch of the synthesized voice. Should be in range [-12, 12].
                Defaults to 0 (which means the original pitch).
            audio_sample_rate (Literal[16_000, 24_000]):
                The sample rate of the synthesized voice. Defaults to 24,000.
            bitrate (Literal[32_900, 64_900, 128_900]):
                The bitrate of the synthesized voice. Defaults to 64,900.
            char_to_pitch (Optional[List[str]], optional):
                List of rules to replace tones/symbols. One string per rule.
                eg. "燕少飞/(yan4)(shao3)(fei1)", "omg/oh my god", "=/等于"
                Defaults to None.

        Returns:
            AudioSpeechLargeResponse: The response from the API
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)

        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"{file_path} does not exist or is not a file")

        body = {
            "model": model,
            "voice_id": voice_id,
            "speed": speed,
            "vol": vol,
            "output_format": output_format,
            "pitch": pitch,
            "audio_sample_rate": audio_sample_rate,
            "bitrate": bitrate,
        }

        if char_to_pitch:
            body["char_to_pitch"] = char_to_pitch

        with file_path.open("rb") as file:
            resp = self.client.post(url="t2a_async", data=body, files={"text": file})

        return AudioSpeechLargeResponse(**resp.json())

    def speech_large_status(self, task_id: int) -> AudioSpeechLargeStatusResponse:
        """
        Retrieve the status of a Text to Speech Large request.

        Args:
            task_id (int): The task_id from the response which creates the request.

        Returns:
            AudioSpeechLargeStatusResponse: The response from the API
        """
        resp = self.client.get(
            url="https://api.minimax.chat/query/t2a_async_query",
            params={"task_id": task_id},
        )

        return AudioSpeechLargeStatusResponse(**resp.json())

    def speech_stream(
        self,
        *,
        text: str,
        model: Literal["speech-01"],
        voice_id: Optional[str] = None,
        timber_weights: Optional[List[Dict[str, Union[str, int]]]] = None,
        speed: float = 1.0,
        vol: float = 1.0,
        format: Literal["mp3", "pcm", "flac"] = "mp3",
        pitch: int = 0,
        audio_sample_rate: Literal[16_000, 24_000, 32_000] = 32_000,
        bitrate: Literal[32_000, 64_000, 128_000] = 128_000,
        char_to_pitch: Optional[List[str]] = None,
    ) -> Generator[AudioSpeechStreamResponse, None, None]:
        """
        Text to Speech Stream. Maximum characters to synthesize: 500

        Args:
            text (str): The text to synthesize.
            model (Literal["speech-01"]):
                The model to use. Only `speech-01` is supported.
            voice_id (Optional[str], optional):
                The ID of the voice to use. eg. "male-qn-qingse", "female-shaonv"
                Could be one of preset IDs from MiniMax, or one out of voice cloning.
            timber_weights (Optional[List[Dict[str, Union[str, int]]]], optional):
                Weights info of mixture of voices.
                If `timber_weights` is specified, `voice_id` will be ignored.
                Defaults to None.
            speed (float):
                The speed of the synthesized voice. Should be in range [0.5, 2].
                Defaults to 1.0.
            vol (float):
                The volume of the synthesized voice. Should be in range (0, 10].
                Defaults to 1.0.
            format (Literal["mp3", "pcm", "flac"]):
                The output format of the synthesized voice. Defaults to "mp3".
            pitch (int):
                The pitch of the synthesized voice. Should be in range [-12, 12].
                Defaults to 0 (which means the original pitch).
            audio_sample_rate (Literal[16_000, 24_000, 32_000]):
                The sample rate of the synthesized voice. Defaults to 32,000.
            bitrate (Literal[32_000, 64_000, 128_000]):
                The bitrate of the synthesized voice. Defaults to 128,000.
            char_to_pitch (Optional[List[str]], optional):
                List of rules to replace tones/symbols. One string per rule.
                eg. "燕少飞/(yan4)(shao3)(fei1)", "omg/oh my god", "=/等于"
                Defaults to None.

        Returns:
            Generator[AudioSpeechStreamResponse, None, None]: The response from the API
        """
        json_body = {
            "text": text,
            "model": model,
            "speed": speed,
            "vol": vol,
            "format": format,
            "pitch": pitch,
            "audio_sample_rate": audio_sample_rate,
            "bitrate": bitrate,
        }

        if timber_weights:
            json_body["timber_weights"] = timber_weights
            json_body["voice_id"] = ""
        elif voice_id:
            json_body["voice_id"] = voice_id

        if char_to_pitch:
            json_body["char_to_pitch"] = char_to_pitch

        with self.client.stream(
            method="POST", url="tts/stream", json=json_body
        ) as resp:
            partial_text = ""

            for data_text in resp.iter_text():
                if not data_text.startswith("data: "):
                    partial_text += data_text
                else:
                    partial_text = data_text

                if "trace_id" in partial_text:
                    data_json = json.loads(partial_text.strip().split("data: ", 2)[1])
                    yield AudioSpeechStreamResponse(**data_json)

    def voice_cloning(self, file_id: int, voice_id: str) -> VoiceCloningResponse:
        """
        Voice Cloning.
        Must have an audio file uploaded in advance and acquire the id of that file.

        Args:
            file_id (int):
                The ID of the already uploaded audio file to clone against.
                The audio file should be in mp3, m4a or wav format.
                The size of the audio file should not exceed 20 MB.
                Length of audio should be within 5 minutes and longer than 10 seconds.
            voice_id (str):
                Custom ID to identify the cloned voice.
                Must be unique (ie. not the same as any existing voice_id).
                Must be at least 8 characters long.
                Must contain both letters and numbers, and start with a letter.
                Eg. "MiniMax001".

        Returns:
            VoiceCloningResponse: The response from the API
        """
        json_body = {"file_id": file_id, "voice_id": voice_id}

        resp = self.client.post(url="voice_clone", json=json_body)

        return VoiceCloningResponse(**resp.json())


class AsyncAudio(BaseAsyncInterface, Audio):
    """Asynchronous Audio (T2A) interface"""

    async def speech(
        self,
        *,
        text: str,
        model: Literal["speech-01", "speech-02"],
        voice_id: Optional[str] = None,
        timber_weights: Optional[List[Dict[str, Union[str, int]]]] = None,
        speed: float = 1.0,
        vol: float = 1.0,
        output_format: Literal["mp3", "wav", "pcm", "flac", "aac"] = "mp3",
        pitch: int = 0,
        char_to_pitch: Optional[List[str]] = None,
    ) -> Union[AudioSpeechErrorResponse, bytes]:
        """
        Text to Speech. Maximum characters to synthesize: 500

        Args:
            text (str): The text to synthesize. Should be < 500 characters.
            model (Literal["speech-01", "speech-02"]):
                The model to use.
                "speech-01" is suited in Chinese cases;
                "speech-02" supports Chinese, English, CN/EN mix, Japanese and Korean.
            voice_id (Optional[str], optional):
                The ID of the voice to use. eg. "male-qn-qingse", "female-shaonv"
                Could be one of preset IDs from MiniMax, or one out of voice cloning.
            timber_weights (Optional[List[Dict[str, Union[str, int]]]], optional):
                Weights info of mixture of voices.
                If `timber_weights` is specified, `voice_id` will be ignored.
                Defaults to None.
            speed (float):
                The speed of the synthesized voice. Should be in range [0.5, 2].
                Defaults to 1.0.
            vol (float):
                The volume of the synthesized voice. Should be in range (0, 10].
                Defaults to 1.0.
            output_format (Literal["mp3", "wav", "pcm", "flac", "aac"]):
                The output format of the synthesized voice. Defaults to "mp3".
            pitch (int):
                The pitch of the synthesized voice. Should be in range [-12, 12].
                Defaults to 0 (which means the original pitch).
            char_to_pitch (Optional[List[str]], optional):
                List of rules to replace tones/symbols. One string per rule.
                eg. "燕少飞/(yan4)(shao3)(fei1)", "omg/oh my god", "=/等于"
                Defaults to None.

        Returns:
            Union[AudioSpeechErrorResponse, bytes]: The response from the API
        """
        json_body = {
            "text": text,
            "model": model,
            "speed": speed,
            "vol": vol,
            "output_format": output_format,
            "pitch": pitch,
        }

        if timber_weights:
            json_body["timber_weights"] = timber_weights
        elif voice_id:
            json_body["voice_id"] = voice_id

        if char_to_pitch:
            json_body["char_to_pitch"] = char_to_pitch

        resp = await self.client.post(url="text_to_speech", json=json_body)

        if resp.headers["Content-Type"] != "audio/mpeg":
            return AudioSpeechErrorResponse(**resp.json())

        return resp.content

    async def speech_pro(
        self,
        *,
        text: str,
        model: Literal["speech-01", "speech-02"],
        voice_id: Optional[str] = None,
        timber_weights: Optional[List[Dict[str, Union[str, int]]]] = None,
        speed: float = 1.0,
        vol: float = 1.0,
        output_format: Literal["mp3", "wav", "pcm", "flac", "aac"] = "mp3",
        pitch: int = 0,
        audio_sample_rate: Literal[16_000, 24_000, 32_000] = 32_000,
        bitrate: Literal[32_000, 64_000, 128_000] = 128_000,
        char_to_pitch: Optional[List[str]] = None,
    ) -> AudioSpeechProResponse:
        """
        Text to Speech Pro. Maximum characters to synthesize: 50,000

        Args:
            text (str): The text to synthesize. Should be < 50,000 characters.
            model (Literal["speech-01", "speech-02"]):
                The model to use.
                "speech-01" is suited in Chinese cases;
                "speech-02" supports Chinese, English, CN/EN mix, Japanese and Korean.
            voice_id (Optional[str], optional):
                The ID of the voice to use. eg. "male-qn-qingse", "female-shaonv"
                Could be one of preset IDs from MiniMax, or one out of voice cloning.
            timber_weights (Optional[List[Dict[str, Union[str, int]]]], optional):
                Weights info of mixture of voices.
                If `timber_weights` is specified, `voice_id` will be ignored.
                Defaults to None.
            speed (float):
                The speed of the synthesized voice. Should be in range [0.5, 2].
                Defaults to 1.0.
            vol (float):
                The volume of the synthesized voice. Should be in range (0, 10].
                Defaults to 1.0.
            output_format (Literal["mp3", "wav", "pcm", "flac", "aac"]):
                The output format of the synthesized voice. Defaults to "mp3".
            pitch (int):
                The pitch of the synthesized voice. Should be in range [-12, 12].
                Defaults to 0 (which means the original pitch).
            audio_sample_rate (Literal[16_000, 24_000, 32_000]):
                The sample rate of the synthesized voice. Defaults to 32,000.
            bitrate (Literal[32_000, 64_000, 128_000]):
                The bitrate of the synthesized voice. Defaults to 128,000.
            char_to_pitch (Optional[List[str]], optional):
                List of rules to replace tones/symbols. One string per rule.
                eg. "燕少飞/(yan4)(shao3)(fei1)", "omg/oh my god", "=/等于"
                Defaults to None.

        Returns:
            AudoSpeechProResponse: The response from the API
        """
        json_body = {
            "text": text,
            "model": model,
            "speed": speed,
            "vol": vol,
            "output_format": output_format,
            "pitch": pitch,
            "audio_sample_rate": audio_sample_rate,
            "bitrate": bitrate,
        }

        if timber_weights:
            json_body["timber_weights"] = timber_weights
        elif voice_id:
            json_body["voice_id"] = voice_id

        if char_to_pitch:
            json_body["char_to_pitch"] = char_to_pitch

        resp = await self.client.post(url="t2a_pro", json=json_body)

        return AudioSpeechProResponse(**resp.json())

    async def speech_large(
        self,
        *,
        file_path: Union[str, Path],
        model: Literal["speech-01"],
        voice_id: str,
        speed: float = 1.0,
        vol: float = 1.0,
        output_format: Literal["mp3", "wav", "pcm", "flac", "aac"] = "mp3",
        pitch: int = 0,
        audio_sample_rate: Literal[16_000, 24_000] = 24_000,
        bitrate: Literal[32_900, 64_900, 128_900] = 64_900,
        char_to_pitch: Optional[List[str]] = None,
    ) -> AudioSpeechLargeResponse:
        """
        Text to Speech Large. Maximum characters to synthesize: 10,000,000
        Asynchronous request

        Args:
            file_path (Union[str, Path]):
                The path to a single (local) zip file containing the text to synthesize.
                The zip file should only contain txt or json files.
                The text inside should be < 10,000,000 characters.
            model (Literal["speech-01"]):
                The model to use. Only `speech-01` is supported.
            voice_id (Optional[str], optional):
                The ID of the voice to use. eg. "male-qn-qingse", "female-shaonv"
                Could be one of preset IDs from MiniMax, or one out of voice cloning.
            speed (float):
                The speed of the synthesized voice. Should be in range [0.5, 2].
                Defaults to 1.0.
            vol (float):
                The volume of the synthesized voice. Should be in range (0, 10].
                Defaults to 1.0.
            output_format (Literal["mp3", "wav", "pcm", "flac", "aac"]):
                The output format of the synthesized voice. Defaults to "mp3".
            pitch (int):
                The pitch of the synthesized voice. Should be in range [-12, 12].
                Defaults to 0 (which means the original pitch).
            audio_sample_rate (Literal[16_000, 24_000]):
                The sample rate of the synthesized voice. Defaults to 24,000.
            bitrate (Literal[32_900, 64_900, 128_900]):
                The bitrate of the synthesized voice. Defaults to 64,900.
            char_to_pitch (Optional[List[str]], optional):
                List of rules to replace tones/symbols. One string per rule.
                eg. "燕少飞/(yan4)(shao3)(fei1)", "omg/oh my god", "=/等于"
                Defaults to None.

        Returns:
            AudioSpeechLargeResponse: The response from the API
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)

        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"{file_path} does not exist or is not a file")

        body = {
            "model": model,
            "voice_id": voice_id,
            "speed": speed,
            "vol": vol,
            "output_format": output_format,
            "pitch": pitch,
            "audio_sample_rate": audio_sample_rate,
            "bitrate": bitrate,
        }

        if char_to_pitch:
            body["char_to_pitch"] = char_to_pitch

        with file_path.open("rb") as file:
            resp = await self.client.post(
                url="t2a_async", data=body, files={"text": file}
            )

        return AudioSpeechLargeResponse(**resp.json())

    async def speech_large_status(self, task_id: int) -> AudioSpeechLargeStatusResponse:
        """
        Retrieve the status of a Text to Speech Large request.

        Args:
            task_id (int): The task_id from the response which creates the request.

        Returns:
            AudioSpeechLargeStatusResponse: The response from the API
        """
        resp = await self.client.get(
            url="https://api.minimax.chat/query/t2a_async_query",
            params={"task_id": task_id},
        )

        return AudioSpeechLargeStatusResponse(**resp.json())

    async def speech_stream(
        self,
        *,
        text: str,
        model: Literal["speech-01"],
        voice_id: Optional[str] = None,
        timber_weights: Optional[List[Dict[str, Union[str, int]]]] = None,
        speed: float = 1.0,
        vol: float = 1.0,
        format: Literal["mp3", "pcm", "flac"] = "mp3",
        pitch: int = 0,
        audio_sample_rate: Literal[16_000, 24_000, 32_000] = 32_000,
        bitrate: Literal[32_000, 64_000, 128_000] = 128_000,
        char_to_pitch: Optional[List[str]] = None,
    ) -> AsyncGenerator[AudioSpeechStreamResponse, None]:
        """
        Text to Speech Stream. Maximum characters to synthesize: 500

        Args:
            text (str): The text to synthesize.
            model (Literal["speech-01"]):
                The model to use. Only `speech-01` is supported.
            voice_id (Optional[str], optional):
                The ID of the voice to use. eg. "male-qn-qingse", "female-shaonv"
                Could be one of preset IDs from MiniMax, or one out of voice cloning.
            timber_weights (Optional[List[Dict[str, Union[str, int]]]], optional):
                Weights info of mixture of voices.
                If `timber_weights` is specified, `voice_id` will be ignored.
                Defaults to None.
            speed (float):
                The speed of the synthesized voice. Should be in range [0.5, 2].
                Defaults to 1.0.
            vol (float):
                The volume of the synthesized voice. Should be in range (0, 10].
                Defaults to 1.0.
            format (Literal["mp3", "pcm", "flac"]):
                The output format of the synthesized voice. Defaults to "mp3".
            pitch (int):
                The pitch of the synthesized voice. Should be in range [-12, 12].
                Defaults to 0 (which means the original pitch).
            audio_sample_rate (Literal[16_000, 24_000, 32_000]):
                The sample rate of the synthesized voice. Defaults to 32,000.
            bitrate (Literal[32_000, 64_000, 128_000]):
                The bitrate of the synthesized voice. Defaults to 128,000.
            char_to_pitch (Optional[List[str]], optional):
                List of rules to replace tones/symbols. One string per rule.
                eg. "燕少飞/(yan4)(shao3)(fei1)", "omg/oh my god", "=/等于"
                Defaults to None.

        Returns:
            AsyncGenerator[AudioSpeechStreamResponse, None]: The response from the API
        """
        json_body = {
            "text": text,
            "model": model,
            "speed": speed,
            "vol": vol,
            "format": format,
            "pitch": pitch,
            "audio_sample_rate": audio_sample_rate,
            "bitrate": bitrate,
        }

        if timber_weights:
            json_body["timber_weights"] = timber_weights
            json_body["voice_id"] = ""
        elif voice_id:
            json_body["voice_id"] = voice_id

        if char_to_pitch:
            json_body["char_to_pitch"] = char_to_pitch

        async with self.client.stream(
            method="POST", url="tts/stream", json=json_body
        ) as resp:
            partial_text = ""

            async for data_text in resp.aiter_text():
                if not data_text.startswith("data: "):
                    partial_text += data_text
                else:
                    partial_text = data_text

                if "trace_id" in partial_text:
                    data_json = json.loads(partial_text.strip().split("data: ", 2)[1])
                    yield AudioSpeechStreamResponse(**data_json)

    async def voice_cloning(self, file_id: int, voice_id: str) -> VoiceCloningResponse:
        """
        Voice Cloning.
        Must have an audio file uploaded in advance and acquire the id of that file.

        Args:
            file_id (int):
                The ID of the already uploaded audio file to clone against.
                The audio file should be in mp3, m4a or wav format.
                The size of the audio file should not exceed 20 MB.
                Length of audio should be within 5 minutes and longer than 10 seconds.
            voice_id (str):
                Custom ID to identify the cloned voice.
                Must be unique (ie. not the same as any existing voice_id).
                Must be at least 8 characters long.
                Must contain both letters and numbers, and start with a letter.
                Eg. "MiniMax001".

        Returns:
            VoiceCloningResponse: The response from the API
        """
        json_body = {"file_id": file_id, "voice_id": voice_id}

        resp = await self.client.post(url="voice_clone", json=json_body)

        return VoiceCloningResponse(**resp.json())
