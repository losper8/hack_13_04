import chromadb

chroma_client = chromadb.HttpClient(host="https://climbing-fox-open.ngrok-free.app", port=443)

openai_collection_raw = chroma_client.get_or_create_collection(name='openai_collection_raw_big')