import React, { useState, useEffect } from 'react';
import { LibraryService } from '../services/libraryService';
import type { LibraryPaper } from '../types/paper';

interface LibraryPageProps {
  onPaperSelect?: (paper: LibraryPaper) => void;
  onClose?: () => void;
}

const LibraryPage: React.FC<LibraryPageProps> = ({
  onPaperSelect,
  onClose
}) => {
  const [papers, setPapers] = useState<LibraryPaper[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  // 라이브러리 데이터 로드
  useEffect(() => {
    setPapers(LibraryService.getLibraryPapers());
  }, []);

  // 검색 필터링
  const filteredPapers = searchQuery 
    ? LibraryService.searchPapers(searchQuery)
    : papers;

  // 파일 업로드 처리
  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setUploadError(null);

    try {
      // Mock 파일 업로드 - 실제 API 연동 시 교체 예정
      // const uploadResult = await uploadService.uploadFile(file);
      
      // 임시 Mock 데이터 생성
      const mockPaper: Omit<LibraryPaper, 'id' | 'uploaded_at'> = {
        title: file.name.replace(/\.[^/.]+$/, ''), // 확장자 제거
        authors: [{ name: 'Unknown Author' }],
        type: 'paper',
        publication_date: new Date().toISOString().split('T')[0],
        venue: 'Uploaded Document',
        abstract: 'This is an uploaded document. Abstract will be extracted automatically.',
        fields_of_study: ['Computer Science'],
        file_path: file.name,
        is_seed: false
      };

      LibraryService.addPaper(mockPaper);
      setPapers(LibraryService.getLibraryPapers());
      
      // 파일 입력 초기화
      event.target.value = '';
    } catch (error) {
      setUploadError(error instanceof Error ? error.message : 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  // 논문 삭제
  const handleDeletePaper = (paperId: string) => {
    if (LibraryService.removePaper(paperId)) {
      setPapers(LibraryService.getLibraryPapers());
    }
  };

  // 논문 선택
  const handlePaperClick = (paper: LibraryPaper) => {
    onPaperSelect?.(paper);
  };

  const stats = LibraryService.getLibraryStats();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 헤더 */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">라이브러리</h1>
            <p className="text-gray-600 mt-1">
              {stats.totalPapers}개 논문 • {stats.totalAuthors}명 저자
            </p>
          </div>
          <div className="flex items-center space-x-4">
            {onClose && (
              <button
                onClick={onClose}
                className="px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors"
              >
                닫기
              </button>
            )}
            <button
              onClick={() => document.getElementById('file-upload')?.click()}
              disabled={isUploading}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isUploading ? '업로드 중...' : '논문 추가'}
            </button>
          </div>
        </div>

        {/* 파일 업로드 (숨김) */}
        <input
          id="file-upload"
          type="file"
          accept=".pdf,.txt,.docx"
          onChange={handleFileUpload}
          className="hidden"
        />

        {/* 검색바 */}
        <div className="mt-4">
          <div className="relative">
            <input
              type="text"
              placeholder="논문 제목, 저자, 초록으로 검색..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <svg className="w-5 h-5 text-gray-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        {/* 에러 메시지 */}
        {uploadError && (
          <div className="mt-3 p-3 bg-red-100 border border-red-300 text-red-700 rounded-lg">
            {uploadError}
          </div>
        )}
      </div>

      {/* 통계 카드 */}
      {stats.totalPapers > 0 && (
        <div className="px-6 py-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <h3 className="text-sm font-medium text-gray-500 mb-1">전체 논문</h3>
              <p className="text-2xl font-bold text-gray-900">{stats.totalPapers}</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <h3 className="text-sm font-medium text-gray-500 mb-1">저자 수</h3>
              <p className="text-2xl font-bold text-gray-900">{stats.totalAuthors}</p>
            </div>
            <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
              <h3 className="text-sm font-medium text-gray-500 mb-1">연구 분야</h3>
              <p className="text-2xl font-bold text-gray-900">{stats.uniqueFields.length}</p>
            </div>
          </div>
        </div>
      )}

      {/* 논문 목록 */}
      <div className="px-6 pb-6">
        {filteredPapers.length === 0 ? (
          <div className="text-center py-12">
            <svg className="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {searchQuery ? '검색 결과가 없습니다' : '논문이 없습니다'}
            </h3>
            <p className="text-gray-500 mb-4">
              {searchQuery 
                ? '다른 검색어를 시도해보세요'
                : '첫 번째 논문을 업로드해보세요'
              }
            </p>
            {!searchQuery && (
              <button
                onClick={() => document.getElementById('file-upload')?.click()}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                논문 업로드
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {filteredPapers.map((paper) => (
              <button
                key={paper.id}
                className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer w-full text-left"
                onClick={() => handlePaperClick(paper)}
              >
                <div className="p-6">
                  {/* 논문 제목 */}
                  <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                    {paper.title}
                  </h3>

                  {/* 저자 */}
                  <div className="mb-3">
                    <p className="text-sm text-gray-600">
                      {paper.authors.map(author => author.name).join(', ')}
                    </p>
                  </div>

                  {/* 메타데이터 */}
                  <div className="space-y-1 mb-3">
                    {paper.publication_date && (
                      <p className="text-xs text-gray-500">
                        📅 {paper.publication_date}
                      </p>
                    )}
                    {paper.venue && (
                      <p className="text-xs text-gray-500">
                        📚 {paper.venue}
                      </p>
                    )}
                    {paper.citation_count && (
                      <p className="text-xs text-gray-500">
                        📊 {paper.citation_count.toLocaleString()} 인용
                      </p>
                    )}
                  </div>

                  {/* 초록 미리보기 */}
                  {paper.abstract && (
                    <p className="text-sm text-gray-700 line-clamp-3 mb-3">
                      {paper.abstract}
                    </p>
                  )}

                  {/* 연구 분야 */}
                  {paper.fields_of_study && paper.fields_of_study.length > 0 && (
                    <div className="flex flex-wrap gap-1 mb-3">
                      {paper.fields_of_study.slice(0, 3).map((field) => (
                        <span key={field} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                          {field}
                        </span>
                      ))}
                      {paper.fields_of_study.length > 3 && (
                        <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded">
                          +{paper.fields_of_study.length - 3}
                        </span>
                      )}
                    </div>
                  )}

                  {/* 업로드 정보 */}
                  <div className="flex items-center justify-between text-xs text-gray-500 pt-3 border-t border-gray-100">
                    <span>업로드: {new Date(paper.uploaded_at).toLocaleDateString()}</span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeletePaper(paper.id);
                      }}
                      className="text-red-500 hover:text-red-700 transition-colors"
                    >
                      삭제
                    </button>
                  </div>
                </div>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default LibraryPage;


