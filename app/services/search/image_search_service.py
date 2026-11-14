import uuid

from app.core.exceptions import ImageSearchException
from app.db.database import SessionLocal
from app.db.models import SearchHistory
from app.schemas.image_search import ImageSearchResponse, ProductResult
from app.services.embeddings.clip import image_embedding
from app.services.image.downloader import download_image
from app.services.image.processor import image_to_bytes
from app.services.image.validator import validate_image_bytes
from app.services.rag.rag_service import build_context
from app.services.search.ranking import LLMRankingService
from app.services.vector.search import vector_search
from app.services.vision.gemini import GeminiVisionService


class ImageSearchService:
    def __init__(self):
        self.vision = GeminiVisionService()
        self.ranker = LLMRankingService()

    async def search_file(self, file):
        data = await file.read()
        image = validate_image_bytes(data, file.content_type)
        return self._run(image, image_to_bytes(image), file.filename or "upload")

    async def search_url(self, url):
        image, _ = await download_image(url)
        return self._run(image, image_to_bytes(image), url)

    def _run(self, image, image_bytes, source):
        query = self.vision.analyze(image_bytes)
        if not query.product_detected:
            raise ImageSearchException(
                "NO_PRODUCT_DETECTED",
                "No recognizable product was detected.",
                422,
                False,
            )

        candidates = vector_search(image_embedding(image))
        search_id = str(uuid.uuid4())

        if not candidates:
            self._history(search_id, source, query.model_dump(), 0)
            return ImageSearchResponse(
                success=True, search_id=search_id, query=query, results=[]
            )

        ranking = self.ranker.rerank(build_context(query, candidates))
        by_id = {p["product_id"]: p for p in candidates}
        results = []

        for ranked in ranking.results:
            product = by_id.get(ranked.product_id)
            if product:
                results.append(
                    ProductResult(
                        product_id=product["product_id"],
                        name=product["name"],
                        image_url=product["image_url"],
                        price=product["price"],
                        similarity=product["similarity"],
                        final_score=ranked.score,
                        reason=ranked.reason,
                    )
                )

        self._history(search_id, source, query.model_dump(), len(results))
        return ImageSearchResponse(
            success=True, search_id=search_id, query=query, results=results
        )

    @staticmethod
    def _history(search_id, source, query, count):
        try:
            with SessionLocal() as db:
                db.add(
                    SearchHistory(
                        id=search_id,
                        image_source=source,
                        query=query,
                        result_count=count,
                    )
                )
                db.commit()
        except Exception:
            # Search history must never make an otherwise successful search fail.
            pass
