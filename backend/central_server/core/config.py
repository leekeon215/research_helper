# core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # 하위 서버 URL 설정
    LOCAL_BACKEND_SERVER_URL: str = os.getenv("LOCAL_BACKEND_SERVER_URL", "http://localhost:8001")
    SS_API_SERVER_URL: str = os.getenv("SS_API_SERVER_URL", "http://localhost:8002")
    
    # LLM API 키
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    # Central Server 포트 설정
    CENTRAL_SERVER_PORT: int = int(os.getenv("CENTRAL_SERVER_PORT", "8000"))
    CENTRAL_SERVER_HOST: str = os.getenv("CENTRAL_SERVER_HOST", "0.0.0.0")

settings = Settings()
