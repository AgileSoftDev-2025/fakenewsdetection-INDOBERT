'use client';

import { useEffect, useState } from 'react';
import useSWR from 'swr';
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

interface RetrainProgress {
  is_running: boolean;
  progress: number;
  stage: string;
  message: string;
  started_at: number | null;
  estimated_completion: number | null;
  current_epoch: number | null;
  total_epochs: number | null;
  error: string | null;
}

export default function Home() {
  const [stats, setStats] = useState<Stats>({
    total: 0,
    hoax: 0,
    valid: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [elapsedTime, setElapsedTime] = useState<string>('00:00:00');
  const [estimatedRemaining, setEstimatedRemaining] = useState<string>('--:--:--');
  const [startingRetrain, setStartingRetrain] = useState(false);
  const [resettingProgress, setResettingProgress] = useState(false);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  // Fetch retrain progress
  const fetcher = (url: string) => fetch(url).then((res) => res.json());
  const { data: progressData } = useSWR<RetrainProgress>(
    `${apiUrl}/retrain/progress`,
    fetcher,
    { refreshInterval: 2000 }
  );

  useEffect(() => {
    fetchStats();
  }, []);

  useEffect(() => {
    if (!progressData?.is_running || !progressData.started_at) {
      setElapsedTime('00:00:00');
      setEstimatedRemaining('--:--:--');
      return;
    }

    const interval = setInterval(() => {
      const now = Date.now() / 1000;
      const elapsed = progressData.started_at ? now - progressData.started_at : 0;
      setElapsedTime(formatDuration(elapsed));

      if (progressData.estimated_completion) {
        const remaining = Math.max(0, progressData.estimated_completion - now);
        setEstimatedRemaining(formatDuration(remaining));
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [progressData]);

  const formatDuration = (seconds: number): string => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  };

  const getStageColor = (stage: string): string => {
    const colors: Record<string, string> = {
      idle: 'bg-gray-100 text-gray-700',
      preparing: 'bg-blue-100 text-blue-700',
      training: 'bg-purple-100 text-purple-700',
      evaluating: 'bg-yellow-100 text-yellow-700',
      saving: 'bg-indigo-100 text-indigo-700',
      uploading: 'bg-cyan-100 text-cyan-700',
      completed: 'bg-green-100 text-green-700',
      failed: 'bg-red-100 text-red-700'
    };
    return colors[stage] || 'bg-gray-100 text-gray-700';
  };

  const getStageIcon = (stage: string): string => {
    const icons: Record<string, string> = {
      idle: '',
      preparing: '',
      training: '',
      evaluating: '',
      saving: '',
      uploading: '',
      completed: '',
      failed: ''
    };
    return icons[stage] || '';
  };

  const fetchStats = async () => {
    try {
      setLoading(true);
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
      setStats({ total: 0, hoax: 0, valid: 0 });
    } finally {
      setLoading(false);
    }
  };

  const startRetrain = async () => {
    try {
      setStartingRetrain(true);
      const response = await fetch(`${apiUrl}/retrain/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Gagal memulai retrain');
      }

      const data = await response.json();
      alert(data.message || 'Retrain berhasil dimulai!');
    } catch (err: any) {
      console.error('Error starting retrain:', err);
      alert(err.message || 'Gagal memulai retrain. Pastikan backend berjalan.');
    } finally {
      setStartingRetrain(false);
    }
  };

  const resetProgress = async () => {
    if (!confirm('Apakah Anda yakin ingin reset status retrain? Progress yang sedang berjalan akan dibatalkan.')) {
      return;
    }

    try {
      setResettingProgress(true);
      const response = await fetch(`${apiUrl}/retrain/reset`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Gagal reset progress');
      }

      const data = await response.json();
      alert(data.message || 'Progress berhasil direset!');
      // Reload page to refresh data
      window.location.reload();
    } catch (err: any) {
      console.error('Error resetting progress:', err);
      alert(err.message || 'Gagal reset progress. Pastikan backend berjalan.');
    } finally {
      setResettingProgress(false);
    }
  };

  return (
    <div className="min-h-screen">
      <Header />
      
      <div className="container max-w-7xl mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-2">Dashboard Admin</h2>
          <p className="text-gray-600">
            Kelola sistem deteksi hoax, pengguna, dan dataset untuk meningkatkan akurasi analisis.
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            <p className="font-medium"> {error}</p>
            <button 
              onClick={fetchStats}
              className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
            >
              Coba Lagi
            </button>
          </div>
        )}

        {loading && !error && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
            <p className="mt-4 text-gray-600">Memuat data statistik...</p>
          </div>
        )}

        {!loading && <StatsGrid stats={stats} />}

        {!loading && progressData && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-6 border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-gray-800">Status Retrain Model</h3>
              <div className="flex items-center gap-3">
                {progressData.is_running && (
                  <button
                    onClick={resetProgress}
                    disabled={resettingProgress}
                    className="px-3 py-1 text-xs font-medium text-red-600 hover:text-red-700 hover:bg-red-50 rounded-md transition-colors"
                  >
                    {resettingProgress ? 'Resetting...' : '🔄 Reset'}
                  </button>
                )}
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStageColor(progressData.stage)}`}>
                  {getStageIcon(progressData.stage)} {progressData.stage.toUpperCase()}
                </span>
              </div>
            </div>

            {/* Info Note - Training only on local */}
            <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <div className="flex items-start">
                <span className="text-yellow-600 text-lg mr-2">ℹ️</span>
                <div className="text-sm text-yellow-800">
                  <p className="font-medium">Catatan Penting:</p>
                  <p className="mt-1">
                    Training model hanya dilakukan di <strong>local laptop dengan GPU</strong>. 
                    Setelah training selesai, model akan di-upload ke <strong>Hugging Face Repository</strong> 
                    untuk digunakan oleh aplikasi di production.
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">Progress</span>
                <span className="text-sm font-bold text-gray-900">{progressData.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                <div
                  className={`h-full transition-all duration-500 ${
                    progressData.is_running
                      ? 'bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 animate-pulse'
                      : progressData.stage === 'completed'
                      ? 'bg-green-500'
                      : progressData.stage === 'failed'
                      ? 'bg-red-500'
                      : 'bg-gray-400'
                  }`}
                  style={{ width: `${progressData.progress}%` }}
                />
              </div>
            </div>

            <div className="mb-4">
              <p className="text-sm text-gray-600">
                {progressData.is_running && ' '}
                {progressData.message || 'Tidak ada proses retrain yang sedang berjalan'}
              </p>
            </div>

            {progressData.is_running && progressData.current_epoch !== null && progressData.total_epochs !== null && (
              <div className="mb-4 p-3 bg-purple-50 rounded-lg border border-purple-200">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-purple-700">Epoch Progress</span>
                  <span className="text-sm font-bold text-purple-900">
                    {progressData.current_epoch} / {progressData.total_epochs}
                  </span>
                </div>
              </div>
            )}

            {progressData.is_running && (
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                  <div className="text-xs text-blue-600 mb-1">Waktu Berjalan</div>
                  <div className="text-lg font-mono font-bold text-blue-900">{elapsedTime}</div>
                </div>
                <div className="p-3 bg-green-50 rounded-lg border border-green-200">
                  <div className="text-xs text-green-600 mb-1">Estimasi Tersisa</div>
                  <div className="text-lg font-mono font-bold text-green-900">{estimatedRemaining}</div>
                </div>
              </div>
            )}

            {progressData.error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-start">
                  <span className="text-red-500 mr-2"></span>
                  <div>
                    <p className="text-sm font-medium text-red-800">Error</p>
                    <p className="text-sm text-red-700 mt-1">{progressData.error}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Manual Retrain Button - Only show when idle or completed */}
            {!progressData.is_running && (progressData.stage === 'idle' || progressData.stage === 'completed' || progressData.stage === 'failed') && (
              <div className="mt-6 pt-6 border-t border-gray-200">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-gray-600">
                    <p className="font-medium">Training manual diperlukan untuk meningkatkan akurasi model</p>
                    <p className="text-xs mt-1">Pastikan Anda menjalankan backend di local dengan GPU tersedia</p>
                  </div>
                  <button
                    onClick={startRetrain}
                    disabled={startingRetrain}
                    className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center ${
                      startingRetrain
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white shadow-lg hover:shadow-xl'
                    }`}
                  >
                    {startingRetrain ? (
                      <>
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Memulai...
                      </>
                    ) : (
                      <>
                        <span className="mr-2">🚀</span>
                        Mulai Retrain
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* System Grid with proper spacing */}
        <div className={!loading && progressData ? 'mt-12' : 'mt-0'}>
          {!loading && <SystemGrid />}
        </div>
      </div>
    </div>
  );
}
