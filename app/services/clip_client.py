import os

import httpx
from PIL import Image


CLIP_SERVICE_URL = os.getenv("CLIP_SERVICE_URL")


def create_embedding(image: Image.Image) -> list[float]:

    if not CLIP_SERVICE_URL:
        raise RuntimeError(
            "CLIP_SERVICE_URL is not configured"
        )

    buffer = __import__("io").BytesIO()

    image.save(
        buffer,
        format="JPEG"
    )

    buffer.seek(0)

    response = httpx.post(
        f"{CLIP_SERVICE_URL}/embedding",
        files={
            "file": (
                "image.jpg",
                buffer,
                "image/jpeg"
            )
        },
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["embedding"]