# rag/similarity_search.py
from typing import List
import logging
from models import SimilarityResult
from database import db_manager
from embeddings import embedding_manager
from config import Config

logger = logging.getLogger(__name__)

class SimilaritySearcher:
    # 유사도 검색을 수행하는 클래스
    
    def search_by_vector(self, query_vector: List[float], limit: int = None, distance_threshold: float = None) -> List[SimilarityResult]:
        # 벡터를 이용한 유사도 검색
        if limit is None:
            limit = Config.DEFAULT_SEARCH_LIMIT
        if distance_threshold is None:
            distance_threshold = 1.0 - Config.DEFAULT_SIMILARITY_THRESHOLD
        
        try:
            collection = db_manager.get_collection()
            
            # near_vector 검색 수행 (벡터값 반환 옵션 추가)
            response = collection.query.near_vector(
                near_vector=query_vector,
                limit=limit,
                distance=distance_threshold,
                return_metadata=["distance"],
                include_vector=True  # 벡터값 반환
            )
            
            results = []
            for obj in response.objects:
                # 거리를 유사도로 변환 (거리가 작을수록 유사도가 높음)
                distance = obj.metadata.distance if obj.metadata.distance is not None else 1.0
                similarity_score = 1.0 - distance
                
                result = SimilarityResult(
                    title=obj.properties.get("title", ""),
                    content=obj.properties.get("content", ""),
                    authors=obj.properties.get("authors", ""),
                    published=obj.properties.get("published"),
                    doi=obj.properties.get("doi", ""),
                    similarity_score=similarity_score,
                    distance=distance,
                    vector=obj.vector.get("default") if obj.vector else None, # 벡터값 할당
                    chunk_index=obj.properties.get("chunk_index")
                )
                results.append(result)
            
            logger.info(f"벡터 검색 완료: {len(results)}개 결과 반환")
            return results
            
        except Exception as e:
            logger.error(f"벡터 검색 실패: {str(e)}")
            raise
    
    def search_by_text(self, query_text: str, limit: int = None, distance_threshold: float = None) -> List[SimilarityResult]:
        # 텍스트를 이용한 유사도 검색
        try:
            # 텍스트를 벡터로 변환
            text_to_embed = f"user's question [SEP] {query_text}"
            query_vector = embedding_manager.embed_text(text_to_embed)
            
            # 벡터 검색 수행
            return self.search_by_vector(query_vector, limit, distance_threshold)
            
        except Exception as e:
            logger.error(f"텍스트 검색 실패: {str(e)}")
            raise
    
# 전역 검색기 인스턴스
similarity_searcher = SimilaritySearcher()