from typing import List

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from cleantext import clean
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
openai_collection_raw = chroma_client.get_or_create_collection(name='openai_collection_raw', embedding_function=openai_embedding_function)
openai_collection_clean = chroma_client.get_or_create_collection(name='openai_collection_clean', embedding_function=openai_embedding_function)


@openai_router.post(
    "/embeddings",
)
async def save_embedding(
    request: List[EmbeddingRequest]
):
    new_raw_entries = []
    new_clean_entries = []

    for item in request:
        split_texts = text_splitter.split_text(item.text)
        for idx, chunk in enumerate(split_texts):
            cleaned_chunk = clean(
                chunk,
                fix_unicode=True,
                to_ascii=False,
                lower=True,
                normalize_whitespace=True,
                no_line_breaks=True,
                strip_lines=True,
                keep_two_line_breaks=False,
                no_urls=True,
                no_emails=True,
                no_phone_numbers=True,
                no_numbers=True,
                no_digits=True,
                no_currency_symbols=True,
                no_punct=True,
                no_emoji=True,
                replace_with_url="<URL>",
                replace_with_email="<EMAIL>",
                replace_with_phone_number="<PHONE>",
                replace_with_number="",
                replace_with_digit="",
                replace_with_currency_symbol="<CUR>",
                replace_with_punct="",
                lang="en",
            )

            print(cleaned_chunk)
            new_raw_entries.append((f"{item.id}_{idx}", chunk, {"source": item.source, "part_index": idx}))
            new_clean_entries.append((f"{item.id}_{idx}", cleaned_chunk, {"source": item.source, "part_index": idx}))

    raw_ids, raw_documents, raw_metadatas = zip(*new_raw_entries)
    clean_ids, clean_documents, clean_metadatas = zip(*new_clean_entries)

    openai_collection_raw.add(
        ids=list(raw_ids),
        documents=list(raw_documents),
        metadatas=list(raw_metadatas),
    )

    openai_collection_clean.add(
        ids=list(clean_ids),
        documents=list(clean_documents),
        metadatas=list(clean_metadatas),
    )

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
