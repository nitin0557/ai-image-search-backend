from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, Float, JSON, String, Text

from app.db.database import Base
from app.core.config import settings


class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(200), nullable=True)
    subcategory = Column(String(200), nullable=True)
    brand = Column(String(200), nullable=True)
    color = Column(String(200), nullable=True)
    price = Column(Float, nullable=True)
    image_url = Column(Text, nullable=False)
    attributes = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    embedding = Column(Vector(settings.vector_dim), nullable=True)


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(String(36), primary_key=True, index=True)
    image_source = Column(Text, nullable=True)
    query = Column(JSON, nullable=True)
    result_count = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
