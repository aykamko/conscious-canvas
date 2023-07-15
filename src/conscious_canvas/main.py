from typing import Annotated
import logging
from fastapi import FastAPI, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil

from .image_util import pil_image_from_b64, pil_image_to_b64
from .a1111 import generate_a1111_controlnet

logging.basicConfig(level=logging.INFO)

app = FastAPI()


class GeneratePayload(BaseModel):
    scribble_control_png_b64: str
    prompt: str


@app.post("/generate")
async def generate(payload: GeneratePayload):
    scribble_byte_len = len(payload.scribble_control_png_b64)

    pil_img = pil_image_from_b64(payload.scribble_control_png_b64).convert("RGB")

    result_img = generate_a1111_controlnet(pil_img, payload.prompt)

    b64_converted = pil_image_to_b64(result_img)

    return {
        "message": f"scribble_byte_len: {scribble_byte_len}",
        "img_b64": b64_converted,
    }


@app.post("/whisper")
async def whisper(audio_file: Annotated[UploadFile, Form()]):
    # import ipdb; ipdb.set_trace()
    with open("recording.wav", "wb") as out_file:
        shutil.copyfileobj(audio_file.file, out_file)
    return {"message": "whisper"}


app.mount("/", StaticFiles(directory="web_static", html=True), name="web_static")
