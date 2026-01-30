'use client';

import Link from 'next/link';
import { ArrowRight, BookOpen, Clock, Trophy, Zap } from 'lucide-react';
import { CATEGORIES, ROADMAP } from '@/types';
import { useProgress } from '@/hooks/useProgress';
import { ProgressBar } from '@/components/ProgressBar';

const TOTAL_CONTENTS = 760;

export default function HomePage() {
  const { getTotalProgress } = useProgress();
  const totalProgress = getTotalProgress(TOTAL_CONTENTS);

  return (
    <div className="space-y-8">
      {/* 히어로 섹션 */}
      <section className="card bg-gradient-to-br from-primary/20 to-dark-card border-primary/30">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold mb-2">🚀 40일 완성 풀스택 부트캠프</h1>
            <p className="text-gray-400 text-lg">{TOTAL_CONTENTS}개 콘텐츠 | 16개 카테고리 | 하루 평균 19개</p>
          </div>
          <div className="flex gap-3">
            <Link href="/roadmap" className="btn btn-primary flex items-center gap-2">
              시작하기 <ArrowRight className="w-4 h-4" />
            </Link>
            <Link href="/curriculum" className="btn btn-outline">커리큘럼 보기</Link>
          </div>
        </div>
        <div className="mt-6 pt-6 border-t border-dark-border">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-400">전체 진행률</span>
            <span className="text-sm text-primary font-bold">
              {totalProgress.completed} / {totalProgress.total} 완료 ({totalProgress.percentage}%)
            </span>
          </div>
          <ProgressBar percentage={totalProgress.percentage} size="lg" />
        </div>
      </section>

      {/* 통계 */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="card flex items-center gap-3">
          <div className="p-3 rounded-lg bg-primary/20"><BookOpen className="w-6 h-6 text-primary" /></div>
          <div><div className="text-2xl font-bold">{TOTAL_CONTENTS}</div><div className="text-sm text-gray-400">총 콘텐츠</div></div>
        </div>
        <div className="card flex items-center gap-3">
          <div className="p-3 rounded-lg bg-yellow-500/20"><Clock className="w-6 h-6 text-yellow-400" /></div>
          <div><div className="text-2xl font-bold">40일</div><div className="text-sm text-gray-400">완성 기간</div></div>
        </div>
        <div className="card flex items-center gap-3">
          <div className="p-3 rounded-lg bg-purple-500/20"><Zap className="w-6 h-6 text-purple-400" /></div>
          <div><div className="text-2xl font-bold">16개</div><div className="text-sm text-gray-400">카테고리</div></div>
        </div>
        <div className="card flex items-center gap-3">
          <div className="p-3 rounded-lg bg-green-500/20"><Trophy className="w-6 h-6 text-green-400" /></div>
          <div><div className="text-2xl font-bold">{totalProgress.completed}</div><div className="text-sm text-gray-400">완료한 학습</div></div>
        </div>
      </section>

      {/* 카테고리 */}
      <section>
        <h2 className="text-xl font-bold mb-4">📚 카테고리별 학습</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {CATEGORIES.map((cat) => (
            <Link key={cat.id} href={`/study/${cat.name}`} className="card card-hover group">
              <div className="flex items-center gap-3 mb-3">
                <span className="text-3xl">{cat.icon}</span>
                <div>
                  <h3 className="font-bold group-hover:text-primary transition">{cat.nameKo}</h3>
                  <p className="text-sm text-gray-400">{cat.contentCount}개 콘텐츠</p>
                </div>
              </div>
              <p className="text-sm text-gray-400 mb-3">{cat.description}</p>
              <div className="flex items-center justify-between text-xs">
                <span className="text-gray-500">Day {cat.days[0]}-{cat.days[cat.days.length - 1]}</span>
                <span className="text-primary flex items-center gap-1">학습하기 <ArrowRight className="w-3 h-3" /></span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* 40일 로드맵 미리보기 */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold">🗓️ 40일 로드맵</h2>
          <Link href="/roadmap" className="text-primary text-sm hover:underline">전체 보기 →</Link>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {ROADMAP.slice(0, 10).map((day) => (
            <div key={day.day} className="card p-3 text-center hover:border-primary/50 transition">
              <div className="text-2xl font-bold text-primary">Day {day.day}</div>
              <div className="text-xs text-gray-400 mt-1 line-clamp-2">{day.title}</div>
              <div className="text-xs text-gray-500 mt-1">{day.hours}시간</div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
