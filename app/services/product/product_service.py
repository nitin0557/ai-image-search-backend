import uuid
from app.db.database import SessionLocal
from app.db.models import Product,ProductEmbedding
from app.services.image.downloader import download_image
from app.services.embeddings.clip import image_embedding
async def index_product(data):
    image,_=await download_image(str(data.image_url)); vector=image_embedding(image); pid=str(uuid.uuid4())
    with SessionLocal() as db:
        db.add(Product(id=pid,name=data.name,description=data.description,category=data.category,subcategory=data.subcategory,brand=data.brand,color=data.color,price=data.price,image_url=str(data.image_url),attributes=data.attributes))
        db.add(ProductEmbedding(id=str(uuid.uuid4()),product_id=pid,embedding=vector)); db.commit()
    return pid
