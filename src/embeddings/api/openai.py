from typing import List

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from fastapi import APIRouter, Query
from langchain_text_splitters import TokenTextSplitter

from embeddings.api.schema import EmbeddingRequest, SearchRequest
from embeddings.infrastructure.chroma_db_config import chroma_db_config
from embeddings.infrastructure.external_api_config import external_api_config

openai_router = APIRouter(
    prefix="/openai",
    tags=["openai"],
)

text_splitter = TokenTextSplitter.from_tiktoken_encoder(
    encoding_name=external_api_config.OPENAI_MODEL_ENCODER_NAME,
    model_name=external_api_config.OPENAI_MODEL_NAME,
    chunk_size=external_api_config.OPENAI_MODEL_MAX_INPUT,
    chunk_overlap=0
)

chroma_client = chromadb.HttpClient(host=chroma_db_config.HOST, port=chroma_db_config.PORT)

openai_embedding_function = OpenAIEmbeddingFunction(api_key=external_api_config.OPENAI_TOKEN, model_name=external_api_config.OPENAI_MODEL_NAME)
openai_collection = chroma_client.get_or_create_collection(name='openai_collection', embedding_function=openai_embedding_function)


@openai_router.post(
    "/embeddings",
)
async def save_embedding(
    request: List[EmbeddingRequest],
):
    new_entries = [
        (
            f"{item.id}_{idx}",
            chunk,
            {"source": item.source, "part_index": idx}
        )
        for item in request
        for idx, chunk in enumerate(text_splitter.split_text(item.text))
    ]

    new_ids, new_documents, new_metadatas = zip(*new_entries)

    openai_collection.add(
        ids=list(new_ids),
        documents=list(new_documents),
        metadatas=list(new_metadatas),
    )

    return {"message": "Embeddings saved"}


@openai_router.post(
    "/search",
)
async def search(
    request: SearchRequest,
    n_results: int = Query(3),
    include_embeddings: bool = Query(False),
):
    results = openai_collection.query(
        query_embeddings=openai_embedding_function([request.text]),
        n_results=n_results,
        include=["metadatas", "documents", "distances"] + (["embeddings"] if include_embeddings else []),
    )
    return results
