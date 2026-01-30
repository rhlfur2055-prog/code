'use client';

import { Star } from 'lucide-react';
import { useBookmark } from '@/hooks/useBookmark';

interface BookmarkButtonProps {
  contentId: string;
  size?: 'sm' | 'md' | 'lg';
}

export function BookmarkButton({ contentId, size = 'md' }: BookmarkButtonProps) {
  const { isBookmarked, toggleBookmark, isLoaded } = useBookmark();
  const bookmarked = isBookmarked(contentId);

  const sizeClasses = { sm: 'w-6 h-6', md: 'w-8 h-8', lg: 'w-10 h-10' };
  const iconSizes = { sm: 'w-4 h-4', md: 'w-5 h-5', lg: 'w-6 h-6' };

  if (!isLoaded) {
    return <div className={`${sizeClasses[size]} rounded-full bg-dark-border animate-pulse`} />;
  }

  return (
    <button
      onClick={() => toggleBookmark(contentId)}
      className={`${sizeClasses[size]} rounded-full flex items-center justify-center transition-all hover:scale-110`}
      title={bookmarked ? '북마크 해제' : '북마크 추가'}
    >
      <Star className={`${iconSizes[size]} ${bookmarked ? 'fill-yellow-400 text-yellow-400' : 'text-gray-400 hover:text-yellow-400'}`} />
    </button>
  );
}
