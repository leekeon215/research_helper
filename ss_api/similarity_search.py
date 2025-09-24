# similarity_search.py
from typing import List, Dict, Any
import logging
import requests
from fastapi import HTTPException
from models import SemanticScholarResult, EmbeddingResult, TldrResult
from config import Config

logger = logging.getLogger(__name__)

class SimilaritySearcher:
    # 유사도 검색을 수행하는 클래스
    
    def _parse_paper_data(self, paper: Dict[str, Any]) -> SemanticScholarResult:
        """API 응답 딕셔너리를 SemanticScholarResult 모델로 변환하는 헬퍼 함수"""
        pdf_url = None
        if paper.get('openAccessPdf'):
            pdf_url = paper['openAccessPdf'].get('url')

        embedding_result = None
        if embedding_data := paper.get('embedding'):
            if isinstance(embedding_data, dict):
                embedding_result = EmbeddingResult(**embedding_data)

        tldr_result = None
        if tldr_data := paper.get('tldr'):
            if isinstance(tldr_data, dict):
                tldr_result = TldrResult(**tldr_data)

        return SemanticScholarResult(
            paperId=paper.get("paperId", ""),
            title=paper.get("title", ""),
            abstract=paper.get("abstract"),
            authors=paper.get("authors", []),
            year=paper.get("year"),
            url=paper.get("url", ""),
            openAccessPdf=pdf_url,
            embedding=embedding_result,
            tldr=tldr_result,
            citationCount=paper.get("citationCount"),
            venue=paper.get("venue"),
            fieldsOfStudy=paper.get("fieldsOfStudy")
        )

    def search_by_text_via_api(self, query_text: str, limit: int) -> List[SemanticScholarResult]:
        """
        Semantic Scholar API를 사용하여 텍스트 기반 논문 검색을 수행합니다.
        """
        api_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query_text,
            "limit": limit,
            "fields": "paperId,title,abstract,authors,year,url,openAccessPdf,embedding,tldr,citationCount,venue,fieldsOfStudy",
            "openAccessPdf": "",
            "publicationDateOrYear": "2022:",
            "sort": "publicationDate:desc",
        }

        headers = {}
        if Config.SEMANTIC_SCHOLAR_API_KEY:
            headers["x-api-key"] = Config.SEMANTIC_SCHOLAR_API_KEY
            logger.info("API Key를 사용하여 Semantic Scholar API에 요청합니다.")
        else:
            logger.warning("API Key가 설정되지 않았습니다. 기본 속도 제한이 적용됩니다.")

        try:
            response = requests.get(api_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json().get("data", [])
            
            if len(data) > limit:
                logger.warning(f"API가 {len(data)}개의 결과를 반환했습니다. {limit}개로 제한합니다.")
                data = data[:limit]

            results = [self._parse_paper_data(paper) for paper in data]
            
            logger.info(f"Semantic Scholar API 검색 완료: {len(results)}개 결과 반환")
            return results
            
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP 오류 발생: {err.response.status_code} - {err.response.text}")
            raise HTTPException(status_code=500, detail="Semantic Scholar API 호출 중 오류가 발생했습니다")
        except Exception as e:
            logger.error(f"API 검색 실패: {str(e)}")
            raise HTTPException(status_code=500, detail="검색 처리 중 오류가 발생했습니다")

    def get_recommendations_by_paper_id(self, paper_id: str, limit: int) -> List[SemanticScholarResult]:
        """
        Semantic Scholar Recommendations API를 사용해 특정 논문 기반 추천 논문 리스트 조회
        """
        api_url = f"https://api.semanticscholar.org/recommendations/v1/papers/forpaper/{paper_id}"
        params = {
            "fields": "paperId,title,abstract,authors,year,url,openAccessPdf",
            "limit": limit
        }
        headers = {}
        if Config.SEMANTIC_SCHOLAR_API_KEY:
            headers["x-api-key"] = Config.SEMANTIC_SCHOLAR_API_KEY
            logger.info("API Key를 사용하여 추천 논문 요청을 보냅니다.")
        else:
            logger.warning("API Key가 설정되지 않았습니다. 기본 속도 제한이 적용됩니다.")

        try:
            response = requests.get(api_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json().get("recommendedPapers", [])

            results = [self._parse_paper_data(paper) for paper in data]

            logger.info(f"추천 논문 검색 완료: {len(results)}개 결과")
            return results
            
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP 오류 발생: {err.response.status_code} - {err.response.text}")
            raise HTTPException(status_code=500, detail="Semantic Scholar Recommendations API 호출 중 오류가 발생했습니다")
        except Exception as e:
            logger.error(f"API 추천 검색 실패: {str(e)}")
            raise HTTPException(status_code=500, detail="추천 논문 처리 중 오류가 발생했습니다")

# 전역 검색기 인스턴스
similarity_searcher = SimilaritySearcher()