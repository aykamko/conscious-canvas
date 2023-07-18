import logging
import shutil
import uuid
from typing import Annotated, Optional
from enum import Enum
from websockets.exceptions import WebSocketException

from fastapi import FastAPI, Form, UploadFile, WebSocket
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from whispercpp import Whisper

from .a1111 import generate_a1111_controlnet
from .image_util import pil_image_from_b64, pil_image_to_b64
from .async_util import YieldingQueue

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ProjectionEventType = Enum(
    "ProjectionEventType",
    [
        "PROJECTION_CLIENT_CONNECTED",
        "GENERATION_STARTING",
        "ARTWORK_GENERATED",
    ],
)

projection_event_queue = YieldingQueue()


class ProjectionEvent(BaseModel):
    event_type: ProjectionEventType


class ProjectionClientConnectedEvent(ProjectionEvent):
    event_type: ProjectionEventType = ProjectionEventType.PROJECTION_CLIENT_CONNECTED
    client_id: uuid.UUID


class GenerationStartedPayload(ProjectionEvent):
    event_type: ProjectionEventType = ProjectionEventType.GENERATION_STARTING
    scribble_b64: str
    prompt: str


class ArtworkGeneratedPayload(ProjectionEvent):
    event_type: ProjectionEventType = ProjectionEventType.ARTWORK_GENERATED
    scribble_b64: str
    prompt: str
    image_b64: str


class GeneratePayload(BaseModel):
    scribble_control_png_b64: str
    prompt: str


app = FastAPI()

whisper = Whisper("base")


@app.post("/generate")
async def generate(payload: GeneratePayload):
    scribble_byte_len = len(payload.scribble_control_png_b64)

    pil_img = pil_image_from_b64(payload.scribble_control_png_b64).convert("RGB")

    await projection_event_queue.put(
        GenerationStartedPayload(
            scribble_b64=payload.scribble_control_png_b64,
            prompt=payload.prompt,
        )
    )
    result_img = await generate_a1111_controlnet(pil_img, payload.prompt)

    b64_converted = pil_image_to_b64(result_img)

    await projection_event_queue.put(
        ArtworkGeneratedPayload(
            scribble_b64=payload.scribble_control_png_b64,
            prompt=payload.prompt,
            image_b64=b64_converted,
        )
    )

    return {
        "message": f"scribble_byte_len: {scribble_byte_len}",
        "img_b64": b64_converted,
    }


@app.post("/transcribe")
async def transcribe(audio_file: Annotated[UploadFile, Form()]):
    TEMP_FILE = "recording.wav"
    with open(TEMP_FILE, "wb") as out_file:
        shutil.copyfileobj(audio_file.file, out_file)

    embedding = whisper.transcribe(TEMP_FILE)
    text = "".join(whisper.extract_text(embedding))

    return {"transcription": text}


@app.websocket("/projection-ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = uuid.uuid4()
    await projection_event_queue.put(
        ProjectionClientConnectedEvent(client_id=client_id)
    )
    while True:
        event: ProjectionEvent = await projection_event_queue.get()
        match event.event_type:
            case ProjectionEventType.PROJECTION_CLIENT_CONNECTED:
                if event.client_id != client_id:
                    return  # new client connected, aborting this one
            case ProjectionEventType.ARTWORK_GENERATED | ProjectionEventType.GENERATION_STARTING:
                payload = event.dict()
                payload['event_type'] = payload['event_type'].name
                logger.info("Sending event: %s", payload['event_type'])

                try:
                    await websocket.send_json(payload)
                except WebSocketException:
                    logger.info("Client disconnected")
                    return


app.mount("/", StaticFiles(directory="web_static", html=True), name="web_static")
