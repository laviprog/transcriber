from typing import Annotated

from fastapi import Depends, Request

from src.recognition.services import RecognitionService


def provide_recognition_service(request: Request) -> RecognitionService:
    """
    Dependency function that retrieves the RecognitionService instance
    from the FastAPI app state.
    """

    return request.app.state.recognition_service


# FastAPI dependency type for injecting RecognitionService
RecognitionServiceDep = Annotated[
    RecognitionService, Depends(provide_recognition_service)
]
