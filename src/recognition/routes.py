from typing import Union

from fastapi import APIRouter, File, Form, UploadFile

from src.auth.security.dependencies import CurrentUserDep
from src.recognition.dependencies import RecognitionServiceDep
from src.recognition.enums import Language
from src.recognition.enums import Model as Model
from src.recognition.enums import ResultFormat
from src.recognition.schemas import (
    LanguageList,
    ModelList,
    RecognitionSrtResult,
    RecognitionTextResult,
)

router = APIRouter(prefix="/recognition", tags=["Recognition"])


@router.get(
    "/models",
    summary="Get available models",
    description="Returns a list of available speech recognition models.",
    responses={
        200: {
            "description": "List of available models",
        },
    },
)
async def get_models() -> ModelList:
    """
    Get a list of supported recognition models.

    :return: A list of model names.
    """

    return ModelList(models=Model.values())


@router.get(
    "/languages",
    summary="Get available languages",
    description="Returns a list of supported languages for recognition.",
    responses={
        200: {
            "description": "List of supported languages",
        },
    },
)
async def get_languages() -> LanguageList:
    """
    Get a list of supported recognition languages.

    :return: A list of language codes.
    """

    return LanguageList(languages=Language.values())


@router.post(
    "/recognize",
    summary="Recognize speech from audio",
    description="Uploads an audio file and returns the recognized speech either as plain text or in SRT subtitle format.",
    responses={
        200: {
            "description": "Recognition result",
        },
    },
)
async def recognize(
    recognition_service: RecognitionServiceDep,
    user: CurrentUserDep,
    file: UploadFile = File(...),
    language: Language | None = Form(None),
    model: Model = Form(Model.SMALL),
    result_format: ResultFormat = Form(ResultFormat.TEXT),
) -> Union[RecognitionSrtResult, RecognitionTextResult]:
    """
    Recognize speech from uploaded audio file.

    :param file: Audio file in supported format (e.g., .mp3, .wav).
    :param language: Optional language hint for recognition.
    :param model: Recognition model to use.
    :param result_format: Desired format of the result.
    :param recognition_service: Injected recognition service.
    :param user: Authenticated user (injected).

    :return: Recognition result as plain text or SRT.
    """

    return recognition_service.recognize(file, model, language, result_format)
