import type { Metadata } from 'next';
import '@/styles/globals.css';
import { Header } from '@/components/Header';
import { Sidebar } from '@/components/Sidebar';
import { AuthProvider } from '@/context/AuthContext';

export const metadata: Metadata = {
  title: '코드마스터 - 40일 완성 풀스택 개발자 부트캠프',
  description: '760개 학습 콘텐츠 | 16개 카테고리 | 한국풍 인프런 스타일',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" className="dark">
      <body className="min-h-screen bg-dark-bg text-gray-100">
        <AuthProvider>
          <Header />
          <div className="max-w-7xl mx-auto px-4 py-6 flex gap-6">
            <Sidebar />
            <main className="flex-1 min-w-0">{children}</main>
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
