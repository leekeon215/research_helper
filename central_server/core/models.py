# core/models.py
from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query_text: str
    limit: int = 5
    similarity_threshold: float = 0.1

class FinalResponse(BaseModel):
    query: str
    answer: str
    references: List[dict]

class SemanticScholarPaper(BaseModel):
    title: str
    abstract: str
    authors: List[dict]
    year: int
    url: str
    openAccessPdf: Optional[str]