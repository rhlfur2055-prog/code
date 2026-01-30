'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { CATEGORIES } from '@/types';

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden lg:block w-64 shrink-0">
      <div className="sticky top-20 bg-dark-card rounded-xl border border-dark-border p-4">
        <h3 className="text-sm font-bold text-gray-400 mb-3">📚 카테고리</h3>
        <nav className="flex flex-col gap-1">
          {CATEGORIES.map((cat) => {
            const isActive = pathname.includes(`/study/${cat.name}`);
            return (
              <Link
                key={cat.id}
                href={`/study/${cat.name}`}
                className={`flex items-center justify-between p-2 rounded-lg transition ${
                  isActive ? 'bg-primary/20 text-primary' : 'hover:bg-dark-border text-gray-300'
                }`}
              >
                <span className="flex items-center gap-2">
                  <span>{cat.icon}</span>
                  <span className="text-sm">{cat.nameKo.split(' ')[0]}</span>
                </span>
                <span className="text-xs text-gray-500">{cat.contentCount}</span>
              </Link>
            );
          })}
        </nav>

        <div className="mt-4 pt-4 border-t border-dark-border">
          <Link href="/roadmap" className="flex items-center gap-2 p-2 rounded-lg hover:bg-dark-border text-gray-300 transition">
            <span>🗓️</span>
            <span className="text-sm">40일 로드맵</span>
          </Link>
        </div>
      </div>
    </aside>
  );
}
