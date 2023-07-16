import asyncio
import logging
import shutil
from typing import Annotated

from fastapi import FastAPI, Form, UploadFile, WebSocket
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from whispercpp import Whisper

from .a1111 import generate_a1111_controlnet
from .image_util import pil_image_from_b64, pil_image_to_b64

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

whisper = Whisper("base")

last_artwork_cache = {
    "scribble_b64": None,
    "image_b64": None,
    "prompt": None,
}
new_artwork_available_event = asyncio.Event()


class GeneratePayload(BaseModel):
    scribble_control_png_b64: str
    prompt: str


@app.post("/generate")
async def generate(payload: GeneratePayload):
    scribble_byte_len = len(payload.scribble_control_png_b64)

    pil_img = pil_image_from_b64(payload.scribble_control_png_b64).convert("RGB")

    result_img = generate_a1111_controlnet(pil_img, payload.prompt)

    b64_converted = pil_image_to_b64(result_img)

    last_artwork_cache.update(
        {
            "scribble_b64": payload.scribble_control_png_b64,
            "image_b64": b64_converted,
            "prompt": payload.prompt,
        }
    )
    new_artwork_available_event.set()

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
    while True:
        if last_artwork_cache["image_b64"] is not None:
            logger.info("Sending cached artwork...")
            await websocket.send_json(last_artwork_cache)
        new_artwork_available_event.clear()
        logger.info("Waiting for new artwork...")
        await new_artwork_available_event.wait()


app.mount("/", StaticFiles(directory="web_static", html=True), name="web_static")
