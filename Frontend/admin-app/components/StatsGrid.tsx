'use client';

import { useEffect, useState } from 'react';
import StatCard from './StatCard';

interface StatsGridProps {
  stats: {
    total: number;
    hoax: number;
    valid: number;
  };
}

export default function StatsGrid({ stats }: StatsGridProps) {
  const hoaxPercentage = Math.round((stats.hoax / stats.total) * 100);
  const validPercentage = Math.round((stats.valid / stats.total) * 100);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <StatCard
        title="Total Pengecekan"
        value={stats.total}
        subtitle="Berita yang telah dianalisis"
        icon="📄"
      />
      <StatCard
        title="Hoax Terdeteksi"
        value={stats.hoax}
        subtitle={`${hoaxPercentage}% dari total`}
        icon="⊗"
        variant="error"
      />
      <StatCard
        title="Berita Valid"
        value={stats.valid}
        subtitle={`${validPercentage}% dari total`}
        icon="✓"
        variant="success"
      />
    </div>
  );
}
