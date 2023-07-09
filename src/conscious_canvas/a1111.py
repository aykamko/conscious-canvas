import requests
from PIL import Image

from .image_util import pil_image_from_b64, pil_image_to_b64

A1111_URL = "http://127.0.0.1:7860"


def generate_a1111_controlnet(pil_img: Image, img_size: int = 512) -> Image.Image:
    pil_img = pil_img.resize((img_size, img_size))

    a1111_payload = {
        "prompt": "an airplane flying above the clouds",
        "negative_prompt": "",
        "batch_size": 1,
        "steps": 50,
        "cfg_scale": 7,
        "sampler_name": "DPM++ 2M SDE Karras",
        "width": img_size,
        "height": img_size,
        "alwayson_scripts": {
            "controlnet": {
                "args": [
                    {
                        "input_image": pil_image_to_b64(pil_img),
                        "module": "scribble",
                        "model": "control_v11p_sd15_scribble [d4ba51ff]",
                    }
                ]
            }
        },
    }

    resp = requests.post(url=f"{A1111_URL}/sdapi/v1/txt2img", json=a1111_payload)

    resp_data = resp.json()
    import ipdb; ipdb.set_trace()
    result = resp_data["images"][0]
    result_pil = pil_image_from_b64(result)

    return result_pil
