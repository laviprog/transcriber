from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.recognition.enums import Model
from src.recognition.recognizer import Recognizer
from src.recognition.services import RecognitionService


@asynccontextmanager
async def lifespan(app: FastAPI):
    recognizer = Recognizer(
        device=settings.DEVICE,
        compute_type=settings.COMPUTE_TYPE,
        download_root=settings.DOWNLOAD_ROOT,
        init_models=[Model.SMALL],
    )

    recognition_service = RecognitionService(recognizer=recognizer)
    app.state.recognition_service = recognition_service

    yield

    recognition_service.clean()
