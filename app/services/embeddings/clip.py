# Compatibility wrapper. All image embeddings use the same CLIP pipeline.
from PIL import Image

from app.services.clip_service import clip_service


def image_embedding(image: Image.Image) -> list[float]:
    return clip_service.create_embedding(image)
