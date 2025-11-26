'use client';

import { useEffect, useState } from 'react';
import Header from '@/components/Header';
import StatsGrid from '@/components/StatsGrid';
import SystemGrid from '@/components/SystemGrid';

interface Stats {
  total: number;
  hoax: number;
  valid: number;
  hoax_percentage?: number;
  valid_percentage?: number;
}

export default function Home() {
  const [stats, setStats] = useState<Stats>({
    total: 0,
    hoax: 0,
    valid: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/admin/stats`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setStats(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching stats:', err);
      setError('Gagal memuat statistik. Pastikan backend berjalan.');
      // Use default data on error
      setStats({
        total: 0,
        hoax: 0,
        valid: 0
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      <Header />
      
      <div className="container max-w-7xl mx-auto px-4 py-8">
        {/* Page Header */}
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-2">Dashboard Admin</h2>
          <p className="text-gray-600">
            Kelola sistem deteksi hoax, pengguna, dan dataset untuk meningkatkan akurasi analisis.
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            <p className="font-medium">⚠️ {error}</p>
            <button 
              onClick={fetchStats}
              className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
            >
              Coba Lagi
            </button>
          </div>
        )}

        {/* Loading State */}
        {loading && !error && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
            <p className="mt-4 text-gray-600">Memuat data statistik...</p>
          </div>
        )}

        {/* Stats Grid */}
        {!loading && <StatsGrid stats={stats} />}

        {/* System Grid */}
        {!loading && <SystemGrid />}
      </div>
    </div>
  );
}
