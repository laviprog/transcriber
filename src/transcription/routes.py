from typing import Union

from fastapi import APIRouter, File, Form, UploadFile

from src.auth.security.dependencies import CurrentUserDep
from src.transcription.dependencies import SpeechTranscriptionServiceDep
from src.transcription.enums import Language
from src.transcription.enums import Model as Model
from src.transcription.enums import ResultFormat
from src.transcription.schemas import (
    LanguageList,
    ModelList,
    TranscriptionSrtResult,
    TranscriptionTextResult,
)

router = APIRouter(prefix="/transcription", tags=["Transcription"])


@router.get(
    "/models",
    summary="Get available models",
    description="Returns a list of available speech transcription models.",
    responses={
        200: {
            "description": "List of available models",
        },
    },
)
async def get_models() -> ModelList:
    """
    Get a list of supported transcription models.

    :return: A list of model names.
    """

    return ModelList(models=Model.values())


@router.get(
    "/languages",
    summary="Get available languages",
    description="Returns a list of supported languages for transcription.",
    responses={
        200: {
            "description": "List of supported languages",
        },
    },
)
async def get_languages() -> LanguageList:
    """
    Get a list of supported transcription languages.

    :return: A list of language codes.
    """

    return LanguageList(languages=Language.values())


@router.post(
    "/transcribe",
    summary="Transcribe speech from audio",
    description="Uploads an audio file and returns the transcribed speech either as plain text or in SRT subtitle format.",
    responses={
        200: {
            "description": "Transcription result",
        },
    },
)
async def transcribe(
    transcription_service: SpeechTranscriptionServiceDep,
    user: CurrentUserDep,
    file: UploadFile = File(...),
    language: Language | None = Form(None),
    model: Model = Form(Model.SMALL),
    result_format: ResultFormat = Form(ResultFormat.TEXT),
) -> Union[TranscriptionSrtResult, TranscriptionTextResult]:
    """
    Transcribe speech from uploaded audio file.

    :param file: Audio file in supported format (e.g., .mp3, .wav).
    :param language: Optional language hint for transcription.
    :param model: Transcription model to use.
    :param result_format: Desired format of the result.
    :param transcription_service: Injected transcription service.
    :param user: Authenticated user (injected).

    :return: Transcription result as plain text or SRT.
    """

    return transcription_service.transcribe(
        file, model, language, result_format
    )
