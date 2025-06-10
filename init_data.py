# init_data.py
import argparse
import logging
from datetime import datetime, timezone
from langchain_community.document_loaders import ArxivLoader
from database import db_manager
from document_processor import document_processor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_sample_data(query: str, max_docs: int):
    # 사용자 정의 쿼리로 Weaviate 초기화
    try:
        db_manager.connect()
        db_manager.initialize_collection()
        
        logger.info(f"ArXiv에서 '{query}' 검색 시작...")
        loader = ArxivLoader(
            query=query,
            load_max_docs=max_docs,
            load_all_available_meta=True
        )
        docs = loader.load()
        
        logger.info(f"{len(docs)}개 논문 로드 완료")
        
        for i, doc in enumerate(docs):
            try:
                meta = doc.metadata
                authors = ", ".join(meta.get("Authors", [])) if isinstance(meta.get("Authors"), list) else meta.get("Authors")
                
                published = None
                if published_raw := meta.get("Published"):
                    try:
                        published = datetime.fromisoformat(published_raw).replace(tzinfo=timezone.utc)
                    except Exception as e:
                        logger.warning(f"날짜 파싱 오류: {str(e)}")
                
                doi = meta.get("entry_id", "").split("/")[-1]
                
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
        
        logger.info("✅ 데이터 로딩 완료!")
        
    except Exception as e:
        logger.error(f"❌ 데이터 로딩 실패: {str(e)}")
        raise
    finally:
        db_manager.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ArXiv 논문 데이터 수집기')
    parser.add_argument('--query', type=str, required=True, 
                    help='검색할 논문 주제 (예: "deep learning")')
    parser.add_argument('--max_docs', type=int, default=3,
                    help='로드할 최대 문서 수 (기본값: 3)')
    
    args = parser.parse_args()
    
    initialize_sample_data(args.query, args.max_docs)
