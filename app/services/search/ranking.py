from google import genai
from google.genai import types
from pydantic import BaseModel,Field
from app.core.config import settings
from app.core.exceptions import ImageSearchException
class RankedProduct(BaseModel): product_id:str; score:float=Field(ge=0,le=1); reason:str
class RankingResponse(BaseModel): results:list[RankedProduct]
class LLMRankingService:
    def __init__(self): self.client=genai.Client(api_key=settings.gemini_api_key)
    def rerank(self,context):
        prompt=f"""You are an e-commerce visual-search reranker. Rank only the supplied candidates against the image query. Visual similarity is strongest, followed by category, subcategory, brand, color and attributes. Never invent IDs. Return at most {settings.rerank_k} candidates. Context:\n{context}"""
        try:
            r=self.client.models.generate_content(model=settings.gemini_model,contents=prompt,config=types.GenerateContentConfig(response_mime_type="application/json",response_schema=RankingResponse,temperature=0.1))
            return RankingResponse.model_validate_json(r.text)
        except Exception as exc: raise ImageSearchException("AI_SERVICE_ERROR",f"Reranking failed: {exc}",502,True)
