# models.py
from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    # 검색 요청 모델
    query_text: Optional[str] = None
    limit: int = 5

class EmbeddingResult(BaseModel):
    # 논문 임베딩 결과를 나타내는 모델
    model: str
    vector: List[float]

class SemanticScholarResult(BaseModel):
    # Semantic Scholar API 검색 결과를 나타내는 모델
    paperId: str
    title: str
    abstract: Optional[str]
    authors: List[dict]
    year: Optional[int]
    url: str
    openAccessPdf: Optional[str]
    embedding: Optional[EmbeddingResult]