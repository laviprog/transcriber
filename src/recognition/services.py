from typing import Union

from fastapi import UploadFile
from whisperx.types import SingleSegment

from src.recognition.enums import Language, Model, ResultFormat
from src.recognition.recognizer import Recognizer
from src.recognition.schemas import (
    RecognitionSrtResult,
    RecognitionTextResult,
    Segment,
)
from src.recognition.utils import temporary_audio_file


class RecognitionService:
    def __init__(self, recognizer: Recognizer):
        self._recognizer = recognizer

    def recognize(
        self,
        file: UploadFile,
        model: Model = Model.SMALL,
        language: Language | None = None,
        format_result: ResultFormat = ResultFormat.TEXT,
    ) -> Union[RecognitionTextResult, RecognitionSrtResult]:
        """
        Recognizes speech from an uploaded audio file and returns the result
        in the specified format.

        :param file: Uploaded audio file to be processed.
        :param model: Recognition model to use (e.g., Model.SMALL, Model.MEDIUM).
        :param language: Optional language enum value (e.g., Language.EN, Language.RU).
        :param format_result: Output format for the recognition result (e.g., ResultFormat.TEXT, ResultFormat.SRT).

        :return: A recognition result in the selected format (text or subtitle).
        """
        segments = self._recognize(file, model, language)

        if format_result == ResultFormat.TEXT:
            text = self._to_text(segments)
            return RecognitionTextResult(text=text)

        srt = self._to_srt(segments)
        return RecognitionSrtResult(srt=srt)

    @staticmethod
    def _to_text(segments: list[SingleSegment]) -> str:
        """
        Converts recognition segments into plain text.

        :param segments: List of recognition segments.

        :return: Concatenated transcription text.
        """
        return " ".join(segment["text"].strip() for segment in segments).strip()

    @staticmethod
    def _to_srt(segments: list[SingleSegment]) -> list[Segment]:
        """
        Converts recognition segments into SRT-like structured segments.

        :param segments: List of recognition segments.

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

    def _recognize(
        self,
        file: UploadFile,
        model: Model = Model.SMALL,
        language: Language | None = None,
    ) -> list[SingleSegment]:
        """
        Recognizes speech from the uploaded audio file using the specified model and language.

        The file is temporarily saved to disk and passed to the underlying recognizer.

        :param file: Uploaded audio file to be processed.
        :param model: Recognition model to use (e.g., Model.SMALL, Model.MEDIUM).
        :param language: Optional language enum value (e.g., Language.EN, Language.RU).

        :return: List of recognized segments containing transcribed text and timestamps.
        """

        with temporary_audio_file(file) as path:
            return self._recognizer.recognize(
                audio_file=path, model=model, language=language
            )

    def clean(self):
        """
        Clean up resources held by the recognizer (e.g., cached models).
        Should be called on application shutdown.
        """

        self._recognizer.clean()
