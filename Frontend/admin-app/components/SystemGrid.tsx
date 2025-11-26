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

  const MetricRow = ({ label, value }: { label: string; value: number }) => (
    <div className="flex justify-between items-center text-sm">
      <span className="text-gray-600">{label}:</span>
      <span className="font-semibold text-purple-600">{value}%</span>
    </div>
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* System Overview */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-base font-semibold">Sistem Overview</h3>
          <button
            onClick={handleUpdateModel}
            className="inline-flex items-center gap-2 bg-purple-100 text-purple-700 px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-purple-200 transition-colors"
          >
            <span>🧠</span>
            <span>Update Model</span>
          </button>
        </div>
        <p className="text-sm text-gray-600 mb-4">
          Status kesehatan sistem dan infrastruktur
        </p>
        <div className="text-sm">
          <span className="text-gray-600">Versi model aktif:</span>
          <span className="ml-2 text-lg font-bold text-purple-600">{modelVersion}</span>
        </div>
      </div>

      {/* Model Performance */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <h3 className="text-base font-semibold mb-2">Performa Model</h3>
        <p className="text-sm text-gray-600 mb-4">
          Metrik performa model {modelVersion} yang sedang digunakan
        </p>
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="text-gray-400 text-center">
              <div className="text-2xl mb-2">📊</div>
              <p className="text-sm">Memuat metrik...</p>
            </div>
          </div>
        ) : modelMetrics ? (
          <div className="space-y-2">
            <MetricRow label="Akurasi" value={modelMetrics.accuracy} />
            <MetricRow label="Presisi" value={modelMetrics.precision} />
            <MetricRow label="Recall" value={modelMetrics.recall} />
            <MetricRow label="F1-Score" value={modelMetrics.f1} />
          </div>
        ) : (
          <div className="flex items-center justify-center py-8">
            <div className="text-gray-400 text-center">
              <div className="text-2xl mb-2">⚠️</div>
              <p className="text-sm">Gagal memuat metrik</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
