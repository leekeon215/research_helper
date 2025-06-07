# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
from typing import List
from contextlib import asynccontextmanager

from config import Config
from models import UploadResponse, SimilarityResult, SearchRequest
from database import db_manager
from file_handler import file_handler
from similarity_search import similarity_searcher

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션 시작/종료 시 실행되는 함수
    # 시작 시
    try:
        db_manager.connect()
        logger.info("FastAPI 애플리케이션 시작됨")
        yield
    finally:
        # 종료 시
        db_manager.close()
        logger.info("FastAPI 애플리케이션 종료됨")

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="RAG 파일 유사도 검색 시스템",
    description="업로드된 파일과 유사한 문서를 검색하는 RAG 시스템",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    # 루트 엔드포인트
    return {"message": "RAG 파일 유사도 검색 시스템이 실행 중입니다"}

@app.get("/health")
async def health_check():
    # 서비스 상태 확인
    try:
        # Weaviate 연결 확인
        collection = db_manager.get_collection()
        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "weaviate_connected": True
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"서비스 상태 불량: {str(e)}")

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    # 파일 업로드 및 유사도 검색
    try:
        logger.info(f"파일 업로드 요청: {file.filename}")
        
        # 파일 처리 및 유사도 검색
        similar_documents = await file_handler.process_uploaded_file(file)
        
        # 응답 생성
        response = UploadResponse(
            filename=file.filename,
            message=f"파일 '{file.filename}' 처리 완료",
            similar_documents=similar_documents,
            total_found=len(similar_documents),
            upload_timestamp=datetime.now()
        )
        
        logger.info(f"파일 업로드 완료: {file.filename}, {len(similar_documents)}개 유사 문서")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"파일 업로드 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="파일 업로드 처리 중 오류가 발생했습니다")

@app.post("/search", response_model=List[SimilarityResult])
async def search_documents(request: SearchRequest):
    # 텍스트 기반 문서 검색
    try:
        if not request.query_text:
            raise HTTPException(status_code=400, detail="검색할 텍스트를 입력해주세요")
        
        logger.info(f"텍스트 검색 요청: {request.query_text[:50]}...")
        
        # 유사도 검색 수행
        results = similarity_searcher.search_by_text(
            query_text=request.query_text,
            limit=request.limit,
            distance_threshold=1.0 - request.similarity_threshold
        )
        
        logger.info(f"텍스트 검색 완료: {len(results)}개 결과")
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"텍스트 검색 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="검색 처리 중 오류가 발생했습니다")

@app.get("/stats")
async def get_stats():
    # 시스템 통계 정보
    try:
        collection = db_manager.get_collection()
        
        # 저장된 문서 수 조회
        result = collection.aggregate.over_all(total_count=True)
        document_count = result.total_count if result.total_count else 0
        
        return {
            "total_documents": document_count,
            "system_status": "running",
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"통계 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="통계 조회 중 오류가 발생했습니다")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT)
