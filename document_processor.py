# document_processor.py
from datetime import datetime, timezone
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader, PyPDFLoader, UnstructuredWordDocumentLoader
)
from typing import List, Dict, Any
import logging
from pathlib import Path
from config import Config
from embeddings import embedding_manager
from database import db_manager

logger = logging.getLogger(__name__)

class DocumentProcessor:
    # 문서 처리 및 Weaviate 저장을 담당하는 클래스
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len
        )
    
    def load_document(self, file_path: Path) -> str:
        # 파일 확장자에 따라 적절한 로더로 문서 로드
        file_extension = file_path.suffix.lower()
        
        try:
            if file_extension == ".txt":
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif file_extension == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif file_extension in [".docx", ".doc"]:
                loader = UnstructuredWordDocumentLoader(str(file_path))
            else:
                raise ValueError(f"지원하지 않는 파일 형식: {file_extension}")
            
            docs = loader.load()
            content = "\n".join([doc.page_content for doc in docs])
            logger.info(f"문서 로드 완료: {file_path.name}")
            return content
            
        except Exception as e:
            logger.error(f"문서 로드 실패 {file_path.name}: {str(e)}")
            raise
    
    def process_and_store_document(self, file_path: Path, metadata: Dict[str, Any] = None) -> List[str]:
        # 문서를 처리하고 Weaviate에 저장
        try:
            # 문서 로드
            content = self.load_document(file_path)
            
            # 텍스트 분할
            chunks = self.text_splitter.split_text(content)
            
            # 메타데이터 기본값 설정
            if metadata is None:
                metadata = {
                    "title": file_path.stem,
                    "authors": "Unknown",
                    "published": datetime.now(timezone.utc),
                    "doi": f"uploaded_{file_path.stem}"
                }
            
            # Weaviate 컬렉션 가져오기
            collection = db_manager.get_collection()
            
            stored_chunk_ids = []
            
            # 배치로 청크 저장
            with collection.batch.dynamic() as batch:
                for i, chunk in enumerate(chunks):
                    try:
                        # 임베딩 생성
                        embedding = embedding_manager.embed_text(chunk)
                        
                        # 데이터 객체 준비
                        data_object = {
                            "title": metadata.get("title", ""),
                            "content": chunk,
                            "authors": metadata.get("authors", ""),
                            "published": metadata.get("published"),
                            "doi": f"{metadata.get('doi', '')}_{i}"
                        }
                        
                        # 배치에 추가
                        result = batch.add_object(
                            properties=data_object,
                            vector=embedding
                        )
                        stored_chunk_ids.append(f"{metadata.get('doi', '')}_{i}")
                        
                    except Exception as e:
                        logger.error(f"청크 {i} 저장 실패: {str(e)}")
                        continue
            
            logger.info(f"문서 '{file_path.name}' 처리 완료: {len(stored_chunk_ids)}개 청크 저장")
            return stored_chunk_ids
            
        except Exception as e:
            logger.error(f"문서 처리 실패 {file_path.name}: {str(e)}")
            raise
    
    def process_raw_content(self, content: str, metadata: Dict[str, Any]) -> List[str]:
        # 임시 파일 없이 직접 콘텐츠 처리
        try:
            # 텍스트 분할
            chunks = self.text_splitter.split_text(content)
            
            # Weaviate 컬렉션 가져오기
            collection = db_manager.get_collection()
            
            stored_chunk_ids = []
            
            # 배치로 청크 저장
            with collection.batch.dynamic() as batch:
                for i, chunk in enumerate(chunks):
                    try:
                        # 임베딩 생성
                        embedding = embedding_manager.embed_text(chunk)
                        
                        # 데이터 객체 준비
                        data_object = {
                            "title": metadata.get("title", ""),
                            "content": chunk,
                            "authors": metadata.get("authors", ""),
                            "published": metadata.get("published"),
                            "doi": f"{metadata.get('doi', '')}_{i}"
                        }
                        
                        # 배치에 추가
                        result = batch.add_object(
                            properties=data_object,
                            vector=embedding
                        )
                        stored_chunk_ids.append(f"{metadata.get('doi', '')}_{i}")
                        
                    except Exception as e:
                        logger.error(f"청크 {i} 저장 실패: {str(e)}")
                        continue
            
            logger.info(f"문서 처리 완료: {len(stored_chunk_ids)}개 청크 저장")
            return stored_chunk_ids
            
        except Exception as e:
            logger.error(f"문서 처리 실패: {str(e)}")
            raise

    def process_uploaded_file_for_search(self, file_path: Path) -> List[float]:
        # 업로드된 파일을 검색용으로 처리 (임베딩만 생성)
        try:
            content = self.load_document(file_path)
            # 전체 내용을 하나의 임베딩으로 변환
            embedding = embedding_manager.embed_text(content)
            logger.info(f"검색용 파일 처리 완료: {file_path.name}")
            return embedding
        except Exception as e:
            logger.error(f"검색용 파일 처리 실패 {file_path.name}: {str(e)}")
            raise

# 전역 문서 프로세서 인스턴스
document_processor = DocumentProcessor()
