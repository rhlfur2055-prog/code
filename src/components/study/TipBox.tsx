'use client';

import { ReactNode } from 'react';
import { Lightbulb, AlertTriangle, CheckCircle, Info, Zap, Target } from 'lucide-react';

interface TipBoxProps {
  type?: 'tip' | 'warning' | 'success' | 'info' | 'important' | 'goal';
  title?: string;
  children: ReactNode;
}

const types = {
  tip: {
    icon: Lightbulb,
    bg: 'bg-blue-500/10',
    border: 'border-blue-500',
    iconColor: 'text-blue-400',
    titleColor: 'text-blue-400',
    defaultTitle: '핵심 포인트',
  },
  warning: {
    icon: AlertTriangle,
    bg: 'bg-yellow-500/10',
    border: 'border-yellow-500',
    iconColor: 'text-yellow-400',
    titleColor: 'text-yellow-400',
    defaultTitle: '주의',
  },
  success: {
    icon: CheckCircle,
    bg: 'bg-green-500/10',
    border: 'border-green-500',
    iconColor: 'text-green-400',
    titleColor: 'text-green-400',
    defaultTitle: '성공',
  },
  info: {
    icon: Info,
    bg: 'bg-cyan-500/10',
    border: 'border-cyan-500',
    iconColor: 'text-cyan-400',
    titleColor: 'text-cyan-400',
    defaultTitle: '정보',
  },
  important: {
    icon: Zap,
    bg: 'bg-purple-500/10',
    border: 'border-purple-500',
    iconColor: 'text-purple-400',
    titleColor: 'text-purple-400',
    defaultTitle: '중요',
  },
  goal: {
    icon: Target,
    bg: 'bg-pink-500/10',
    border: 'border-pink-500',
    iconColor: 'text-pink-400',
    titleColor: 'text-pink-400',
    defaultTitle: '학습 목표',
  },
};

export function TipBox({ type = 'tip', title, children }: TipBoxProps) {
  const config = types[type];
  const Icon = config.icon;
  const displayTitle = title || config.defaultTitle;

  return (
    <div
      className={`
        ${config.bg} border-l-4 ${config.border} rounded-r-lg
        p-4 mb-6 transition-all duration-300
        hover:translate-x-1
      `}
    >
      <div className="flex items-start gap-3">
        <Icon size={20} className={`${config.iconColor} flex-shrink-0 mt-0.5`} />
        <div className="flex-1">
          <div className={`font-bold ${config.titleColor} mb-1`}>{displayTitle}</div>
          <div className="text-gray-400 leading-relaxed">{children}</div>
        </div>
      </div>
    </div>
  );
}
