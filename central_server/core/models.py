# core/models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class InternalSearchRequest(BaseModel):
    query_text: str
    limit: int = 5
    similarity_threshold: float = 0.1

class ExternalSearchRequest(BaseModel):
    query_text: str
    limit: int = 5

class SimilarityLink(BaseModel):
    # 논문 간 유사도 관계(엣지)를 나타내는 모델
    source: str  # source paperId
    target: str  # target paperId
    similarity: float

# --- 내부 검색 전용 모델 ---

class ChunkReference(BaseModel):
    """검색된 개별 청크의 정보를 담는 모델"""
    chunk_content: str = Field(description="검색된 청크의 원문 내용")
    chunk_index: int = Field(description="문서 내 청크의 순서")
    similarity_score: float = Field(description="벡터 검색 유사도 점수")

class InternalDocumentReference(BaseModel):
    """그룹화된 내부 문서 참조 모델"""
    paper_id: str = Field(description="문서의 고유 ID (DOI)")
    title: str
    authors: Optional[List[str]] = None
    publication_date: Optional[str] = None
    # 각 문서에 속한 청크들의 목록
    chunks: List[ChunkReference]

class InternalSearchResponse(BaseModel):
    """내부 검색 API의 최종 응답 모델"""
    query: str
    answer: str
    references: List[InternalDocumentReference]
    similarity_graph: List[SimilarityLink]

# --- 외부 검색 전용 모델 ---

class ExternalReference(BaseModel):
    """외부 논문 검색 결과를 위한 Reference 모델"""
    paper_id: str = Field(description="Semantic Scholar의 논문 ID")
    title: str
    url: Optional[str] = None
    authors: Optional[List[str]] = None
    publication_date: Optional[str] = None
    tldr: Optional[str] = Field(None, description="AI 생성 한 줄 요약")
    citation_count: Optional[int] = Field(None, description="논문이 인용된 횟수")
    venue: Optional[str] = None
    fields_of_study: Optional[List[str]] = Field(None, description="논문이 속한 연구 분야")

class ExternalSearchResponse(BaseModel):
    """외부 검색 API의 최종 응답 모델"""
    query: str
    answer: str
    references: List[ExternalReference]
    similarity_graph: List[SimilarityLink]