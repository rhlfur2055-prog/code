'use client';

import Link from 'next/link';
import { Star, Trash2 } from 'lucide-react';
import { useBookmark } from '@/hooks/useBookmark';

export default function BookmarkPage() {
  const { getBookmarkList, getBookmarkCount, clearBookmarks } = useBookmark();
  const bookmarks = getBookmarkList();
  const count = getBookmarkCount();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">⭐ 내 북마크</h1>
          <p className="text-gray-400 mt-1">{count}개의 콘텐츠를 저장했습니다</p>
        </div>
        {count > 0 && (
          <button
            onClick={clearBookmarks}
            className="btn flex items-center gap-2 text-red-400 hover:bg-red-500/20"
          >
            <Trash2 className="w-4 h-4" />
            전체 삭제
          </button>
        )}
      </div>

      {count === 0 ? (
        <div className="card text-center py-16">
          <div className="text-6xl mb-4">📚</div>
          <h2 className="text-xl font-bold mb-2">북마크가 비어있습니다</h2>
          <p className="text-gray-400 mb-4">
            학습 중 ⭐ 버튼을 눌러 북마크를 추가해보세요!
          </p>
          <Link href="/" className="btn btn-primary">
            학습 시작하기
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {bookmarks.map((bookmark) => (
            <div
              key={bookmark.contentId}
              className="card p-4 flex items-center gap-4"
            >
              <Star className="w-5 h-5 fill-yellow-400 text-yellow-400 shrink-0" />
              <div className="flex-1">
                <h3 className="font-medium">{bookmark.contentId}</h3>
                <p className="text-xs text-gray-500">
                  {new Date(bookmark.addedAt).toLocaleDateString('ko-KR')} 저장됨
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
