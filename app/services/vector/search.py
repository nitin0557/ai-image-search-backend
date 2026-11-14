from sqlalchemy import select

from app.core.config import settings
from app.db.database import SessionLocal
from app.db.models import Product


def vector_search(embedding: list[float], limit: int | None = None) -> list[dict]:
    limit = limit or settings.top_k
    distance = Product.embedding.cosine_distance(embedding)

    with SessionLocal() as db:
        rows = db.execute(
            select(Product, distance.label("distance"))
            .where(Product.embedding.is_not(None))
            .order_by(distance)
            .limit(limit)
        ).all()

    results = []
    for product, distance_value in rows:
        distance_value = float(distance_value)
        results.append(
            {
                "product_id": product.id,
                "name": product.name,
                "description": product.description,
                "category": product.category,
                "subcategory": product.subcategory,
                "brand": product.brand,
                "color": product.color,
                "price": product.price,
                "image_url": product.image_url,
                "attributes": product.attributes or [],
                "similarity": max(0.0, min(1.0, 1.0 - distance_value)),
            }
        )
    return results
