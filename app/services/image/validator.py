import io
from PIL import Image, UnidentifiedImageError
from app.core.config import settings
from app.core.exceptions import ImageSearchException
ALLOWED={"image/jpeg","image/png","image/webp"}
def validate_image_bytes(data,content_type=None):
    if not data: raise ImageSearchException("INVALID_IMAGE","Image is empty.")
    if len(data)>settings.max_image_size_mb*1024*1024: raise ImageSearchException("IMAGE_TOO_LARGE","Image is too large.",413)
    if content_type and content_type not in ALLOWED: raise ImageSearchException("UNSUPPORTED_IMAGE","Unsupported image format.",415)
    try:
        probe=Image.open(io.BytesIO(data)); probe.verify(); image=Image.open(io.BytesIO(data)).convert("RGB")
    except (UnidentifiedImageError,OSError): raise ImageSearchException("INVALID_IMAGE","Invalid image.")
    if image.width*image.height>settings.max_image_pixels: raise ImageSearchException("IMAGE_TOO_LARGE","Image dimensions are too large.",413)
    return image
