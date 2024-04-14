from io import BytesIO
from zipfile import is_zipfile, ZipFile

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from embeddings.api.schema import EmbeddingRequest
from embeddings.domain.embeddings import domain_save_embeddings

files_router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@files_router.post("/upload-zip")
async def upload_zip(
    file: UploadFile = File(...),
):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="File is not a ZIP archive")

    try:
        content = await file.read()
        zip_file = BytesIO(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

    if not is_zipfile(zip_file):
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid ZIP archive")

    embedding_requests = []
    try:
        with ZipFile(zip_file, 'r') as z:
            txt_files = [f for f in z.namelist() if f.endswith('.txt') and f.count('/') >= 2 and '__MACOSX' not in f]


            for file_path in txt_files:
                parent_directory = file_path.strip('/').split('/')[-2]

                with z.open(file_path, 'r') as file:
                    print(f"Processing file: {file_path}")
                    data = file.read().decode('utf-8')

                embedding_request = EmbeddingRequest(
                    id=file_path,
                    text=data,
                    source=parent_directory
                )
                embedding_requests.append(embedding_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process ZIP archive: {str(e)}")

    await domain_save_embeddings(embedding_requests)
