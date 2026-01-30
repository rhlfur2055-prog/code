'use client';

import Link from 'next/link';
import { ArrowLeft, Clock, BookOpen } from 'lucide-react';
import { useParams } from 'next/navigation';
import { CATEGORIES } from '@/types';
import contentsData from '@/data/contents.json';
import { ProgressButton } from '@/components/ProgressButton';
import { BookmarkButton } from '@/components/BookmarkButton';
import { ProgressBar } from '@/components/ProgressBar';
import { useProgress } from '@/hooks/useProgress';

// 타입 정보
const TYPE_INFO: Record<string, { emoji: string; label: string }> = {
  theory: { emoji: '📚', label: '이론' },
  practice: { emoji: '🛠️', label: '실습' },
  quiz: { emoji: '✅', label: '퀴즈' },
  interview: { emoji: '💼', label: '면접' },
};

const TAG_INFO: Record<string, { emoji: string; color: string }> = {
  required: { emoji: '🔥', color: 'tag-required' },
  interview: { emoji: '💼', color: 'tag-interview' },
  practical: { emoji: '🛠️', color: 'tag-practical' },
  coding: { emoji: '📝', color: 'tag-coding' },
};

export default function CategoryPage() {
  const params = useParams();
  const category = params.category as string;
  const { getCategoryProgress, isCompleted } = useProgress();
  
  const categoryInfo = CATEGORIES.find(c => c.name === category);
  const contents = contentsData.contents.filter(c => c.category === category);
  
  // 서브카테고리별로 그룹화
  const grouped = contents.reduce((acc, content) => {
    if (!acc[content.subcategory]) {
      acc[content.subcategory] = [];
    }
    acc[content.subcategory].push(content);
    return acc;
  }, {} as Record<string, typeof contents>);

  const contentIds = contents.map(c => c.id);
  const progress = getCategoryProgress(contentIds);

  if (!categoryInfo) {
    return (
      <div className="text-center py-20">
        <h1 className="text-2xl font-bold mb-4">카테고리를 찾을 수 없습니다</h1>
        <Link href="/" className="text-primary hover:underline">홈으로 돌아가기</Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* 헤더 */}
      <div className="flex items-center gap-4">
        <Link href="/" className="p-2 rounded-lg hover:bg-dark-border transition">
          <ArrowLeft className="w-5 h-5" />
        </Link>
        <div className="flex-1">
          <div className="flex items-center gap-3">
            <span className="text-4xl">{categoryInfo.icon}</span>
            <div>
              <h1 className="text-2xl font-bold">{categoryInfo.nameKo}</h1>
              <p className="text-gray-400">{categoryInfo.description}</p>
            </div>
          </div>
        </div>
      </div>

      {/* 진행률 */}
      <div className="card">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-400">학습 진행률</span>
          <span className="text-sm text-primary font-bold">
            {progress.completed} / {progress.total} 완료 ({progress.percentage}%)
          </span>
        </div>
        <ProgressBar percentage={progress.percentage} size="md" />
        <p className="text-xs text-gray-500 mt-2">
          Day {categoryInfo.days[0]} ~ Day {categoryInfo.days[categoryInfo.days.length - 1]}
        </p>
      </div>

      {/* 콘텐츠 목록 (서브카테고리별) */}
      {Object.entries(grouped).sort().map(([subcategory, items]) => (
        <div key={subcategory} className="space-y-3">
          <h2 className="text-lg font-bold text-gray-300 flex items-center gap-2">
            <span className="text-primary">📁</span>
            {subcategory}
            <span className="text-sm text-gray-500">({items.length})</span>
          </h2>
          
          <div className="space-y-2">
            {items.map((content) => {
              const completed = isCompleted(content.id);
              const typeInfo = TYPE_INFO[content.type] || TYPE_INFO.theory;
              
              return (
                <div
                  key={content.id}
                  className={`card flex items-center gap-4 hover:border-primary/50 transition relative ${
                    completed ? 'border-primary/30 bg-primary/5' : ''
                  }`}
                >
                  <div className="relative z-10">
                    <ProgressButton contentId={content.id} size="sm" />
                  </div>
                  
                  <Link
                    href={`/study/${category}/${content.slug}`}
                    className="flex-1 min-w-0"
                  >
                    <span className="absolute inset-0 z-0" />
                    <div className="flex items-center gap-2">
                      <span className="text-sm">{typeInfo.emoji}</span>
                      <h3 className={`font-medium truncate ${completed ? 'text-gray-400' : ''}`}>
                        {content.title}
                      </h3>
                    </div>
                    <div className="flex items-center gap-2 mt-1">
                      {content.tags.map(tag => {
                        const info = TAG_INFO[tag];
                        return info ? (
                          <span key={tag} className={`tag ${info.color} text-xs`}>
                            {info.emoji}
                          </span>
                        ) : null;
                      })}
                      <span className="text-xs text-gray-500 flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {content.time}
                      </span>
                    </div>
                  </Link>
                  
                  <div className="relative z-10">
                    <BookmarkButton contentId={content.id} size="sm" />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}
