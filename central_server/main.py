# main.py
from fastapi import FastAPI, HTTPException
import logging
from typing import List, Dict, Any

from core.config import settings
from core.models import InternalSearchRequest, ExternalSearchRequest, FinalResponse
from services.query_service import QueryService

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Central Processing Server",
    description="중앙에서 검색 및 LLM 처리를 담당하는 서버",
    version="1.0.0"
)

# 의존성 주입을 위한 서비스 인스턴스
query_service = QueryService()

@app.get("/")
async def root():
    return {"message": "중앙 처리 서버가 실행 중입니다."}

@app.post("/search/internal", response_model=FinalResponse)
async def search_internal_data(request: InternalSearchRequest):
    """
    내부 백엔드 서버를 통해 검색을 수행하고 LLM 답변을 반환합니다.
    """
    try:
        logger.info(f"내부 검색 요청 수신: {request.query_text}")
        response = await query_service.process_internal_search(request)
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"내부 검색 처리 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="내부 검색 처리 중 오류가 발생했습니다.")

@app.post("/search/external", response_model=FinalResponse)
async def search_external_data(request: ExternalSearchRequest):
    """
    Semantic Scholar API 서버를 통해 검색을 수행하고 LLM 답변을 반환합니다.
    """
    try:
        logger.info(f"외부 검색 요청 수신: {request.query_text}")
        response = await query_service.process_external_search(request)
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"외부 검색 처리 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="외부 검색 처리 중 오류가 발생했습니다.")