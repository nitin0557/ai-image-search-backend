from io import BytesIO

import httpx
from PIL import Image
from sqlalchemy.orm import Session

from app.db.models import Product
from app.services.clip_client import create_embedding


class ProductIndexer:

    def index_product(
        self,
        db: Session,
        product_data
    ) -> Product:

        response = httpx.get(
            product_data.image_url,
            timeout=20,
            follow_redirects=True,
            headers={
                "User-Agent": "AIImageSearch/1.0"
            },
        )

        response.raise_for_status()

        image = Image.open(
            BytesIO(response.content)
        ).convert("RGB")

        # Call external CLIP service
        embedding = create_embedding(image)

        product = (
            db.query(Product)
            .filter(
                Product.id == product_data.id
            )
            .first()
        )

        if product is None:
            product = Product(
                id=product_data.id
            )
            db.add(product)

        product.name = product_data.name
        product.description = product_data.description
        product.category = product_data.category
        product.subcategory = product_data.subcategory
        product.brand = product_data.brand
        product.color = product_data.color
        product.price = product_data.price
        product.image_url = product_data.image_url
        product.attributes = (
            product_data.attributes or []
        )
        product.embedding = embedding

        db.commit()
        db.refresh(product)

        return product