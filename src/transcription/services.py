from typing import Union

from fastapi import UploadFile
from whisperx.types import SingleSegment

from src.transcription.enums import Language, Model, ResultFormat
from src.transcription.schemas import (
    Segment,
    TranscriptionSrtResult,
    TranscriptionTextResult,
)
from src.transcription.speech_transcription import SpeechTranscription
from src.transcription.utils import temporary_audio_file


class SpeechTranscriptionService:
    def __init__(self, transcriber: SpeechTranscription):
        self._transcriber = transcriber

    def transcribe(
        self,
        file: UploadFile,
        model: Model = Model.SMALL,
        language: Language | None = None,
        format_result: ResultFormat = ResultFormat.TEXT,
    ) -> Union[TranscriptionTextResult, TranscriptionSrtResult]:
        """
        Transcribes speech from an uploaded audio file and returns the result
        in the specified format.

        :param file: Uploaded audio file to be processed.
        :param model: Transcription model to use (e.g., Model.SMALL, Model.MEDIUM).
        :param language: Optional language enum value (e.g., Language.EN, Language.RU).
        :param format_result: Output format for the transcription result (e.g., ResultFormat.TEXT, ResultFormat.SRT).

        :return: A transcription result in the selected format (text or subtitle).
        """
        segments = self._transcribe(file, model, language)

        if format_result == ResultFormat.TEXT:
            text = self._to_text(segments)
            return TranscriptionTextResult(text=text)

        srt = self._to_srt(segments)
        return TranscriptionSrtResult(srt=srt)

    @staticmethod
    def _to_text(segments: list[SingleSegment]) -> str:
        """
        Converts transcription segments into plain text.

        :param segments: List of transcription segments.

        :return: Concatenated transcription text.
        """
        return " ".join(segment["text"].strip() for segment in segments).strip()

    @staticmethod
    def _to_srt(segments: list[SingleSegment]) -> list[Segment]:
        """
        Converts transcription segments into SRT-like structured segments.

        :param segments: List of transcription segments.

        :return: List of Segment objects suitable for SRT serialization.
        """
        return [
            Segment(
                number=index,
                text=segment["text"].strip(),
                start=segment["start"],
                end=segment["end"],
            )
            for index, segment in enumerate(segments, start=1)
        ]

    def _transcribe(
        self,
        file: UploadFile,
        model: Model = Model.SMALL,
        language: Language | None = None,
    ) -> list[SingleSegment]:
        """
        Transcribes from the uploaded audio file using the specified model and language.

        The file is temporarily saved to disk and passed to the underlying transcriber.

        :param file: Uploaded audio file to be processed.
        :param model: Transcription model to use (e.g., Model.SMALL, Model.MEDIUM).
        :param language: Optional language enum value (e.g., Language.EN, Language.RU).

        :return: List of transcribed segments containing transcribed text and timestamps.
        """

        with temporary_audio_file(file) as path:
            return self._transcriber.transcribe(
                audio_file=path, model=model, language=language
            )

    def clean(self):
        """
        Clean up resources held by the transcriber (e.g., cached models).
        Should be called on application shutdown.
        """

        self._transcriber.clean()
