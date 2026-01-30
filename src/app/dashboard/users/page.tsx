'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { useApi } from '@/hooks/useApi';
import { User, ApiResponse } from '@/types';

export default function UsersPage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading, token } = useAuth();
  const { request, isLoading, error } = useApi();
  const [users, setUsers] = useState<User[]>([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [authLoading, isAuthenticated, router]);

  useEffect(() => {
    if (token && user?.role === 'ADMIN') {
      fetchUsers();
    }
  }, [token, user]);

  const fetchUsers = async () => {
    try {
      const response = await request<ApiResponse<User[]>>('/api/users');
      if (response.success) {
        setUsers(response.data);
      }
    } catch (err) {
      console.error('Failed to fetch users:', err);
    }
  };

  const handleDeleteUser = async (userId: number) => {
    if (!confirm('정말로 이 사용자를 삭제하시겠습니까?')) return;

    try {
      await request(`/api/users/${userId}`, { method: 'DELETE' });
      setUsers(users.filter(u => u.id !== userId));
    } catch (err) {
      console.error('Failed to delete user:', err);
    }
  };

  if (authLoading) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="text-gray-400">로딩 중...</div>
      </div>
    );
  }

  if (!isAuthenticated || !user) {
    return null;
  }

  if (user.role !== 'ADMIN') {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-white mb-2">접근 권한 없음</h1>
          <p className="text-gray-400">관리자만 이 페이지에 접근할 수 있습니다.</p>
        </div>
      </div>
    );
  }

  const filteredUsers = users.filter(u =>
    u.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">사용자 관리</h1>
          <p className="text-gray-400 mt-1">시스템 사용자를 관리합니다</p>
        </div>
        <button
          onClick={() => router.push('/dashboard')}
          className="px-4 py-2 text-gray-400 hover:text-white transition-colors"
        >
          ← 대시보드
        </button>
      </div>

      {/* Search */}
      <div className="bg-dark-card border border-dark-border rounded-xl p-4">
        <input
          type="text"
          placeholder="사용자 검색..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-4 py-3 bg-dark-bg border border-dark-border rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        />
      </div>

      {/* Error */}
      {error && (
        <div className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {/* Users Table */}
      <div className="bg-dark-card border border-dark-border rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-dark-bg">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">ID</th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">사용자명</th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">이메일</th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">역할</th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">상태</th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">가입일</th>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-400">액션</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border">
              {isLoading ? (
                <tr>
                  <td colSpan={7} className="px-6 py-8 text-center text-gray-400">
                    로딩 중...
                  </td>
                </tr>
              ) : filteredUsers.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-6 py-8 text-center text-gray-400">
                    사용자가 없습니다
                  </td>
                </tr>
              ) : (
                filteredUsers.map((u) => (
                  <tr key={u.id} className="hover:bg-dark-bg/50 transition-colors">
                    <td className="px-6 py-4 text-sm text-gray-300">{u.id}</td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center text-sm text-primary">
                          {u.username.charAt(0).toUpperCase()}
                        </div>
                        <span className="text-white">{u.username}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-300">{u.email}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        u.role === 'ADMIN'
                          ? 'bg-purple-500/20 text-purple-400'
                          : 'bg-blue-500/20 text-blue-400'
                      }`}>
                        {u.role}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        u.isActive
                          ? 'bg-green-500/20 text-green-400'
                          : 'bg-red-500/20 text-red-400'
                      }`}>
                        {u.isActive ? '활성' : '비활성'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-400">
                      {new Date(u.createdAt).toLocaleDateString('ko-KR')}
                    </td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => handleDeleteUser(u.id)}
                        className="text-red-400 hover:text-red-300 text-sm transition-colors"
                        disabled={u.id === user.id}
                      >
                        삭제
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-dark-card border border-dark-border rounded-xl p-5">
          <p className="text-gray-400 text-sm">전체 사용자</p>
          <p className="text-2xl font-bold text-white mt-1">{users.length}명</p>
        </div>
        <div className="bg-dark-card border border-dark-border rounded-xl p-5">
          <p className="text-gray-400 text-sm">관리자</p>
          <p className="text-2xl font-bold text-white mt-1">
            {users.filter(u => u.role === 'ADMIN').length}명
          </p>
        </div>
        <div className="bg-dark-card border border-dark-border rounded-xl p-5">
          <p className="text-gray-400 text-sm">활성 사용자</p>
          <p className="text-2xl font-bold text-white mt-1">
            {users.filter(u => u.isActive).length}명
          </p>
        </div>
      </div>
    </div>
  );
}
