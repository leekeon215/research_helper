# file_handler.py
import uuid
from pathlib import Path
from typing import List
import logging
from fastapi import UploadFile, HTTPException
from config import Config
from models import SimilarityResult
from document_processor import document_processor
from similarity_search import similarity_searcher

logger = logging.getLogger(__name__)

class FileHandler:
    # 파일 업로드 및 처리를 담당하는 클래스
    
    def __init__(self):
        Config.ensure_upload_dir()
    
    def validate_file(self, file: UploadFile) -> None:
        # 업로드된 파일의 유효성 검사
        # 파일 확장자 검사
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in Config.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"지원하지 않는 파일 형식입니다. 허용된 형식: {', '.join(Config.ALLOWED_EXTENSIONS)}"
            )
        
        # 파일 크기 검사 (선택적 - UploadFile에서 size가 None일 수 있음)
        if hasattr(file, 'size') and file.size and file.size > Config.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"파일 크기가 너무 큽니다. 최대 크기: {Config.MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
    
    async def save_uploaded_file(self, file: UploadFile) -> Path:
        # 업로드된 파일을 서버에 저장
        try:
            # 고유한 파일명 생성
            file_extension = Path(file.filename).suffix
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = Config.UPLOAD_DIR / unique_filename
            
            # 파일 저장
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            logger.info(f"파일 저장 완료: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"파일 저장 실패: {str(e)}")
            raise HTTPException(status_code=500, detail="파일 저장 중 오류가 발생했습니다")
    
    async def process_uploaded_file(self, file: UploadFile) -> List[SimilarityResult]:
        # 업로드된 파일을 처리하고 유사도 검색 수행
        try:
            # 파일 유효성 검사
            self.validate_file(file)
            
            # 파일 저장
            file_path = await self.save_uploaded_file(file)
            
            try:
                # 업로드된 파일을 임베딩으로 변환
                file_vector = document_processor.process_uploaded_file_for_search(file_path)
                
                # 유사한 문서 검색
                similar_docs = similarity_searcher.search_similar_documents(
                    file_content_vector=file_vector,
                    limit=Config.DEFAULT_SEARCH_LIMIT
                )
                
                logger.info(f"파일 처리 완료: {file.filename}, {len(similar_docs)}개 유사 문서 발견")
                return similar_docs
                
            finally:
                # 임시 파일 정리
                if file_path.exists():
                    file_path.unlink()
                    logger.info(f"임시 파일 삭제: {file_path}")
                    
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"파일 처리 실패 {file.filename}: {str(e)}")
            raise HTTPException(status_code=500, detail="파일 처리 중 오류가 발생했습니다")
    
    def cleanup_old_files(self, max_age_hours: int = 24) -> None:
        # 오래된 업로드 파일들 정리
        try:
            import time
            current_time = time.time()
            
            for file_path in Config.UPLOAD_DIR.iterdir():
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > (max_age_hours * 3600):
                        file_path.unlink()
                        logger.info(f"오래된 파일 삭제: {file_path}")
                        
        except Exception as e:
            logger.error(f"파일 정리 실패: {str(e)}")

# 전역 파일 핸들러 인스턴스
file_handler = FileHandler()
