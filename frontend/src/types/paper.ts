// 논문 및 저자 관련 타입 정의

export interface Paper {
  id: string;
  title: string;
  authors: Author[];
  publication_date?: string;
  venue?: string;
  citation_count?: number;
  abstract?: string;
  url?: string;
  tldr?: string;
  fields_of_study?: string[];
  type: 'paper' | 'author';
}

export interface Author {
  name: string;
  id?: string;
  affiliation?: string;
  publication_count?: number;
  citation_count?: number;
}

export interface PaperNode {
  id: string;
  type: 'paper' | 'author';
  data: Paper;
  position?: { x: number; y: number };
  locked?: boolean;
}

export interface PaperEdge {
  id: string;
  source: string;
  target: string;
  type: 'citation' | 'similarity';
  score: number;
}

export interface PaperGraph {
  nodes: PaperNode[];
  edges: PaperEdge[];
  seedNodeId?: string;
  query?: string;
  searchMode?: 'internal' | 'external';
}

export interface LibraryPaper extends Paper {
  uploaded_at: string;
  file_path?: string;
  is_seed?: boolean;
}


