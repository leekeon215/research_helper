# core/models.py
from pydantic import BaseModel, Field
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
    authors: Optional[List[str]] = None
    publicationDate: Optional[str] = None
    tldr: Optional[str] = Field(None, description="Too Long; Didn't Read one-line summary")
    citation_count: Optional[int] = Field(None, alias="citationCount")
    venue: Optional[str] = None
    fields_of_study: Optional[List[str]] = Field(None, alias="fieldsOfStudy")

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
    similarity_graph: List[SimilarityLink]