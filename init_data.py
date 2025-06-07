# init_data.py
from datetime import datetime, timezone
import logging
from langchain_community.document_loaders import ArxivLoader
from database import db_manager
from document_processor import document_processor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_sample_data():
    # 샘플 논문 데이터로 Weaviate 초기화
    try:
        # Weaviate 연결
        db_manager.connect()
        
        # 컬렉션 초기화
        db_manager.initialize_collection()
        
        # ArXiv에서 샘플 논문 로드
        logger.info("ArXiv에서 샘플 논문 로딩 시작...")
        loader = ArxivLoader(
            query="deep learning",
            load_max_docs=3,
            load_all_available_meta=True
        )
        docs = loader.load()
        
        logger.info(f"{len(docs)}개 논문 로드 완료")
        
        # 각 논문 처리 및 저장
        for i, doc in enumerate(docs):
            try:
                meta = doc.metadata
                
                # authors 필드 처리
                authors_raw = meta.get("Authors", "")
                authors = ", ".join(authors_raw) if isinstance(authors_raw, list) else authors_raw
                
                # published 필드 처리
                published = None
                if published_raw := meta.get("Published"):
                    try:
                        published = datetime.fromisoformat(published_raw).replace(tzinfo=timezone.utc)
                    except Exception as e:
                        logger.warning(f"날짜 파싱 오류: {str(e)}")
                
                # doi 처리
                doi = meta.get("entry_id", "").split("/")[-1]
                
                # 메타데이터 구성
                metadata = {
                    "title": meta.get("Title", ""),
                    "authors": authors,
                    "published": published,
                    "doi": doi
                }
                
                # 직접 콘텐츠 처리
                document_processor.process_raw_content(
                    content=doc.page_content,
                    metadata=metadata
                )
                logger.info(f"논문 {i+1}/{len(docs)} 처리 완료: {metadata['title'][:50]}...")
                        
            except Exception as e:
                logger.error(f"논문 {i+1} 처리 실패: {str(e)}")
                continue
        
        logger.info("✅ 초기 데이터 로딩 완료!")
        
    except Exception as e:
        logger.error(f"❌ 초기 데이터 로딩 실패: {str(e)}")
        raise
    finally:
        db_manager.close()

if __name__ == "__main__":
    initialize_sample_data()
