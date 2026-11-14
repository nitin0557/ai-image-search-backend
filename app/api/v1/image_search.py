from fastapi import APIRouter,UploadFile,File,HTTPException
from app.schemas.image_search import ImageSearchUrlRequest
from app.services.search.image_search_service import ImageSearchService
from app.core.exceptions import ImageSearchException
router=APIRouter(prefix="/image-search",tags=["image-search"]); service=ImageSearchService()
def err(e): raise HTTPException(status_code=e.status_code,detail={"success":False,"error":{"code":e.code,"message":e.message,"retryable":e.retryable}})
@router.post("/upload")
async def upload(file:UploadFile=File(...)):
    try: return await service.search_file(file)
    except ImageSearchException as e: err(e)
@router.post("/url")
async def url(request:ImageSearchUrlRequest):
    try: return await service.search_url(str(request.image_url))
    except ImageSearchException as e: err(e)
