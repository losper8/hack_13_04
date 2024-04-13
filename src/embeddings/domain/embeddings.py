import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from cleantext import clean
from langchain_text_splitters import TokenTextSplitter

from embeddings.infrastructure.chroma_db_config import chroma_db_config
from embeddings.infrastructure.external_api_config import external_api_config

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


async def domain_save_embeddings(request):
    new_raw_entries = []
    new_clean_entries = []

    for item in request:
        full_text_clean = clean(
            item.text,
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
            replace_with_url="<ссылка>",
            replace_with_email="<почта>",
            replace_with_phone_number="<телефон>",
            replace_with_number="",
            replace_with_digit="",
            replace_with_currency_symbol="<валюта>",
            replace_with_punct="",
            lang="en",
        )

        raw_splits = text_splitter.split_text(item.text)
        clean_splits = text_splitter.split_text(full_text_clean)

        for idx, raw_chunk in enumerate(raw_splits):
            new_raw_entries.append((f"{item.id}_{idx}", raw_chunk, {"source": item.source, "part_index": idx}))

        for idx, cleaned_chunk in enumerate(clean_splits):
            new_clean_entries.append((f"{item.id}_{idx}", cleaned_chunk, {"source": item.source, "part_index": idx}))

    raw_ids, raw_documents, raw_metadatas = zip(*new_raw_entries) if new_raw_entries else ([], [], [])
    clean_ids, clean_documents, clean_metadatas = zip(*new_clean_entries) if new_clean_entries else ([], [], [])

    if new_raw_entries:
        openai_collection_raw.add(
            ids=list(raw_ids),
            documents=list(raw_documents),
            metadatas=list(raw_metadatas),
        )
    if new_clean_entries:
        openai_collection_clean.add(
            ids=list(clean_ids),
            documents=list(clean_documents),
            metadatas=list(clean_metadatas),
        )

    print("Embeddings saved for both raw and cleaned texts.")
