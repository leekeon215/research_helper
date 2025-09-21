# services/query_service.py
import httpx
import logging
import json
from typing import List, Dict, Any
from fastapi import HTTPException
from core.models import SearchRequest, FinalResponse
from core.config import settings
from services.llm_service import LLMService

logger = logging.getLogger(__name__)

class QueryService:
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self.llm_service = LLMService()

    async def process_internal_search(self, request: SearchRequest) -> FinalResponse:
        """
        내부 검색 파이프라인을 실행하고 최종 응답을 반환합니다.
        """
        try:
            response = await self.http_client.post(
                f"{settings.LOCAL_BACKEND_SERVER_URL}/search",
                json=request.model_dump()
            )
            response.raise_for_status()
            search_results = response.json()
            
            context = self._build_internal_context(search_results)
            llm_answer = await self.llm_service.get_final_response(context, request.query_text)

            references = [{
                "title": doc.get('title', ''),
            } for doc in search_results]

            return FinalResponse(query=request.query_text, answer=llm_answer, references=references)
        
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"내부 서버 오류: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"내부 검색 처리 중 오류 발생: {str(e)}")

    async def process_external_search(self, request: SearchRequest) -> FinalResponse:
        """
        외부 검색 파이프라인을 실행하고 최종 응답을 반환합니다.
        """
        try:
            expanded_query = await self.llm_service.expand_query(request.query_text)
            logger.info(f"원본 쿼리: '{request.query_text}' -> 확장된 쿼리: '{expanded_query}'")

            response = await self.http_client.post(
                f"{settings.SS_API_SERVER_URL}/search",
                json={"query_text": expanded_query, "limit": request.limit}
            )
            response.raise_for_status()
            search_results = response.json()
            
            context = self._build_external_context(search_results)
            logger.info(f"--- LLM 컨텍스트 시작 ---\n{context}\n--- LLM 컨텍스트 끝 ---")
            llm_answer = await self.llm_service.get_final_response(context, request.query_text)
            
            references = [{
                "title": paper.get('title', '제목 없음'),
                "id": paper.get('paperId', ''),
                "url": paper.get('openAccessPdf') or paper.get('url')
            } for paper in search_results]

            return FinalResponse(query=request.query_text, answer=llm_answer, references=references)
        
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"외부 서버 오류: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"외부 검색 처리 중 오류 발생: {str(e)}")

    def _build_internal_context(self, chunks: List[Dict[str, Any]]) -> str:
        """내부 검색 결과를 LLM 컨텍스트로 구성"""
        return "\n\n---\n\n".join([chunk.get("content", "") for chunk in chunks])

    def _build_external_context(self, papers: List[Dict[str, Any]]) -> str:
        """외부 논문 검색 결과를 LLM 컨텍스트로 구성"""
        context_parts = []
        for paper in papers:
            title = paper.get('title', '제목 없음')
            authors = ", ".join([author.get('name', '알 수 없음') for author in paper.get('authors', [])])
            year = paper.get('year', '알 수 없음')
            abstract = paper.get('abstract', '초록 없음')

            context_parts.append(f"제목: {title}\n저자: {authors}\n출판년도: {year}\n\n초록:\n{abstract}")
        
        return "\n\n---\n\n".join(context_parts)