from pydantic import BaseModel


class EmbeddingRequest(BaseModel):
    id: str
    text: str
    source: str


class SearchRequest(BaseModel):
    text: str
