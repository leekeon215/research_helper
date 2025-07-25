# database.py
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from typing import Optional
import logging
from config import Config

logger = logging.getLogger(__name__)

class WeaviateManager:
    # Weaviate 데이터베이스 연결 및 관리 클래스
    
    def __init__(self):
        self.client: Optional[weaviate.WeaviateClient] = None
        self.collection_name = "ResearchPaper"
    
    def connect(self) -> weaviate.WeaviateClient:
        # Weaviate 클라이언트에 연결
        try:
            self.client = weaviate.connect_to_local(
                host=Config.WEAVIATE_HOST,
                port=Config.WEAVIATE_PORT,
                grpc_port=Config.WEAVIATE_GRPC_PORT
            )
            logger.info("Weaviate 연결 성공")
            return self.client
        except Exception as e:
            logger.error(f"Weaviate 연결 실패: {str(e)}")
            raise
    
    def initialize_collection(self) -> None:
        # 연구 논문 컬렉션 초기화
        if not self.client:
            raise ValueError("Weaviate 클라이언트가 연결되지 않았습니다")
        
        try:
            # 기존 컬렉션이 있으면 삭제
            if self.client.collections.exists(self.collection_name):
                self.client.collections.delete(self.collection_name)
                logger.info(f"기존 '{self.collection_name}' 컬렉션 삭제됨")
            
            # 새 컬렉션 생성
            self.client.collections.create(
                name=self.collection_name,
                vectorizer_config=Configure.Vectorizer.none(),
                properties=[
                    Property(name="title", data_type=DataType.TEXT),
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="authors", data_type=DataType.TEXT),
                    Property(name="published", data_type=DataType.DATE),
                    Property(name="doi", data_type=DataType.TEXT)
                ]
            )
            logger.info(f"'{self.collection_name}' 컬렉션 생성 완료")
            
        except Exception as e:
            logger.error(f"컬렉션 초기화 실패: {str(e)}")
            raise

    def get_collection(self):
        # 컬렉션 객체 반환
        if not self.client:
            raise ValueError("Weaviate 클라이언트가 연결되지 않았습니다")
        return self.client.collections.get(self.collection_name)
    
    def close(self) -> None:
        # 클라이언트 연결 종료
        if self.client:
            self.client.close()
            logger.info("Weaviate 연결 종료")

# 전역 데이터베이스 매니저 인스턴스
db_manager = WeaviateManager()
