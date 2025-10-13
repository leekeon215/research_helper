// API 명세서 기반 타입 정의

// ==================== 외부 검색 관련 ====================
export interface ExternalSearchRequest {
  query_text: string;
  limit?: number;
}

export interface ExternalReference {
  paper_id: string;
  title: string;
  url?: string;
  authors?: string[];
  publication_date?: string;
  tldr?: string;
  citation_count?: number;
  venue?: string;
  fields_of_study?: string[];
}

export interface SimilarityLink {
  source: string;
  target: string;
  score: number;
  type: 'citation' | 'similarity';
}

export interface ExternalSearchResponse {
  query: string;
  answer: string;
  references: ExternalReference[];
  similarity_graph: SimilarityLink[];
}

// ==================== 내부 검색 관련 ====================
export interface InternalSearchRequest {
  query_text: string;
  limit?: number;
  similarity_threshold?: number;
}

export interface ChunkReference {
  chunk_content: string;
  chunk_index: number;
  similarity_score: number;
}

export interface InternalDocumentReference {
  paper_id: string;
  title: string;
  authors?: string[];
  publication_date?: string;
  chunks: ChunkReference[];
}

export interface InternalSearchResponse {
  query: string;
  answer: string;
  references: InternalDocumentReference[];
  similarity_graph: SimilarityLink[];
}

// ==================== 파일 업로드 관련 ====================
export interface UploadResponse {
  filename: string;
  message: string;
  upload_timestamp: string;
}

// ==================== Semantic Scholar API 관련 ====================
export interface SearchRequest {
  query_text?: string;
  limit?: number;
}

export interface Author {
  name: string;
  authorId?: string;
}

export interface EmbeddingResult {
  model: string;
  vector: number[];
}

export interface TldrResult {
  model: string;
  text: string;
}

export interface SemanticScholarResult {
  paperId: string;
  title: string;
  abstract?: string;
  authors: Author[];
  publicationDate?: string;
  openAccessPdf?: string;
  embedding?: EmbeddingResult;
  tldr?: TldrResult;
  citationCount?: number;
  venue?: string;
  fieldsOfStudy?: string[];
}


