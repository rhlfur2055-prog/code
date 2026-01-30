'use client';

import { Check, Circle } from 'lucide-react';
import { useProgress } from '@/hooks/useProgress';

interface ProgressButtonProps {
  contentId: string;
  size?: 'sm' | 'md' | 'lg';
}

export function ProgressButton({ contentId, size = 'md' }: ProgressButtonProps) {
  const { isCompleted, toggleComplete, isLoaded } = useProgress();
  const completed = isCompleted(contentId);

  const sizeClasses = { sm: 'w-6 h-6', md: 'w-8 h-8', lg: 'w-10 h-10' };

  if (!isLoaded) {
    return <div className={`${sizeClasses[size]} rounded-full bg-dark-border animate-pulse`} />;
  }

  return (
    <button
      onClick={() => toggleComplete(contentId)}
      className={`${sizeClasses[size]} rounded-full flex items-center justify-center transition-all ${
        completed ? 'bg-primary text-white' : 'bg-dark-border text-gray-400 hover:bg-primary/20 hover:text-primary'
      }`}
      title={completed ? '완료 취소' : '완료 표시'}
    >
      {completed ? <Check className="w-4 h-4" /> : <Circle className="w-4 h-4" />}
    </button>
  );
}
