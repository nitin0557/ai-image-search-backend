from pydantic import BaseModel, Field


class ProductIndexRequest(BaseModel):
    id: str = Field(min_length=1, max_length=36)
    name: str = Field(min_length=1, max_length=500)
    description: str | None = None
    category: str | None = None
    subcategory: str | None = None
    brand: str | None = None
    color: str | None = None
    price: float | None = None
    image_url: str
    attributes: list[str] = Field(default_factory=list)


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    category: str | None = None
    subcategory: str | None = None
    brand: str | None = None
    color: str | None = None
    price: float | None = None
    image_url: str
    attributes: list[str] = Field(default_factory=list)
    has_embedding: bool

    model_config = {"from_attributes": True}
