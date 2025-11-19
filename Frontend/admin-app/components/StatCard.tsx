'use client';

import { useEffect, useState } from 'react';

interface StatCardProps {
  title: string;
  value: number;
  subtitle: string;
  icon: string;
  variant?: 'default' | 'error' | 'success';
}

export default function StatCard({ title, value, subtitle, icon, variant = 'default' }: StatCardProps) {
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = value;
    const duration = 2000; // 2 seconds
    const increment = Math.ceil(end / 20);
    
    const timer = setInterval(() => {
      start += increment;
      if (start >= end) {
        setDisplayValue(end);
        clearInterval(timer);
      } else {
        setDisplayValue(start);
      }
    }, 100);

    return () => clearInterval(timer);
  }, [value]);

  const valueColorClass = 
    variant === 'error' ? 'text-red-500' : 
    variant === 'success' ? 'text-green-500' : 
    'text-gray-900';

  const iconColorClass = 
    variant === 'error' ? 'text-red-500' : 
    variant === 'success' ? 'text-green-500' : 
    'text-gray-600';

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <span className="text-sm font-medium text-gray-600">{title}</span>
        <span className={`text-2xl ${iconColorClass}`}>{icon}</span>
      </div>
      <div className={`text-4xl font-bold mb-1 ${valueColorClass}`}>
        {displayValue.toLocaleString('id-ID')}
      </div>
      <div className="text-sm text-gray-500">{subtitle}</div>
    </div>
  );
}
