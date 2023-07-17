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


class GeneratePayload(BaseModel):
    scribble_control_png_b64: str
    prompt: str


class ArtworkPayload(BaseModel):
    scribble_b64: str
    prompt: str
    image_b64: Optional[str] = None


ProjectionEvent = Enum(
    "ProjectionEvent",
    [
        "PROJECTION_CLIENT_CONNECTED",
        "GENERATION_STARTING",
        "NEW_ARTWORK_AVAILABLE",
    ],
)


app = FastAPI()

whisper = Whisper("base")

last_artwork_cache: Optional[ArtworkPayload] = None

projection_event_queue = YieldingQueue()
projection_client_id = None


@app.post("/generate")
async def generate(payload: GeneratePayload):
    global last_artwork_cache
    last_artwork_cache = ArtworkPayload(
        scribble_b64=payload.scribble_control_png_b64,
        prompt=payload.prompt,
    )

    scribble_byte_len = len(payload.scribble_control_png_b64)

    pil_img = pil_image_from_b64(payload.scribble_control_png_b64).convert("RGB")

    await projection_event_queue.put(ProjectionEvent.GENERATION_STARTING)
    result_img = await generate_a1111_controlnet(pil_img, payload.prompt)

    b64_converted = pil_image_to_b64(result_img)

    last_artwork_cache = ArtworkPayload(
        scribble_b64=payload.scribble_control_png_b64,
        image_b64=b64_converted,
        prompt=payload.prompt,
    )
    await projection_event_queue.put(ProjectionEvent.NEW_ARTWORK_AVAILABLE)

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
    global projection_client_id
    my_client_id = projection_client_id = uuid.uuid4()
    await websocket.accept()
    await projection_event_queue.put(ProjectionEvent.PROJECTION_CLIENT_CONNECTED)
    if last_artwork_cache is not None and last_artwork_cache.image_b64 is not None:
        logger.info("Sending cached artwork...")
        payload = {
            "event_type": ProjectionEvent.NEW_ARTWORK_AVAILABLE.name,
            **last_artwork_cache.dict(),
        }
        await websocket.send_json(payload)
    while True:
        event: ProjectionEvent = await projection_event_queue.get()
        payload = {"event_type": event.name}
        if event in [
            ProjectionEvent.NEW_ARTWORK_AVAILABLE,
            ProjectionEvent.GENERATION_STARTING,
        ]:
            payload.update(last_artwork_cache.dict())
        elif event == ProjectionEvent.PROJECTION_CLIENT_CONNECTED:
            if my_client_id != projection_client_id:
                logger.info("A new client connected")
                return
            continue
        logger.info("Sending event: %s", event.name)

        try:
            await websocket.send_json(payload)
        except WebSocketException:
            logger.info("Client disconnected")
            return


app.mount("/", StaticFiles(directory="web_static", html=True), name="web_static")
