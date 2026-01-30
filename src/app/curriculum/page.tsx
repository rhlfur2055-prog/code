'use client';

import Link from 'next/link';
import { ArrowRight } from 'lucide-react';
import curriculum from '@/data/curriculum.json';
import { CATEGORIES, LEVELS, TAGS } from '@/types';
import { ProgressBar } from '@/components/ProgressBar';
import { useProgress } from '@/hooks/useProgress';

export default function CurriculumPage() {
  const { getTotalProgress } = useProgress();
  const progress = getTotalProgress(curriculum.meta.totalContents);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">📚 전체 커리큘럼</h1>
        <p className="text-gray-400 mt-1">
          {curriculum.meta.totalContents}개 콘텐츠 | 16개 카테고리 | 40일 완성
        </p>
      </div>

      {/* 전체 진행률 */}
      <div className="card">
        <div className="flex items-center justify-between mb-2">
          <span className="font-bold">전체 진행률</span>
          <span className="text-primary font-bold">{progress.percentage}%</span>
        </div>
        <ProgressBar percentage={progress.percentage} size="lg" />
        <p className="text-sm text-gray-400 mt-2">
          {progress.completed} / {progress.total} 완료
        </p>
      </div>

      {/* 난이도 & 태그 가이드 */}
      <div className="grid md:grid-cols-2 gap-4">
        <div className="card">
          <h3 className="font-bold mb-3">🎯 난이도 시스템</h3>
          <div className="space-y-2">
            {Object.entries(LEVELS).map(([key, level]) => (
              <div key={key} className="flex items-center gap-2 text-sm">
                <span className={`level level-${key} px-2 py-1 rounded`}>
                  {level.emoji} {level.label}
                </span>
                <span className="text-gray-400">{level.description}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="card">
          <h3 className="font-bold mb-3">🏷️ 태그 시스템</h3>
          <div className="space-y-2">
            {Object.entries(TAGS).map(([key, tag]) => (
              <div key={key} className="flex items-center gap-2 text-sm">
                <span className={`tag tag-${key} px-2 py-1 rounded-full`}>
                  {tag.emoji} {tag.label}
                </span>
                <span className="text-gray-400">{tag.description}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 카테고리 목록 */}
      <div className="space-y-4">
        <h2 className="text-xl font-bold">📂 카테고리별 학습</h2>
        {CATEGORIES.map((cat) => (
          <Link
            key={cat.id}
            href={`/study/${cat.name}`}
            className="card flex items-center gap-4 hover:border-primary/50 transition group"
          >
            <div className="w-14 h-14 rounded-xl flex items-center justify-center text-3xl"
              style={{ backgroundColor: `${cat.color}20` }}
            >
              {cat.icon}
            </div>
            <div className="flex-1">
              <h3 className="font-bold group-hover:text-primary transition">
                {cat.nameKo}
              </h3>
              <p className="text-sm text-gray-400">{cat.description}</p>
              <div className="text-xs text-gray-500 mt-1">
                Day {cat.days[0]}-{cat.days[cat.days.length - 1]} | {cat.contentCount}개 콘텐츠
              </div>
            </div>
            <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-primary transition" />
          </Link>
        ))}
      </div>
    </div>
  );
}
