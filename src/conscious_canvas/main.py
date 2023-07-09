from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .image_util import pil_image_from_b64, pil_image_to_b64

app = FastAPI()


class GeneratePayload(BaseModel):
    scribble_control_png_b64: str


@app.post("/generate")
async def generate(payload: GeneratePayload):
    scribble_byte_len = len(payload.scribble_control_png_b64)

    pil_img = pil_image_from_b64(payload.scribble_control_png_b64).convert('RGB')
    b64_converted = pil_image_to_b64(pil_img)

    return {
        "message": f"scribble_byte_len: {scribble_byte_len}",
        "img_b64": b64_converted,
    }


app.mount("/", StaticFiles(directory="web_static", html=True), name="web_static")