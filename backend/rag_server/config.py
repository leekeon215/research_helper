# config.py
import os
from pathlib import Path

class Config:
    # 시스템 전반의 설정을 관리하는 클래스
    
    # Weaviate 설정
    WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "localhost")
    WEAVIATE_PORT = int(os.getenv("WEAVIATE_PORT", 8080))
    WEAVIATE_GRPC_PORT = int(os.getenv("WEAVIATE_GRPC_PORT", 50051))
    
    # 임베딩 모델 설정
    EMBEDDING_MODEL_NAME = "allenai/specter"
    EMBEDDING_DEVICE = "cpu"
    NORMALIZE_EMBEDDINGS = True
    
    # 텍스트 분할 설정
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # 파일 업로드 설정
    UPLOAD_DIR = Path("uploads")
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx", ".md"}
    
    # 검색 설정
    DEFAULT_SEARCH_LIMIT = 5
    DEFAULT_SIMILARITY_THRESHOLD = 0.7
    
    # FastAPI 설정
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    @classmethod
    def ensure_upload_dir(cls):
        # 업로드 디렉토리가 존재하는지 확인하고 생성
        cls.UPLOAD_DIR.mkdir(exist_ok=True)
