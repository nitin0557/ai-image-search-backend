import json
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.exceptions import ImageSearchException
from app.schemas.image_search import ProductAnalysis
class GeminiVisionService:
    def __init__(self): self.client=genai.Client(api_key=settings.gemini_api_key)
    def analyze(self,image_bytes):
        prompt="""
Analyze this e-commerce image. Determine whether a recognizable PRODUCT is present.
Ignore people, scenery, backgrounds and unrelated objects.
If no recognizable product exists, product_detected=false.
If a product exists, extract category, subcategory, visible brand, colors,
material, gender/target audience, important attributes and description.
Never invent a brand. Return structured JSON only.
"""
        try:
            response=self.client.models.generate_content(
                model=settings.gemini_model,
                contents=[types.Part.from_bytes(data=image_bytes,mime_type="image/jpeg"),prompt],
                config=types.GenerateContentConfig(response_mime_type="application/json",response_schema=ProductAnalysis,temperature=0.1),
            )
            return ProductAnalysis.model_validate(json.loads(response.text))
        except Exception as exc: raise ImageSearchException("AI_SERVICE_ERROR",f"Vision analysis failed: {exc}",502,True)
