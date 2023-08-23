from transformers import CLIPFeatureExtractor
from diffusers.pipelines.stable_diffusion.safety_checker import StableDiffusionSafetyChecker
from PIL import Image
import numpy as np


class NSFWChecker:
    def __init__(self):
        self.feature_extractor = CLIPFeatureExtractor.from_pretrained("openai/clip-vit-base-patch32")
        self.safety_checker = StableDiffusionSafetyChecker.from_pretrained(
            "runwayml/stable-diffusion-v1-5", subfolder="safety_checker"
        )

    def check_image(self, image: Image.Image) -> bool:
        safety_checker_input = self.feature_extractor(images=image, return_tensors="pt")
        _, has_nsfw_concept = self.safety_checker(images=[np.array(image)], clip_input=safety_checker_input.pixel_values)
        return has_nsfw_concept[0]
