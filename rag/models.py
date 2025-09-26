# rag/models.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

class SimilarityResult(BaseModel):
    # 유사도 검색 결과를 나타내는 모델
    title: str
    content: str
    authors: str
    published: Optional[datetime]
    doi: str
    similarity_score: float
    distance: float
    # chunk_index 필드 추가
    chunk_index: Optional[int] = None
    vector: Optional[List[float]] = None

class UploadResponse(BaseModel):
    # 파일 업로드 응답 모델
    filename: str
    message: str
    upload_timestamp: datetime

@dataclass
class ProcessedDocument:
    # 처리된 문서 정보를 담는 데이터 클래스
    title: str
    content: str
    authors: str
    published: Optional[datetime]
    doi: str
    embedding: List[float]

class SearchRequest(BaseModel):
    # 검색 요청 모델
    query_text: Optional[str] = None
    limit: int = 5
    similarity_threshold: float = 0.7