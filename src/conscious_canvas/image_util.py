import base64
import re
from io import BytesIO

from PIL import Image


def pil_image_from_b64(b64_str: str) -> Image.Image:
    b64_str = re.sub(r"^data:.*?base64,", "", b64_str)  # remove data type prefix
    return Image.open(BytesIO(base64.b64decode(b64_str)))


def pil_image_to_b64(pil_img: Image.Image) -> str:
    buffered = BytesIO()
    pil_img.save(buffered, format="JPEG")
    b64_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{b64_str}"
