import httpx
from app.core.exceptions import ImageSearchException
from app.services.image.validator import validate_image_bytes
async def download_image(url):
    try:
        async with httpx.AsyncClient(follow_redirects=True,timeout=15) as client: response=await client.get(url,headers={"User-Agent":"AIImageSearch/1.0"})
    except Exception: raise ImageSearchException("INVALID_IMAGE_URL","Could not reach image URL.",422,True)
    if response.status_code>=400: raise ImageSearchException("INVALID_IMAGE_URL","Image URL returned an error.",422,True)
    ct=response.headers.get("content-type","").split(";")[0].lower()
    if ct not in {"image/jpeg","image/png","image/webp"}: raise ImageSearchException("INVALID_IMAGE_URL","URL is not a supported image.",422,True)
    return validate_image_bytes(response.content,ct),response.content
