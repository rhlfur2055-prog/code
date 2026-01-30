'use client';

import Link from 'next/link';
import { ArrowRight, Clock, CheckCircle } from 'lucide-react';
import curriculum from '@/data/curriculum.json';
import { CATEGORIES, ROADMAP } from '@/types';
import { useProgress } from '@/hooks/useProgress';

export default function RoadmapPage() {
  const { getTotalProgress } = useProgress();
  const progress = getTotalProgress(curriculum.meta.totalContents);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">🗓️ 40일 로드맵</h1>
          <p className="text-gray-400 mt-1">
            하루 평균 {curriculum.meta.avgContentsPerDay}개 | 총 {curriculum.meta.totalContents}개 콘텐츠
          </p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-primary">{progress.percentage}%</div>
          <div className="text-sm text-gray-400">완료</div>
        </div>
      </div>

      <div className="grid gap-4">
        {ROADMAP.map((day, index) => {
          const category = CATEGORIES.find(c => c.name === day.categories[0]);
          const isWeekend = index > 0 && (index) % 7 === 0;
          
          return (
            <div key={day.day}>
              {isWeekend && (
                <div className="text-center py-2 text-sm text-gray-500 border-t border-dark-border mt-4">
                  🎉 Week {Math.floor(index / 7)} 완료!
                </div>
              )}
              <div className="card hover:border-primary/50 transition">
                <div className="flex items-center gap-4">
                  <div className="w-16 h-16 rounded-xl bg-primary/20 flex items-center justify-center shrink-0">
                    <span className="text-2xl font-bold text-primary">D{day.day}</span>
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-2xl">{category?.icon}</span>
                      <h2 className="text-lg font-bold truncate">{day.title}</h2>
                    </div>
                    <div className="flex items-center gap-3 text-sm text-gray-400">
                      <span className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {day.hours}시간
                      </span>
                      <span>{category?.nameKo}</span>
                    </div>
                  </div>

                  <Link
                    href={`/study/${day.categories[0]}`}
                    className="btn btn-outline shrink-0 flex items-center gap-1"
                  >
                    학습하기 <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="card bg-gradient-to-r from-primary/20 to-purple-500/20 border-primary/30 text-center py-8">
        <div className="text-4xl mb-2">🎓</div>
        <h2 className="text-2xl font-bold mb-2">40일 완주 축하드립니다!</h2>
        <p className="text-gray-400">풀스택 개발자로서의 첫걸음을 떼셨습니다!</p>
      </div>
    </div>
  );
}
