from pydantic import BaseModel, Field, HttpUrl


class ImageSearchUrlRequest(BaseModel):
    image_url: HttpUrl


class ProductAnalysis(BaseModel):
    product_detected: bool
    category: str | None = None
    subcategory: str | None = None
    brand: str | None = None
    color: list[str] = Field(default_factory=list)
    material: str | None = None
    gender: str | None = None
    attributes: list[str] = Field(default_factory=list)
    description: str | None = None


class ProductResult(BaseModel):
    product_id: str
    name: str
    image_url: str
    price: float | None = None
    similarity: float
    final_score: float
    reason: str | None = None


class ImageSearchResponse(BaseModel):
    success: bool
    search_id: str
    query: ProductAnalysis
    results: list[ProductResult]
