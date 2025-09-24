# core/models.py
from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query_text: str
    limit: int = 5
    similarity_threshold: float = 0.1

class Reference(BaseModel):
    # 개별 논문 정보를 담는 모델
    paperId: str
    title: str
    url: Optional[str] = None

class SimilarityLink(BaseModel):
    # 논문 간 유사도 관계(엣지)를 나타내는 모델
    source: str  # source paperId
    target: str  # target paperId
    similarity: float

class FinalResponse(BaseModel):
    # 최종 응답 모델
    query: str
    answer: str
    references: List[Reference]
    # 유사도 그래프 정보 추가
    similarity_graph: List[SimilarityLink]

class SemanticScholarPaper(BaseModel):
    title: str
    abstract: str
    authors: List[dict]
    year: int
    url: str
    openAccessPdf: Optional[str]