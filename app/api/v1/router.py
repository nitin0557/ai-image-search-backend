from fastapi import APIRouter

from app.api.v1.image_search import router as image_router
from app.api.v1.products import router as product_router

router = APIRouter()
router.include_router(image_router)
router.include_router(product_router)
