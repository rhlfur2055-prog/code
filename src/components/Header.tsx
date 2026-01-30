'use client';

import Link from 'next/link';
import { Search, Moon, Sun, Bookmark, Menu, X } from 'lucide-react';
import { useTheme } from '@/hooks/useTheme';
import { useBookmark } from '@/hooks/useBookmark';
import { useState } from 'react';

export function Header() {
  const { theme, toggleTheme } = useTheme();
  const { getBookmarkCount } = useBookmark();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 bg-dark-card/95 backdrop-blur border-b border-dark-border">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* 로고 */}
        <Link href="/" className="flex items-center gap-2">
          <span className="text-2xl">🚀</span>
          <span className="text-xl font-bold text-primary">코드마스터</span>
          <span className="hidden sm:inline text-sm text-gray-400">40일 풀스택</span>
        </Link>

        {/* 네비게이션 */}
        <nav className="hidden md:flex items-center gap-6">
          <Link href="/curriculum" className="text-gray-300 hover:text-primary transition">커리큘럼</Link>
          <Link href="/roadmap" className="text-gray-300 hover:text-primary transition">40일 로드맵</Link>
          <Link href="/bookmark" className="flex items-center gap-1 text-gray-300 hover:text-primary transition">
            <Bookmark className="w-4 h-4" />
            <span>북마크</span>
            {getBookmarkCount() > 0 && (
              <span className="bg-primary text-white text-xs px-1.5 rounded-full">{getBookmarkCount()}</span>
            )}
          </Link>
        </nav>

        {/* 우측 아이콘 */}
        <div className="flex items-center gap-3">
          <button className="p-2 rounded-lg hover:bg-dark-border transition" title="검색 (Cmd+K)">
            <Search className="w-5 h-5 text-gray-400" />
          </button>
          <button onClick={toggleTheme} className="p-2 rounded-lg hover:bg-dark-border transition">
            {theme === 'dark' ? <Sun className="w-5 h-5 text-yellow-400" /> : <Moon className="w-5 h-5 text-gray-400" />}
          </button>
          <button onClick={() => setIsMenuOpen(!isMenuOpen)} className="md:hidden p-2 rounded-lg hover:bg-dark-border">
            {isMenuOpen ? <X className="w-5 h-5 text-gray-400" /> : <Menu className="w-5 h-5 text-gray-400" />}
          </button>
        </div>
      </div>

      {/* 모바일 메뉴 */}
      {isMenuOpen && (
        <div className="md:hidden border-t border-dark-border bg-dark-card">
          <nav className="flex flex-col p-4 gap-2">
            <Link href="/curriculum" className="p-3 rounded-lg hover:bg-dark-border text-gray-300">📚 커리큘럼</Link>
            <Link href="/roadmap" className="p-3 rounded-lg hover:bg-dark-border text-gray-300">🗓️ 40일 로드맵</Link>
            <Link href="/bookmark" className="p-3 rounded-lg hover:bg-dark-border text-gray-300">⭐ 북마크 ({getBookmarkCount()})</Link>
          </nav>
        </div>
      )}
    </header>
  );
}
