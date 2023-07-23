import os
import logging
import time
import json
import pprint
import asyncio

import aiohttp
from PIL import Image

from .image_util import pil_image_from_b64, pil_image_to_b64

logger = logging.getLogger(__name__)

A1111_URL = "http://127.0.0.1:7860"


async def mock_generate_a1111_controlnet(
    prompt: str, img_size: int = 512
) -> Image.Image:
    mock_img = Image.new("RGB", (img_size, img_size), color="blue")
    await asyncio.sleep(1) # sleep so progress bar is visible
    return mock_img


async def generate_a1111_controlnet(
    sketch_img: Image, prompt: str, img_size: int = 512
) -> Image.Image:
    if os.environ['MOCK_A1111'].lower() == 'true':
        return await mock_generate_a1111_controlnet(prompt, img_size)
    sketch_img = sketch_img.resize((img_size, img_size))

    a1111_payload = {
        "prompt": prompt,
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
                        "input_image": pil_image_to_b64(sketch_img),
                        "module": "scribble_pidinet",
                        "model": "control_v11p_sd15_scribble [d4ba51ff]",
                        "processor_res": img_size,
                    }
                ]
            }
        },
    }

    req_start_time = time.time()
    logger.info("Sending request to A1111")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"{A1111_URL}/sdapi/v1/txt2img", json=a1111_payload
        ) as resp:
            resp_data = await resp.json()

    gen_info = json.loads(resp_data["info"])
    logger.info("A1111 info: %s", pprint.pformat(gen_info))

    logger.info(
        "Received response from A1111, time elapsed: %s", time.time() - req_start_time
    )

    result = resp_data["images"][0]
    result_pil = pil_image_from_b64(result)

    return result_pil
