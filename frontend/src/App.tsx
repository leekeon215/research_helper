// src/App.tsx

import { useState, useEffect } from 'react';
import MainLayout from './components/layout/MainLayout';
import HomePage from './pages/HomePage';
import VisualizationPage from './pages/VisualizationPage';
import LibraryPage from './pages/LibraryPage';
import { LibraryService } from './services/libraryService';
import { ThemeProvider, useTheme } from './context/ThemeContext';
import type { VisualizationState, VisualizationView } from './types/visualization';
import type { SearchMode } from './types/search';
import type { LibraryPaper } from './types/paper';

// App 컴포넌트를 테마 컨텍스트로 감싸기
const AppContent: React.FC = () => {
  const { searchMode, setSearchMode } = useTheme();
  const [currentPage, setCurrentPage] = useState<'home' | 'visualization' | 'library'>('home');
  const [isLoading, setIsLoading] = useState(false);
  const [libraryPapers, setLibraryPapers] = useState<LibraryPaper[]>([]);
  const [visualizationState, setVisualizationState] = useState<VisualizationState>({
    currentViewIndex: 0,
    views: [],
    maxViews: 20
  });

  // 라이브러리 데이터 로드
  useEffect(() => {
    setLibraryPapers(LibraryService.getLibraryPapers());
  }, []);

  // 검색 실행
  const handleSearch = async (query: string, mode: SearchMode, selectedSeedPaper?: string) => {
    setIsLoading(true);
    
    try {
      // Mock 데이터 사용 - 실제 API 연동 시 교체 예정
      // const result = await searchService.externalSearch(query, mode, selectedSeedPaper);
      
      // 임시 Mock 데이터로 첫 번째 시각화 화면 생성 (더 많은 노드)
      const mockViewId = `view-${Date.now()}`;
      const mockView: VisualizationView = {
        id: mockViewId,
        title: query,
        graph: {
          nodes: [
            {
              id: 'paper-1',
              type: 'paper',
              data: {
                id: 'paper-1',
                title: query,
                authors: [{ name: 'Dr. Alice Johnson', affiliation: 'Stanford University' }, { name: 'Prof. Bob Smith', affiliation: 'MIT' }],
                type: 'paper',
                publication_date: '2024-01-15',
                venue: 'Nature Machine Intelligence',
                citation_count: 127,
                abstract: 'This paper presents a novel approach to machine learning that combines deep neural networks with traditional statistical methods. Our approach achieves state-of-the-art results on multiple benchmark datasets.',
                tldr: 'Novel ML approach combining deep learning with statistics for improved performance.',
                fields_of_study: ['Machine Learning', 'Artificial Intelligence', 'Statistics']
              },
              position: { x: 400, y: 300 },
              locked: false
            },
            {
              id: 'paper-2',
              type: 'paper',
              data: {
                id: 'paper-2',
                title: 'Deep Learning in Computer Vision: A Comprehensive Survey',
                authors: [{ name: 'Dr. Carol Davis', affiliation: 'Google Research' }, { name: 'Dr. David Wilson', affiliation: 'Facebook AI' }],
                type: 'paper',
                publication_date: '2023-11-20',
                venue: 'IEEE Transactions on Pattern Analysis',
                citation_count: 89,
                abstract: 'A comprehensive survey of deep learning applications in computer vision, covering recent advances in convolutional neural networks, attention mechanisms, and transformer architectures.',
                tldr: 'Comprehensive survey of deep learning in computer vision applications.',
                fields_of_study: ['Computer Vision', 'Deep Learning', 'Neural Networks']
              },
              position: { x: 600, y: 250 },
              locked: false
            },
            {
              id: 'paper-3',
              type: 'paper',
              data: {
                id: 'paper-3',
                title: 'Natural Language Processing with Transformers: Recent Advances',
                authors: [{ name: 'Prof. Emma Brown', affiliation: 'OpenAI' }, { name: 'Dr. Frank Miller', affiliation: 'Anthropic' }],
                type: 'paper',
                publication_date: '2024-02-10',
                venue: 'Journal of Machine Learning Research',
                citation_count: 156,
                abstract: 'This paper reviews recent advances in transformer-based natural language processing, including GPT models, BERT variants, and multimodal transformers.',
                tldr: 'Review of transformer advances in NLP including GPT and BERT models.',
                fields_of_study: ['Natural Language Processing', 'Transformers', 'Large Language Models']
              },
              position: { x: 300, y: 500 },
              locked: false
            },
            {
              id: 'paper-4',
              type: 'paper',
              data: {
                id: 'paper-4',
                title: 'Reinforcement Learning for Autonomous Systems',
                authors: [{ name: 'Dr. Grace Lee', affiliation: 'Tesla AI' }, { name: 'Prof. Henry Chen', affiliation: 'Waymo' }],
                type: 'paper',
                publication_date: '2023-12-05',
                venue: 'Neural Information Processing Systems',
                citation_count: 203,
                abstract: 'We present a novel reinforcement learning framework for autonomous vehicle control, demonstrating improved safety and efficiency in complex traffic scenarios.',
                tldr: 'RL framework for autonomous vehicle control with improved safety.',
                fields_of_study: ['Reinforcement Learning', 'Autonomous Systems', 'Robotics']
              },
              position: { x: 700, y: 400 },
              locked: false
            },
            {
              id: 'paper-5',
              type: 'paper',
              data: {
                id: 'paper-5',
                title: 'Federated Learning: Privacy-Preserving Machine Learning',
                authors: [{ name: 'Dr. Ivy Rodriguez', affiliation: 'Apple' }, { name: 'Dr. Jack Taylor', affiliation: 'Microsoft Research' }],
                type: 'paper',
                publication_date: '2024-01-30',
                venue: 'ACM Computing Surveys',
                citation_count: 94,
                abstract: 'This survey examines federated learning approaches that enable machine learning model training while preserving user privacy through decentralized computation.',
                tldr: 'Survey of privacy-preserving ML through federated learning.',
                fields_of_study: ['Federated Learning', 'Privacy', 'Distributed Computing']
              },
              position: { x: 300, y: 200 },
              locked: false
            }
          ],
          edges: [
            {
              id: 'edge-1',
              source: 'paper-1',
              target: 'paper-2',
              type: 'similarity',
              score: 0.85
            },
            {
              id: 'edge-2',
              source: 'paper-1',
              target: 'paper-3',
              type: 'citation',
              score: 0.92
            },
            {
              id: 'edge-3',
              source: 'paper-1',
              target: 'paper-4',
              type: 'similarity',
              score: 0.78
            },
            {
              id: 'edge-4',
              source: 'paper-1',
              target: 'paper-5',
              type: 'citation',
              score: 0.88
            },
            {
              id: 'edge-5',
              source: 'paper-2',
              target: 'paper-3',
              type: 'similarity',
              score: 0.76
            },
            {
              id: 'edge-6',
              source: 'paper-3',
              target: 'paper-4',
              type: 'citation',
              score: 0.81
            }
          ],
          seedNodeId: selectedSeedPaper || 'paper-1',
          query: query,
          searchMode: mode
        },
        createdAt: new Date().toISOString(),
        breadcrumbPath: [
          {
            id: 'home',
            title: '홈',
            timestamp: new Date().toISOString()
          },
          {
            id: mockViewId,
            title: query,
            query: query,
            timestamp: new Date().toISOString()
          }
        ]
      };

      setVisualizationState({
        currentViewIndex: 0,
        views: [mockView],
        maxViews: 20
      });
      
      setCurrentPage('visualization');
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // 노드 클릭 처리
  const handleNodeClick = async (nodeId: string) => {
    setIsLoading(true);
    
    try {
      // Mock 데이터 사용 - 실제 API 연동 시 교체 예정
      // const result = await searchService.expandNode(nodeId);
      
      // 임시 Mock 데이터로 새로운 시각화 화면 생성
      const currentView = visualizationState.views[visualizationState.currentViewIndex];
      const clickedNode = currentView.graph.nodes.find((node: any) => node.id === nodeId);
      
      if (!clickedNode) return;
      
      const timestamp = Date.now();
      const newViewId = `view-${timestamp}`;
      const newView: VisualizationView = {
        id: newViewId,
        title: clickedNode.data.title,
        graph: {
          nodes: [
            {
              id: nodeId,
              type: 'paper',
              data: clickedNode.data,
              position: { x: 400, y: 300 },
              locked: false
            },
            {
              id: `paper-${timestamp}-1`,
              type: 'paper',
              data: {
                id: `paper-${timestamp}-1`,
                title: `Advanced Applications of ${clickedNode.data.title.split(':')[0]}`,
                authors: [{ name: 'Dr. Sarah Kim', affiliation: 'DeepMind' }, { name: 'Prof. Michael Wang', affiliation: 'UC Berkeley' }],
                type: 'paper',
                publication_date: '2024-03-15',
                venue: 'International Conference on Machine Learning',
                citation_count: 67,
                abstract: `Building upon the foundation of ${clickedNode.data.title}, this work explores advanced applications and novel methodologies that extend the original framework to solve real-world problems.`,
                tldr: `Advanced applications extending ${clickedNode.data.title.split(':')[0]} methodology.`,
                fields_of_study: [...(clickedNode.data.fields_of_study || ['Machine Learning']), 'Applications']
              },
              position: { x: 600, y: 200 },
              locked: false
            },
            {
              id: `paper-${timestamp}-2`,
              type: 'paper',
              data: {
                id: `paper-${timestamp}-2`,
                title: `Comparative Analysis: ${clickedNode.data.title.split(':')[0]} vs Traditional Methods`,
                authors: [{ name: 'Dr. Lisa Chen', affiliation: 'Meta AI' }, { name: 'Dr. Robert Garcia', affiliation: 'Amazon Science' }],
                type: 'paper',
                publication_date: '2024-02-28',
                venue: 'IEEE Transactions on Neural Networks',
                citation_count: 89,
                abstract: `This paper provides a comprehensive comparative analysis between ${clickedNode.data.title.split(':')[0]} and traditional machine learning approaches, highlighting advantages and limitations.`,
                tldr: `Comparative analysis of ${clickedNode.data.title.split(':')[0]} vs traditional ML methods.`,
                fields_of_study: [...(clickedNode.data.fields_of_study || ['Machine Learning']), 'Comparative Analysis']
              },
              position: { x: 200, y: 400 },
              locked: false
            },
            {
              id: `paper-${timestamp}-3`,
              type: 'paper',
              data: {
                id: `paper-${timestamp}-3`,
                title: `Optimization Techniques for ${clickedNode.data.title.split(':')[0]} Models`,
                authors: [{ name: 'Dr. Amanda White', affiliation: 'NVIDIA Research' }, { name: 'Prof. Carlos Martinez', affiliation: 'Carnegie Mellon' }],
                type: 'paper',
                publication_date: '2024-01-20',
                venue: 'Journal of Optimization Theory and Applications',
                citation_count: 45,
                abstract: `We introduce novel optimization techniques specifically designed for ${clickedNode.data.title.split(':')[0]} models, achieving significant improvements in training efficiency and model performance.`,
                tldr: `Novel optimization techniques for ${clickedNode.data.title.split(':')[0]} models.`,
                fields_of_study: [...(clickedNode.data.fields_of_study || ['Machine Learning']), 'Optimization']
              },
              position: { x: 700, y: 350 },
              locked: false
            },
            {
              id: `paper-${timestamp}-4`,
              type: 'paper',
              data: {
                id: `paper-${timestamp}-4`,
                title: `Real-World Deployment of ${clickedNode.data.title.split(':')[0]} Systems`,
                authors: [{ name: 'Dr. Jennifer Liu', affiliation: 'Google Cloud' }, { name: 'Dr. Thomas Anderson', affiliation: 'Microsoft Azure' }],
                type: 'paper',
                publication_date: '2024-03-01',
                venue: 'ACM Transactions on Intelligent Systems',
                citation_count: 112,
                abstract: `This paper discusses the challenges and solutions encountered when deploying ${clickedNode.data.title.split(':')[0]} systems in production environments, including scalability and reliability considerations.`,
                tldr: `Production deployment challenges and solutions for ${clickedNode.data.title.split(':')[0]} systems.`,
                fields_of_study: [...(clickedNode.data.fields_of_study || ['Machine Learning']), 'Production Systems', 'Deployment']
              },
              position: { x: 300, y: 500 },
              locked: false
            },
            {
              id: `paper-${timestamp}-5`,
              type: 'paper',
              data: {
                id: `paper-${timestamp}-5`,
                title: `Ethical Considerations in ${clickedNode.data.title.split(':')[0]} Development`,
                authors: [{ name: 'Dr. Maria Rodriguez', affiliation: 'AI Ethics Institute' }, { name: 'Prof. James Thompson', affiliation: 'MIT CSAIL' }],
                type: 'paper',
                publication_date: '2024-02-10',
                venue: 'Nature Machine Intelligence',
                citation_count: 78,
                abstract: `As ${clickedNode.data.title.split(':')[0]} technologies become more prevalent, understanding their ethical implications becomes crucial. This work examines bias, fairness, and transparency issues.`,
                tldr: `Ethical implications and considerations in ${clickedNode.data.title.split(':')[0]} development.`,
                fields_of_study: [...(clickedNode.data.fields_of_study || ['Machine Learning']), 'AI Ethics', 'Fairness']
              },
              position: { x: 550, y: 450 },
              locked: false
            }
          ],
          edges: [
            {
              id: `edge-${timestamp}-1`,
              source: nodeId,
              target: `paper-${timestamp}-1`,
              type: 'similarity',
              score: 0.92
            },
            {
              id: `edge-${timestamp}-2`,
              source: nodeId,
              target: `paper-${timestamp}-2`,
              type: 'citation',
              score: 0.88
            },
            {
              id: `edge-${timestamp}-3`,
              source: nodeId,
              target: `paper-${timestamp}-3`,
              type: 'similarity',
              score: 0.85
            },
            {
              id: `edge-${timestamp}-4`,
              source: nodeId,
              target: `paper-${timestamp}-4`,
              type: 'citation',
              score: 0.90
            },
            {
              id: `edge-${timestamp}-5`,
              source: nodeId,
              target: `paper-${timestamp}-5`,
              type: 'similarity',
              score: 0.82
            },
            {
              id: `edge-${timestamp}-6`,
              source: `paper-${timestamp}-1`,
              target: `paper-${timestamp}-3`,
              type: 'citation',
              score: 0.76
            },
            {
              id: `edge-${timestamp}-7`,
              source: `paper-${timestamp}-2`,
              target: `paper-${timestamp}-4`,
              type: 'similarity',
              score: 0.81
            },
            {
              id: `edge-${timestamp}-8`,
              source: `paper-${timestamp}-3`,
              target: `paper-${timestamp}-5`,
              type: 'citation',
              score: 0.74
            }
          ],
          seedNodeId: nodeId,
          query: `Related to: ${clickedNode.data.title}`,
          searchMode: currentView.graph.searchMode
        },
        createdAt: new Date().toISOString(),
        breadcrumbPath: [
          ...currentView.breadcrumbPath,
          {
            id: newViewId,
            title: clickedNode.data.title,
            timestamp: new Date().toISOString()
          }
        ]
      };

      // 새로운 뷰를 현재 뷰 다음에 추가 (최대 20개 제한)
      const newViews = [...visualizationState.views];
      const insertIndex = visualizationState.currentViewIndex + 1;
      
      // 최대 뷰 수 제한
      if (newViews.length >= visualizationState.maxViews) {
        // 가장 오래된 뷰 제거
        newViews.shift();
      }
      
      newViews.splice(insertIndex, 0, newView);
      
      setVisualizationState({
        ...visualizationState,
        views: newViews,
        currentViewIndex: insertIndex
      });
      
    } catch (error) {
      console.error('Node expansion failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // 브레드크럼 네비게이션
  const handleNavigateToView = (breadcrumbIndex: number) => {
    // 브레드크럼 인덱스를 뷰 인덱스로 변환
    // breadcrumbIndex 0 = 홈 (뷰 없음), breadcrumbIndex 1 = 뷰 인덱스 0
    const viewIndex = breadcrumbIndex - 1;
    
    if (viewIndex < 0) {
      // 홈으로 돌아가기 - 시각화 상태 완전 초기화
      setCurrentPage('home');
      setVisualizationState({
        currentViewIndex: 0,
        views: [],
        maxViews: 20
      });
      return;
    }
    
    setVisualizationState(prev => ({
      ...prev,
      currentViewIndex: viewIndex,
      // 이후 경로들 제거 (클릭한 뷰까지 포함)
      views: prev.views.slice(0, viewIndex + 1)
    }));
  };

  // 검색 모드 변경
  const handleModeChange = (mode: SearchMode) => {
    setSearchMode(mode);
  };

  // 라이브러리 페이지로 이동
  const handleOpenLibrary = () => {
    setCurrentPage('library');
  };

  // 현재 페이지 렌더링
  const renderCurrentPage = () => {
    if (currentPage === 'home') {
      return (
        <HomePage
          onSearch={handleSearch}
          libraryPapers={libraryPapers}
          isLoading={isLoading}
          currentMode={searchMode}
          onModeChange={handleModeChange}
        />
      );
    }
    
    if (currentPage === 'library') {
      return (
        <LibraryPage
          onPaperSelect={() => setCurrentPage('home')}
          onClose={() => setCurrentPage('home')}
        />
      );
    }
    
    return (
      <VisualizationPage
        views={visualizationState.views}
        currentViewIndex={visualizationState.currentViewIndex}
        onNodeClick={handleNodeClick}
        onNavigateToView={handleNavigateToView}
      />
    );
  };

  return (
    <MainLayout
      visualizationState={visualizationState}
      onNavigateToView={handleNavigateToView}
      onOpenLibrary={handleOpenLibrary}
      showSidebar={currentPage === 'visualization'}
    >
      {renderCurrentPage()}
    </MainLayout>
  );
};

// 메인 App 컴포넌트
function App() {
  return (
    <ThemeProvider initialMode="external">
      <AppContent />
    </ThemeProvider>
  );
}

export default App;