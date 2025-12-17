'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

interface ModelMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
}

export default function SystemGrid() {
  const router = useRouter();
  const [modelVersion, setModelVersion] = useState<string>('v1');
  const [modelMetrics, setModelMetrics] = useState<ModelMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModelData();
  }, []);

  const fetchModelData = async () => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    try {
      // Fetch model version and metrics
      const [versionRes, metricsRes] = await Promise.all([
        fetch(`${apiUrl}/model/version`),
        fetch(`${apiUrl}/api/models/active`)
      ]);

      const versionData = await versionRes.json();
      const metricsData = await metricsRes.json();

      setModelVersion(versionData.version);
      if (metricsData.metrics) {
        setModelMetrics(metricsData.metrics);
      }
    } catch (error) {
      console.error('Failed to fetch model data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateModel = () => {
    router.push('/list-model');
  };

  const getMetricColor = (value: number) => {
    if (value >= 95) return 'from-green-500 to-emerald-500';
    if (value >= 90) return 'from-blue-500 to-cyan-500';
    if (value >= 85) return 'from-yellow-500 to-orange-500';
    return 'from-red-500 to-pink-500';
  };

  const MetricBar = ({ label, value }: { label: string; value: number }) => (
    <div className="mb-4 last:mb-0">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm font-medium text-gray-700">{label}</span>
        <span className="text-sm font-bold text-gray-900">{value}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
        <div
          className={`h-full bg-gradient-to-r ${getMetricColor(value)} transition-all duration-500 shadow-sm`}
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* System Overview */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-bold text-gray-800 mb-2">Sistem Overview</h3>
        <p className="text-sm text-gray-500 mb-6">
          Status kesehatan sistem dan infrastruktur
        </p>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-lg border border-purple-100">
            <div>
              <p className="text-xs text-gray-600 mb-1">Versi Model Aktif</p>
              <p className="text-2xl font-bold text-purple-700">{modelVersion}</p>
            </div>
            <div className="text-4xl">🧠</div>
          </div>

          <button
            onClick={handleUpdateModel}
            className="w-full inline-flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-4 py-3 rounded-lg font-medium hover:from-purple-700 hover:to-indigo-700 transition-all shadow-md hover:shadow-lg"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>Kelola Model</span>
          </button>
        </div>
      </div>

      {/* Model Performance */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-bold text-gray-800 mb-2">Performa Model</h3>
        <p className="text-sm text-gray-500 mb-6">
          Metrik performa model {modelVersion} yang sedang digunakan
        </p>
        
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mb-3"></div>
              <p className="text-sm text-gray-500">Memuat metrik...</p>
            </div>
          </div>
        ) : modelMetrics ? (
          <div className="space-y-3">
            <MetricBar label="Akurasi" value={modelMetrics.accuracy} />
            <MetricBar label="Presisi" value={modelMetrics.precision} />
            <MetricBar label="Recall" value={modelMetrics.recall} />
            <MetricBar label="F1-Score" value={modelMetrics.f1} />
          </div>
        ) : (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="text-5xl mb-3">⚠️</div>
              <p className="text-sm text-gray-500 font-medium">Gagal memuat metrik</p>
              <button 
                onClick={fetchModelData}
                className="mt-4 text-sm text-purple-600 hover:text-purple-700 font-medium"
              >
                Coba Lagi
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
