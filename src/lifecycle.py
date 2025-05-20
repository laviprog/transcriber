from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.transcription.enums import Model
from src.transcription.services import SpeechTranscriptionService
from src.transcription.speech_transcription import SpeechTranscription


@asynccontextmanager
async def lifespan(app: FastAPI):
    transcriber = SpeechTranscription(
        device=settings.DEVICE,
        compute_type=settings.COMPUTE_TYPE,
        download_root=settings.DOWNLOAD_ROOT,
        init_models=[Model.SMALL],
    )

    transcription_service = SpeechTranscriptionService(transcriber=transcriber)
    app.state.transcription_service = transcription_service

    yield

    transcription_service.clean()
