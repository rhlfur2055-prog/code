'use client';

import { ReactNode } from 'react';
import { Lightbulb, BookOpen, Wrench, FileText } from 'lucide-react';

interface SectionProps {
  title: string;
  children: ReactNode;
  variant?: 'concept' | 'theory' | 'practice' | 'note';
}

const variants = {
  concept: {
    icon: Lightbulb,
    gradient: 'from-blue-500/20 to-cyan-500/20',
    border: 'border-blue-500/30',
    iconColor: 'text-blue-400',
  },
  theory: {
    icon: BookOpen,
    gradient: 'from-purple-500/20 to-pink-500/20',
    border: 'border-purple-500/30',
    iconColor: 'text-purple-400',
  },
  practice: {
    icon: Wrench,
    gradient: 'from-green-500/20 to-emerald-500/20',
    border: 'border-green-500/30',
    iconColor: 'text-green-400',
  },
  note: {
    icon: FileText,
    gradient: 'from-yellow-500/20 to-orange-500/20',
    border: 'border-yellow-500/30',
    iconColor: 'text-yellow-400',
  },
};

export function Section({ title, children, variant = 'concept' }: SectionProps) {
  const config = variants[variant];
  const Icon = config.icon;

  return (
    <div
      className={`
        relative overflow-hidden rounded-xl border ${config.border}
        bg-gradient-to-br ${config.gradient} backdrop-blur-sm
        p-6 mb-6 transition-all duration-300
        hover:shadow-lg hover:shadow-black/20 hover:scale-[1.01]
      `}
    >
      <div className="flex items-start gap-4">
        <div className={`p-2 rounded-lg bg-gray-800/50 ${config.iconColor}`}>
          <Icon size={24} />
        </div>
        <div className="flex-1">
          <h2 className="text-xl font-bold text-white mb-3">{title}</h2>
          <div className="text-gray-300 leading-relaxed">{children}</div>
        </div>
      </div>
    </div>
  );
}
