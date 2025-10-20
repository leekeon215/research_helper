# services/loader_service.py
import logging
from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, UnstructuredWordDocumentLoader
)

logger = logging.getLogger(__name__)

class DocumentLoaderService:
    """파일 경로를 받아 내용을 텍스트로 로드하는 서비스"""

    def load_document(self, file_path: Path) -> str:
        """파일 확장자에 따라 적절한 로더를 사용하여 문서 내용을 로드"""
        file_extension = file_path.suffix.lower()
        logger.info(f"Loading document: {file_path.name} (type: {file_extension})")

        try:
            if file_extension == ".txt":
                # Ensure UTF-8 encoding is used
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif file_extension == ".pdf":
                # PyPDFLoader is generally recommended for better PDF handling
                loader = PyPDFLoader(str(file_path))
            elif file_extension in [".docx", ".doc"]:
                loader = UnstructuredWordDocumentLoader(str(file_path))
            # Consider adding .md support if needed
            # elif file_extension == ".md":
            #     loader = TextLoader(str(file_path), encoding='utf-8') # Or a specific Markdown loader
            else:
                # Raise a specific, informative error
                raise ValueError(f"Unsupported file type: {file_extension}. Allowed types: .txt, .pdf, .docx, .doc")

            docs = loader.load()
            # Ensure content is joined correctly and handle empty pages/docs
            content = "\n".join([doc.page_content for doc in docs if doc.page_content and isinstance(doc.page_content, str)]).strip()

            if not content:
                 logger.warning(f"No content extracted from {file_path.name}. The file might be empty or unreadable.")
                 # Decide whether to return empty string or raise an error for empty content
                 # return ""

            logger.info(f"Successfully loaded content from: {file_path.name}")
            return content

        except FileNotFoundError:
             logger.error(f"File not found: {file_path}")
             raise # Re-raise FileNotFoundError
        except ValueError as ve: # Catch specific ValueError for unsupported type
             logger.error(str(ve))
             raise # Re-raise ValueError
        except ImportError as ie:
             logger.error(f"Missing dependency for file type {file_extension}: {ie}. Please install required libraries.")
             # Consider raising HTTPException here if called from API context
             raise RuntimeError(f"Missing dependency for {file_extension}: {ie}") from ie
        except Exception as e:
            # Catch unexpected errors during loading
            logger.error(f"Failed to load document {file_path.name} due to unexpected error: {str(e)}", exc_info=True)
            # Re-raise a generic exception or a custom one
            raise RuntimeError(f"Failed to load document {file_path.name}") from e

# --- 팩토리 함수 추가 ---
def get_loader_service() -> DocumentLoaderService:
    """FastAPI Depends를 위한 DocumentLoaderService 인스턴스 반환 함수"""
    # Stateless, can be recreated or used as singleton
    return DocumentLoaderService()