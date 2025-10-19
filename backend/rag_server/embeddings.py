# embeddings.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List
import logging
from config import settings

logger = logging.getLogger(__name__)

class EmbeddingManager:
    # 임베딩 모델을 관리하는 클래스
    
    def __init__(self):
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self) -> None:
        # HuggingFace 임베딩 모델 초기화
        try:
            self.model = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL_NAME,
                model_kwargs={'device': settings.EMBEDDING_DEVICE},
                encode_kwargs={'normalize_embeddings': settings.NORMALIZE_EMBEDDINGS}
            )
            logger.info(f"임베딩 모델 '{settings.EMBEDDING_MODEL_NAME}' 초기화 완료")
        except Exception as e:
            logger.error(f"임베딩 모델 초기화 실패: {str(e)}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        # 텍스트를 벡터로 임베딩
        if not self.model:
            raise ValueError("임베딩 모델이 초기화되지 않았습니다")
        
        try:
            return self.model.embed_query(text)
        except Exception as e:
            logger.error(f"텍스트 임베딩 실패: {str(e)}")
            raise
    
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        # 여러 문서를 한번에 임베딩
        if not self.model:
            raise ValueError("임베딩 모델이 초기화되지 않았습니다")
        
        try:
            return self.model.embed_documents(documents)
        except Exception as e:
            logger.error(f"문서 임베딩 실패: {str(e)}")
            raise

# 전역 임베딩 매니저 인스턴스
embedding_manager_instance = EmbeddingManager()

# --- 팩토리 함수 추가 ---
def get_embedding_manager() -> EmbeddingManager:
    """FastAPI Depends를 위한 EmbeddingManager 인스턴스 반환 함수"""
    return embedding_manager_instance