# services/splitter_service.py
import logging
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.config import settings

logger = logging.getLogger(__name__)

class TextSplitterService:
    """텍스트를 청크로 분할하는 서비스"""

    def __init__(self):
        try:
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
            )
            logger.info(f"TextSplitterService initialized with chunk_size={settings.CHUNK_SIZE}, chunk_overlap={settings.CHUNK_OVERLAP}")
        except Exception as e:
            logger.critical(f"Failed to initialize RecursiveCharacterTextSplitter: {e}", exc_info=True)
            raise RuntimeError(f"Failed to initialize text splitter: {e}") from e


    def split_text(self, text: str) -> List[str]:
        """주어진 텍스트를 설정된 크기의 청크로 분할"""
        if not text:
            logger.warning("Attempted to split empty or None text.")
            return [] # Return empty list for empty input
        try:
            chunks = self.text_splitter.split_text(text)
            logger.info(f"Split text into {len(chunks)} chunks.")
            # Optional: Log first few chars of first chunk for debugging
            # if chunks: logger.debug(f"First chunk starts with: {chunks[0][:50]}...")
            return chunks
        except Exception as e:
            # Catch potential errors during splitting
            logger.error(f"Failed to split text: {str(e)}", exc_info=True)
            # Re-raise the exception to be handled upstream
            raise RuntimeError("Failed during text splitting") from e

# --- 팩토리 함수 추가 ---
splitter_service_instance = TextSplitterService()

def get_splitter_service() -> TextSplitterService:
    """FastAPI Depends를 위한 TextSplitterService 인스턴스 반환 함수"""
    if splitter_service_instance is None:
         raise RuntimeError("TextSplitterService failed to initialize.")
    return splitter_service_instance