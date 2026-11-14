from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Product
from app.schemas.product import ProductIndexRequest, ProductResponse
from app.services.product_indexer import ProductIndexer

router = APIRouter(prefix="/products", tags=["Products"])
indexer = ProductIndexer()


@router.post("/index")
def index_product(product: ProductIndexRequest, db: Session = Depends(get_db)):
    try:
        indexed = indexer.index_product(db=db, product_data=product)
        return {
            "success": True,
            "message": "Product indexed successfully",
            "product": ProductResponse(
                id=indexed.id,
                name=indexed.name,
                description=indexed.description,
                category=indexed.category,
                subcategory=indexed.subcategory,
                brand=indexed.brand,
                color=indexed.color,
                price=indexed.price,
                image_url=indexed.image_url,
                attributes=indexed.attributes or [],
                has_embedding=indexed.embedding is not None,
            ),
        }
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/", response_model=dict)
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).order_by(Product.created_at.desc()).all()
    return {
        "success": True,
        "count": len(products),
        "products": [
            ProductResponse(
                id=p.id,
                name=p.name,
                description=p.description,
                category=p.category,
                subcategory=p.subcategory,
                brand=p.brand,
                color=p.color,
                price=p.price,
                image_url=p.image_url,
                attributes=p.attributes or [],
                has_embedding=p.embedding is not None,
            ).model_dump()
            for p in products
        ],
    }
