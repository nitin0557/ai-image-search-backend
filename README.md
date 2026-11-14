# AI Image Search Backend

FastAPI + Gemini Vision + CLIP image embeddings + PostgreSQL/pgvector + RAG + Gemini reranking.

## Local development

1. Copy `.env.example` to `.env`.
2. Add your Gemini API key to `.env`.
3. Start the stack:

```bash
docker compose up --build
```

Swagger: http://localhost:8000/docs

Health: http://localhost:8000/health

Products: http://localhost:8000/api/v1/products/

## Index a product

Use `POST /api/v1/products/index` in Swagger.

Example:

```json
{
  "id": "TI10001",
  "name": "Black Running Shoes",
  "description": "Mens black running shoes",
  "category": "Footwear",
  "subcategory": "Running Shoes",
  "brand": "Nike",
  "color": "black",
  "price": 2499,
  "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800",
  "attributes": ["black", "sports", "running", "mens"]
}
```

## Check indexed products

Open:

```text
http://localhost:8000/api/v1/products/
```

This is a GET endpoint and returns product metadata plus `has_embedding`.

## Image search

Upload:

```bash
curl -X POST http://localhost:8000/api/v1/image-search/upload \
  -F "file=@/absolute/path/image.jpg"
```

URL:

```bash
curl -X POST http://localhost:8000/api/v1/image-search/url \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://example.com/query.jpg"}'
```

## Architecture

Customer image -> FastAPI -> Gemini Vision + CLIP -> pgvector top-K -> RAG context -> Gemini reranking -> results.

The same `CLIPService` is used for product indexing and customer image queries, so vectors are generated with the same model and preprocessing.

## Production note

Vercel can host the FastAPI application, but PostgreSQL/pgvector and Redis/Celery should be external managed services. The Docker Compose stack is intended for local development.

Never commit `.env` or API keys.
