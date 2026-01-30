'use client';

import { useState, useEffect, useCallback } from 'react';

const STORAGE_KEY = 'codemaster_bookmarks';

export interface BookmarkItem {
  contentId: string;
  addedAt: string;
}

export function useBookmark() {
  const [bookmarks, setBookmarks] = useState<Record<string, BookmarkItem>>({});
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        try {
          setBookmarks(JSON.parse(saved));
        } catch (e) {
          console.error('Bookmark 로드 실패:', e);
        }
      }
      setIsLoaded(true);
    }
  }, []);

  useEffect(() => {
    if (isLoaded && typeof window !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(bookmarks));
    }
  }, [bookmarks, isLoaded]);

  const toggleBookmark = useCallback((contentId: string) => {
    setBookmarks(prev => {
      if (prev[contentId]) {
        const { [contentId]: _, ...rest } = prev;
        return rest;
      }
      return {
        ...prev,
        [contentId]: { contentId, addedAt: new Date().toISOString() },
      };
    });
  }, []);

  const isBookmarked = useCallback((contentId: string) => {
    return !!bookmarks[contentId];
  }, [bookmarks]);

  const getBookmarkList = useCallback(() => {
    return Object.values(bookmarks).sort(
      (a, b) => new Date(b.addedAt).getTime() - new Date(a.addedAt).getTime()
    );
  }, [bookmarks]);

  const getBookmarkCount = useCallback(() => {
    return Object.keys(bookmarks).length;
  }, [bookmarks]);

  const clearBookmarks = useCallback(() => {
    setBookmarks({});
    if (typeof window !== 'undefined') {
      localStorage.removeItem(STORAGE_KEY);
    }
  }, []);

  return { bookmarks, isLoaded, toggleBookmark, isBookmarked, getBookmarkList, getBookmarkCount, clearBookmarks };
}
