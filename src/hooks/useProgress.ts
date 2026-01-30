'use client';

import { useState, useEffect, useCallback } from 'react';

const STORAGE_KEY = 'codemaster_progress';

export interface ProgressItem {
  contentId: string;
  completed: boolean;
  completedAt: string | null;
}

export function useProgress() {
  const [progress, setProgress] = useState<Record<string, ProgressItem>>({});
  const [isLoaded, setIsLoaded] = useState(false);

  // 초기 로드
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        try {
          setProgress(JSON.parse(saved));
        } catch (e) {
          console.error('Progress 로드 실패:', e);
        }
      }
      setIsLoaded(true);
    }
  }, []);

  // 저장
  useEffect(() => {
    if (isLoaded && typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    }
  }, [progress, isLoaded]);

  // 탭 간 동기화
  useEffect(() => {
    const handleStorage = (e: StorageEvent) => {
      if (e.key === STORAGE_KEY && e.newValue) {
        try {
          setProgress(JSON.parse(e.newValue));
        } catch (err) {
          console.error('Storage sync error:', err);
        }
      }
    };
    window.addEventListener('storage', handleStorage);
    return () => window.removeEventListener('storage', handleStorage);
  }, []);

  // 완료 토글
  const toggleComplete = useCallback((contentId: string) => {
    setProgress(prev => {
      const current = prev[contentId];
      if (current?.completed) {
        const { [contentId]: _, ...rest } = prev;
        return rest;
      }
      return {
        ...prev,
        [contentId]: {
          contentId,
          completed: true,
          completedAt: new Date().toISOString(),
        },
      };
    });
  }, []);

  // 완료 여부 확인
  const isCompleted = useCallback((contentId: string) => {
    return progress[contentId]?.completed ?? false;
  }, [progress]);

  // 카테고리별 진행률
  const getCategoryProgress = useCallback((contentIds: string[]) => {
    const completed = contentIds.filter(id => progress[id]?.completed).length;
    return {
      completed,
      total: contentIds.length,
      percentage: contentIds.length > 0 ? Math.round((completed / contentIds.length) * 100) : 0,
    };
  }, [progress]);

  // 전체 진행률
  const getTotalProgress = useCallback((totalContents: number) => {
    const completed = Object.values(progress).filter(p => p.completed).length;
    return {
      completed,
      total: totalContents,
      percentage: totalContents > 0 ? Math.round((completed / totalContents) * 100) : 0,
    };
  }, [progress]);

  // 초기화
  const resetProgress = useCallback(() => {
    setProgress({});
    if (typeof window !== 'undefined') {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  return {
    progress,
    isLoaded,
    toggleComplete,
    isCompleted,
    getCategoryProgress,
    getTotalProgress,
    resetProgress,
  };
}
