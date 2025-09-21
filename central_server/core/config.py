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

settings = Settings()