from typing import Annotated

from fastapi import Depends, Request

from src.transcription.services import SpeechTranscriptionService


def provide_transcription_service(
    request: Request,
) -> SpeechTranscriptionService:
    """
    Dependency function that retrieves the SpeechTranscriptionService instance
    from the FastAPI app state.
    """

    return request.app.state.transcription_service


SpeechTranscriptionServiceDep = Annotated[
    SpeechTranscriptionService, Depends(provide_transcription_service)
]
