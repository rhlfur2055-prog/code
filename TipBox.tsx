'use client';

import { ReactNode } from 'react';
import { 
  Lightbulb, 
  AlertTriangle, 
  CheckCircle, 
  Info,
  Zap,
  Target
} from 'lucide-react';

interface TipBoxProps {
  children: ReactNode;
  type?: 'tip' | 'warning' | 'success' | 'info' | 'important' | 'goal';
  title?: string;
}

export function TipBox({ children, type = 'tip', title }: TipBoxProps) {
  const types = {
    tip: {
      icon: Lightbulb,
      bg: 'bg-gradient-to-r from-blue-500/10 to-blue-600/5',
      border: 'border-l-blue-500',
      titleColor: 'text-blue-400',
      iconColor: 'text-blue-400',
      defaultTitle: '💡 핵심 포인트'
    },
    warning: {
      icon: AlertTriangle,
      bg: 'bg-gradient-to-r from-yellow-500/10 to-yellow-600/5',
      border: 'border-l-yellow-500',
      titleColor: 'text-yellow-400',
      iconColor: 'text-yellow-400',
      defaultTitle: '⚠️ 주의사항'
    },
    success: {
      icon: CheckCircle,
      bg: 'bg-gradient-to-r from-green-500/10 to-green-600/5',
      border: 'border-l-green-500',
      titleColor: 'text-green-400',
      iconColor: 'text-green-400',
      defaultTitle: '✅ 성공 팁'
    },
    info: {
      icon: Info,
      bg: 'bg-gradient-to-r from-cyan-500/10 to-cyan-600/5',
      border: 'border-l-cyan-500',
      titleColor: 'text-cyan-400',
      iconColor: 'text-cyan-400',
      defaultTitle: 'ℹ️ 참고사항'
    },
    important: {
      icon: Zap,
      bg: 'bg-gradient-to-r from-purple-500/10 to-purple-600/5',
      border: 'border-l-purple-500',
      titleColor: 'text-purple-400',
      iconColor: 'text-purple-400',
      defaultTitle: '⚡ 중요'
    },
    goal: {
      icon: Target,
      bg: 'bg-gradient-to-r from-pink-500/10 to-pink-600/5',
      border: 'border-l-pink-500',
      titleColor: 'text-pink-400',
      iconColor: 'text-pink-400',
      defaultTitle: '🎯 학습 목표'
    }
  };

  const style = types[type];
  const Icon = style.icon;
  const displayTitle = title || style.defaultTitle;

  return (
    <div className={`
      relative rounded-r-xl p-5 mb-6
      border-l-4 ${style.border} ${style.bg}
      backdrop-blur-sm
      transition-all duration-300
      hover:shadow-lg hover:translate-x-1
    `}>
      <div className="flex items-start gap-3">
        <Icon className={`w-5 h-5 mt-0.5 flex-shrink-0 ${style.iconColor}`} />
        
        <div className="flex-1">
          <div className={`font-bold mb-2 ${style.titleColor}`}>
            {displayTitle}
          </div>
          
          <div className="prose prose-invert prose-sm max-w-none">
            <div className="text-gray-300 leading-relaxed">
              {children}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
