from functools import lru_cache

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

from app.core.config import settings


class CLIPService:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.model.eval()

    def create_embedding(self, image: Image.Image) -> list[float]:
        image = image.convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")

        with torch.no_grad():
            vision_outputs = self.model.vision_model(
                pixel_values=inputs["pixel_values"]
            )
            features = self.model.visual_projection(vision_outputs.pooler_output)

        features = features / features.norm(p=2, dim=-1, keepdim=True)
        embedding = features[0].cpu().numpy().tolist()

        if len(embedding) != settings.vector_dim:
            raise ValueError(
                f"Expected CLIP embedding dimension {settings.vector_dim}, "
                f"got {len(embedding)}"
            )
        return embedding


@lru_cache(maxsize=1)
def get_clip_service() -> CLIPService:
    return CLIPService()


clip_service = get_clip_service()
