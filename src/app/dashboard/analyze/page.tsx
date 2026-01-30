'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { useApi } from '@/hooks/useApi';

interface SentimentResult {
  label: string;
  score: number;
  details?: {
    positive_indicators: number;
    negative_indicators: number;
    text_length: number;
  };
}

interface KeywordResult {
  word: string;
  count: number;
  score: number;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export default function AnalyzePage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const { aiRequest, isLoading, error } = useApi();

  const [activeTab, setActiveTab] = useState<'sentiment' | 'keywords' | 'chat'>('sentiment');
  const [text, setText] = useState('');
  const [sentimentResult, setSentimentResult] = useState<SentimentResult | null>(null);
  const [keywordsResult, setKeywordsResult] = useState<KeywordResult[]>([]);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState('');

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [authLoading, isAuthenticated, router]);

  const analyzeSentiment = async () => {
    if (!text.trim()) return;
    try {
      const response = await aiRequest<{ success: boolean; sentiment: SentimentResult }>(
        '/api/v1/text/sentiment',
        { method: 'POST', body: { text } }
      );
      if (response.success) {
        setSentimentResult(response.sentiment);
      }
    } catch (err) {
      console.error('Sentiment analysis failed:', err);
    }
  };

  const extractKeywords = async () => {
    if (!text.trim()) return;
    try {
      const response = await aiRequest<{ success: boolean; keywords: KeywordResult[] }>(
        '/api/v1/text/keywords',
        { method: 'POST', body: { text } }
      );
      if (response.success) {
        setKeywordsResult(response.keywords);
      }
    } catch (err) {
      console.error('Keyword extraction failed:', err);
    }
  };

  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;

    const userMessage = chatInput;
    setChatInput('');
    setChatMessages(prev => [...prev, { role: 'user', content: userMessage }]);

    try {
      const response = await aiRequest<{ success: boolean; response: string }>(
        '/api/v1/chat',
        { method: 'POST', body: { message: userMessage } }
      );
      if (response.success) {
        setChatMessages(prev => [...prev, { role: 'assistant', content: response.response }]);
      }
    } catch (err) {
      console.error('Chat failed:', err);
      setChatMessages(prev => [...prev, { role: 'assistant', content: '오류가 발생했습니다. 다시 시도해주세요.' }]);
    }
  };

  const getSentimentColor = (label: string) => {
    switch (label) {
      case 'positive': return 'text-green-400 bg-green-500/20';
      case 'negative': return 'text-red-400 bg-red-500/20';
      default: return 'text-gray-400 bg-gray-500/20';
    }
  };

  const getSentimentEmoji = (label: string) => {
    switch (label) {
      case 'positive': return '😊';
      case 'negative': return '😢';
      default: return '😐';
    }
  };

  if (authLoading) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center">
        <div className="text-gray-400">로딩 중...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">AI 분석</h1>
          <p className="text-gray-400 mt-1">텍스트를 AI로 분석합니다</p>
        </div>
        <button
          onClick={() => router.push('/dashboard')}
          className="px-4 py-2 text-gray-400 hover:text-white transition-colors"
        >
          ← 대시보드
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-2">
        {[
          { id: 'sentiment', label: '감성 분석', icon: '❤️' },
          { id: 'keywords', label: '키워드 추출', icon: '🔑' },
          { id: 'chat', label: 'AI 채팅', icon: '💬' },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as typeof activeTab)}
            className={`px-4 py-2 rounded-lg transition-colors flex items-center gap-2 ${
              activeTab === tab.id
                ? 'bg-primary text-white'
                : 'bg-dark-card text-gray-400 hover:text-white'
            }`}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Error */}
      {error && (
        <div className="p-4 bg-red-500/10 border border-red-500/50 rounded-lg">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {/* Content */}
      {activeTab !== 'chat' ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input */}
          <div className="bg-dark-card border border-dark-border rounded-xl p-6">
            <h2 className="text-lg font-semibold text-white mb-4">텍스트 입력</h2>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="분석할 텍스트를 입력하세요..."
              className="w-full h-48 px-4 py-3 bg-dark-bg border border-dark-border rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary resize-none"
            />
            <div className="mt-4 flex gap-3">
              {activeTab === 'sentiment' && (
                <button
                  onClick={analyzeSentiment}
                  disabled={isLoading || !text.trim()}
                  className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50 transition-colors"
                >
                  {isLoading ? '분석 중...' : '감성 분석'}
                </button>
              )}
              {activeTab === 'keywords' && (
                <button
                  onClick={extractKeywords}
                  disabled={isLoading || !text.trim()}
                  className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50 transition-colors"
                >
                  {isLoading ? '추출 중...' : '키워드 추출'}
                </button>
              )}
            </div>
          </div>

          {/* Results */}
          <div className="bg-dark-card border border-dark-border rounded-xl p-6">
            <h2 className="text-lg font-semibold text-white mb-4">분석 결과</h2>

            {activeTab === 'sentiment' && (
              <>
                {sentimentResult ? (
                  <div className="space-y-6">
                    <div className="text-center">
                      <div className="text-6xl mb-4">{getSentimentEmoji(sentimentResult.label)}</div>
                      <span className={`px-4 py-2 rounded-full text-lg font-medium ${getSentimentColor(sentimentResult.label)}`}>
                        {sentimentResult.label === 'positive' ? '긍정적' :
                         sentimentResult.label === 'negative' ? '부정적' : '중립적'}
                      </span>
                    </div>

                    <div className="space-y-3">
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-400">신뢰도</span>
                          <span className="text-white">{(sentimentResult.score * 100).toFixed(1)}%</span>
                        </div>
                        <div className="h-2 bg-dark-bg rounded-full overflow-hidden">
                          <div
                            className="h-full bg-primary rounded-full transition-all"
                            style={{ width: `${sentimentResult.score * 100}%` }}
                          />
                        </div>
                      </div>

                      {sentimentResult.details && (
                        <div className="grid grid-cols-2 gap-4 mt-4">
                          <div className="bg-dark-bg rounded-lg p-3">
                            <p className="text-gray-400 text-sm">긍정 지표</p>
                            <p className="text-white text-lg font-semibold">{sentimentResult.details.positive_indicators}</p>
                          </div>
                          <div className="bg-dark-bg rounded-lg p-3">
                            <p className="text-gray-400 text-sm">부정 지표</p>
                            <p className="text-white text-lg font-semibold">{sentimentResult.details.negative_indicators}</p>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ) : (
                  <div className="text-center text-gray-500 py-12">
                    텍스트를 입력하고 분석을 시작하세요
                  </div>
                )}
              </>
            )}

            {activeTab === 'keywords' && (
              <>
                {keywordsResult.length > 0 ? (
                  <div className="space-y-4">
                    <div className="flex flex-wrap gap-2">
                      {keywordsResult.map((keyword, index) => (
                        <span
                          key={index}
                          className="px-3 py-2 bg-primary/20 text-primary rounded-lg"
                          style={{ fontSize: `${Math.max(12, 14 + keyword.score * 10)}px` }}
                        >
                          {keyword.word}
                          <span className="text-xs ml-1 opacity-60">({keyword.count})</span>
                        </span>
                      ))}
                    </div>

                    <div className="mt-6 space-y-2">
                      {keywordsResult.slice(0, 5).map((keyword, index) => (
                        <div key={index} className="flex items-center gap-3">
                          <span className="text-gray-400 text-sm w-24 truncate">{keyword.word}</span>
                          <div className="flex-1 h-2 bg-dark-bg rounded-full overflow-hidden">
                            <div
                              className="h-full bg-primary rounded-full"
                              style={{ width: `${Math.min(keyword.score * 100, 100)}%` }}
                            />
                          </div>
                          <span className="text-white text-sm w-12">{keyword.count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                ) : (
                  <div className="text-center text-gray-500 py-12">
                    텍스트를 입력하고 키워드를 추출하세요
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      ) : (
        /* Chat Tab */
        <div className="bg-dark-card border border-dark-border rounded-xl overflow-hidden">
          <div className="h-[500px] flex flex-col">
            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {chatMessages.length === 0 ? (
                <div className="text-center text-gray-500 py-12">
                  AI와 대화를 시작하세요
                </div>
              ) : (
                chatMessages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] px-4 py-3 rounded-2xl ${
                        msg.role === 'user'
                          ? 'bg-primary text-white'
                          : 'bg-dark-bg text-gray-200'
                      }`}
                    >
                      {msg.content}
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Chat Input */}
            <div className="border-t border-dark-border p-4">
              <div className="flex gap-3">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
                  placeholder="메시지를 입력하세요..."
                  className="flex-1 px-4 py-3 bg-dark-bg border border-dark-border rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary"
                />
                <button
                  onClick={sendChatMessage}
                  disabled={isLoading || !chatInput.trim()}
                  className="px-6 py-3 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50 transition-colors"
                >
                  {isLoading ? '...' : '전송'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
