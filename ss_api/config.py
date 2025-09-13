# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 시스템 전반의 설정을 관리하는 클래스
    
    # 검색 설정
    DEFAULT_SEARCH_LIMIT = 5
    DEFAULT_SIMILARITY_THRESHOLD = 0.7
    
    # FastAPI 설정
    API_HOST = "0.0.0.0"
    API_PORT = 8001
    
    # Semantic Scholar API 키
    SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")