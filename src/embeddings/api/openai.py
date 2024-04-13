from typing import List

from fastapi import APIRouter, Query

from embeddings.api.schema import EmbeddingRequest, SearchRequest
from embeddings.domain.embeddings import domain_save_embeddings, openai_collection_clean, openai_collection_raw, openai_embedding_function

openai_router = APIRouter(
    prefix="/openai",
    tags=["openai"],
)


@openai_router.post(
    "/embeddings",
)
async def save_embedding(
    request: List[EmbeddingRequest]
):
    await domain_save_embeddings(request)
    return {"message": "Embeddings saved"}


@openai_router.post(
    "/search",
)
async def search(
    request: SearchRequest,
    n_results: int = Query(3),
    include_embeddings: bool = Query(False),
    raw: bool = Query(False)
):
    if raw:
        return openai_collection_raw.query(
            query_embeddings=openai_embedding_function([request.text]),
            n_results=n_results,
            include=["metadatas", "documents", "distances"] + (["embeddings"] if include_embeddings else []),
        )
    return openai_collection_clean.query(
        query_embeddings=openai_embedding_function([request.text]),
        n_results=n_results,
        include=["metadatas", "documents", "distances"] + (["embeddings"] if include_embeddings else []),
    )
