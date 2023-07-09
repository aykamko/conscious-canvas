from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

class GeneratePayload(BaseModel):
    scribble_control_png_b64: str


@app.post("/generate")
async def generate(payload: GeneratePayload):
    scribble_byte_len = len(payload.scribble_control_png_b64)
    return {
        "message": f"scribble_byte_len: {scribble_byte_len}",
        "img_b64": payload.scribble_control_png_b64,
    }


app.mount("/", StaticFiles(directory="web_static", html=True), name="web_static")