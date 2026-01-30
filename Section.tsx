'use client';

import { ReactNode } from 'react';

interface SectionProps {
  title: string;
  children: ReactNode;
  variant?: 'concept' | 'theory' | 'practice' | 'note';
}

export function Section({ title, children, variant = 'concept' }: SectionProps) {
  const variants = {
    concept: {
      bg: 'bg-gradient-to-br from-blue-500/10 to-blue-600/5',
      border: 'border-blue-500/30',
      titleColor: 'text-blue-400',
      icon: '💡'
    },
    theory: {
      bg: 'bg-gradient-to-br from-purple-500/10 to-purple-600/5',
      border: 'border-purple-500/30',
      titleColor: 'text-purple-400',
      icon: '📚'
    },
    practice: {
      bg: 'bg-gradient-to-br from-green-500/10 to-green-600/5',
      border: 'border-green-500/30',
      titleColor: 'text-green-400',
      icon: '🛠️'
    },
    note: {
      bg: 'bg-gradient-to-br from-yellow-500/10 to-yellow-600/5',
      border: 'border-yellow-500/30',
      titleColor: 'text-yellow-400',
      icon: '📝'
    }
  };

  const style = variants[variant];

  return (
    <div className={`
      rounded-xl p-6 mb-6 
      border ${style.border} ${style.bg}
      backdrop-blur-sm
      transition-all duration-300
      hover:shadow-lg hover:scale-[1.01]
    `}>
      <div className="flex items-center gap-3 mb-4">
        <span className="text-2xl">{style.icon}</span>
        <h2 className={`text-2xl font-bold ${style.titleColor}`}>
          {title}
        </h2>
      </div>
      
      <div className="prose prose-invert max-w-none">
        <div className="text-gray-300 leading-relaxed">
          {children}
        </div>
      </div>
    </div>
  );
}
