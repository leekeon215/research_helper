# rag/similarity_search.py
from typing import List, Optional
import logging
# 필요한 필터 클래스 import 추가
from weaviate.classes.query import Filter, MetadataQuery

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

    # --- 제목으로 검색 ---
    def search_by_title(self, title_query: str, limit: int = None) -> List[SimilarityResult]:
        """
        논문 제목에 특정 키워드가 포함된 문서를 검색합니다. (부분 일치)
        """
        if limit is None:
            limit = Config.DEFAULT_SEARCH_LIMIT

        try:
            collection = db_manager.get_collection()

            # 'title' 속성에 대해 필터링 수행 (Like 연산자 사용)
            response = collection.query.fetch_objects(
                limit=limit,
                filters=Filter.by_property("title").like(f"*{title_query}*"), # 부분 일치 검색
                return_properties=["title", "content", "authors", "published", "doi", "chunk_index"],
                include_vector=True # 벡터값도 반환
            )

            results = []
            for obj in response.objects:
                # 필터 검색 결과에는 distance/similarity가 없으므로 기본값 또는 None 처리
                result = SimilarityResult(
                    title=obj.properties.get("title", ""),
                    content=obj.properties.get("content", ""),
                    authors=obj.properties.get("authors", ""),
                    published=obj.properties.get("published"),
                    doi=obj.properties.get("doi", ""),
                    similarity_score=0.0, # 필터 검색이므로 유사도 점수는 0 또는 None
                    distance=1.0,         # 필터 검색이므로 거리는 최대값 또는 None
                    vector=obj.vector.get("default") if obj.vector else None,
                    chunk_index=obj.properties.get("chunk_index")
                )
                results.append(result)

            logger.info(f"제목 검색 완료 ('{title_query}'): {len(results)}개 결과 반환")
            return results

        except Exception as e:
            logger.error(f"제목 검색 실패: {str(e)}")
            raise

    # --- 저자명으로 검색 ---
    def search_by_authors(self, author_query: str, limit: int = None) -> List[SimilarityResult]:
        """
        저자명에 특정 키워드가 포함된 문서를 검색합니다. (부분 일치)
        """
        if limit is None:
            limit = Config.DEFAULT_SEARCH_LIMIT

        try:
            collection = db_manager.get_collection()

            # 'authors' 속성에 대해 필터링 수행 (Like 연산자 사용)
            response = collection.query.fetch_objects(
                limit=limit,
                filters=Filter.by_property("authors").like(f"*{author_query}*"), # 부분 일치 검색
                return_properties=["title", "content", "authors", "published", "doi", "chunk_index"],
                include_vector=True # 벡터값도 반환
            )

            results = []
            for obj in response.objects:
                result = SimilarityResult(
                    title=obj.properties.get("title", ""),
                    content=obj.properties.get("content", ""),
                    authors=obj.properties.get("authors", ""),
                    published=obj.properties.get("published"),
                    doi=obj.properties.get("doi", ""),
                    similarity_score=0.0,
                    distance=1.0,
                    vector=obj.vector.get("default") if obj.vector else None,
                    chunk_index=obj.properties.get("chunk_index")
                )
                results.append(result)

            logger.info(f"저자 검색 완료 ('{author_query}'): {len(results)}개 결과 반환")
            return results

        except Exception as e:
            logger.error(f"저자 검색 실패: {str(e)}")
            raise

    def get_all_documents(self, limit: Optional[int] = None) -> List[SimilarityResult]:
        """
        Weaviate DB에 저장된 모든 문서(청크) 데이터를 조회합니다.
        limit 파라미터로 가져올 최대 개수를 지정할 수 있습니다. (기본값: 제한 없음)
        """
        results = []
        try:
            collection = db_manager.get_collection()

            response = collection.query.fetch_objects(
                limit=limit, # None이면 모든 객체
                return_properties=["title", "content", "authors", "published", "doi", "chunk_index"],
                include_vector=True # 벡터값도 포함
            )

            for obj in response.objects:
                result = SimilarityResult(
                    title=obj.properties.get("title", ""),
                    content=obj.properties.get("content", ""),
                    authors=obj.properties.get("authors", ""),
                    published=obj.properties.get("published"),
                    doi=obj.properties.get("doi", ""),
                    similarity_score=0.0, # 전체 조회이므로 유사도/거리 의미 없음
                    distance=1.0,
                    vector=obj.vector.get("default") if obj.vector else None,
                    chunk_index=obj.properties.get("chunk_index")
                )
                results.append(result)

            logger.info(f"모든 문서 조회 완료: 총 {len(results)}개 결과 반환 (limit: {limit})")
            return results

        except Exception as e:
            logger.error(f"모든 문서 조회 실패: {str(e)}")
            raise
    
# 전역 검색기 인스턴스
similarity_searcher = SimilaritySearcher()