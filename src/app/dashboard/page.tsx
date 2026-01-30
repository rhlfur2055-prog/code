'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';

export default function DashboardPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading, logout } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="text-gray-400">로딩 중...</div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return null;
  }

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  const stats = [
    { label: '학습 진행률', value: '45%', icon: '📚', color: 'bg-blue-500' },
    { label: '완료한 챕터', value: '18', icon: '✅', color: 'bg-green-500' },
    { label: '북마크', value: '7', icon: '🔖', color: 'bg-yellow-500' },
    { label: '연속 학습일', value: '5일', icon: '🔥', color: 'bg-orange-500' },
  ];

  const quickLinks = [
    { title: '사용자 관리', href: '/dashboard/users', icon: '👥', description: '시스템 사용자 관리' },
    { title: 'AI 분석', href: '/dashboard/analyze', icon: '🤖', description: '텍스트 AI 분석' },
    { title: 'AI 데모', href: '/ai-demo', icon: '🎯', description: '번호판/음성 인식' },
    { title: '학습 커리큘럼', href: '/curriculum', icon: '📖', description: '40일 완성 로드맵' },
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">대시보드</h1>
          <p className="text-gray-400 mt-1">안녕하세요, {user.username}님!</p>
        </div>
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-500/10 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors"
        >
          로그아웃
        </button>
      </div>

      {/* User Info Card */}
      <div className="bg-dark-card border border-dark-border rounded-xl p-6">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 bg-primary/20 rounded-full flex items-center justify-center text-2xl">
            {user.username.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="text-xl font-semibold text-white">{user.username}</h2>
            <p className="text-gray-400">{user.email}</p>
            <span className={`inline-block mt-2 px-3 py-1 text-xs rounded-full ${
              user.role === 'ADMIN' ? 'bg-purple-500/20 text-purple-400' : 'bg-green-500/20 text-green-400'
            }`}>
              {user.role}
            </span>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <div key={index} className="bg-dark-card border border-dark-border rounded-xl p-5">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">{stat.label}</p>
                <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
              </div>
              <div className={`w-12 h-12 ${stat.color}/20 rounded-lg flex items-center justify-center text-2xl`}>
                {stat.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Links */}
      <div>
        <h2 className="text-xl font-semibold text-white mb-4">빠른 메뉴</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickLinks.map((link, index) => (
            <Link
              key={index}
              href={link.href}
              className="bg-dark-card border border-dark-border rounded-xl p-5 hover:border-primary/50 transition-colors group"
            >
              <div className="text-3xl mb-3">{link.icon}</div>
              <h3 className="text-white font-medium group-hover:text-primary transition-colors">
                {link.title}
              </h3>
              <p className="text-gray-500 text-sm mt-1">{link.description}</p>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-dark-card border border-dark-border rounded-xl p-6">
        <h2 className="text-xl font-semibold text-white mb-4">최근 활동</h2>
        <div className="space-y-4">
          <div className="flex items-center gap-4 text-gray-400">
            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
            <span>로그인 완료</span>
            <span className="text-gray-600 ml-auto text-sm">방금 전</span>
          </div>
          <div className="flex items-center gap-4 text-gray-400">
            <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
            <span>Java OOP 챕터 완료</span>
            <span className="text-gray-600 ml-auto text-sm">2시간 전</span>
          </div>
          <div className="flex items-center gap-4 text-gray-400">
            <span className="w-2 h-2 bg-yellow-500 rounded-full"></span>
            <span>Spring Boot 강의 북마크</span>
            <span className="text-gray-600 ml-auto text-sm">어제</span>
          </div>
        </div>
      </div>
    </div>
  );
}
