'use client';

import { useState, useEffect, useCallback, useMemo } from 'react';

const STORAGE_KEY = 'codemaster_recent_searches';
const MAX_RECENT = 5;

export interface SearchResult {
  id: string;
  title: string;
  category: string;
  slug: string;
}

export function useSearch(allContents: SearchResult[]) {
  const [query, setQuery] = useState('');
  const [recentSearches, setRecentSearches] = useState<string[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) setRecentSearches(JSON.parse(saved));
    }
  }, []);

  useEffect(() => {
    if (typeof window !== 'undefined' && recentSearches.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(recentSearches));
    }
  }, [recentSearches]);

  const results = useMemo(() => {
    if (!query.trim()) return [];
    const lowerQuery = query.toLowerCase();
    return allContents.filter(c => 
      c.title.toLowerCase().includes(lowerQuery)
    ).slice(0, 10);
  }, [query, allContents]);

  const addToRecent = useCallback((q: string) => {
    if (!q.trim()) return;
    setRecentSearches(prev => [q, ...prev.filter(s => s !== q)].slice(0, MAX_RECENT));
  }, []);

  const clearRecent = useCallback(() => {
    setRecentSearches([]);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(prev => !prev);
      }
      if (e.key === 'Escape') setIsOpen(false);
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return { query, setQuery, results, recentSearches, isOpen, setIsOpen, addToRecent, clearRecent };
}
