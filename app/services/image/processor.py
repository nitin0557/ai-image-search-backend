import io
from PIL import Image
def image_to_bytes(image:Image.Image):
    out=io.BytesIO(); image.save(out,format="JPEG",quality=90); return out.getvalue()
