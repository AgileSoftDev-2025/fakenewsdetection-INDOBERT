'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Model {
  id: number;
  name: string;
  description: string;
  version: string;
  metrics: { 
    accuracy: number; 
    precision: number; 
    recall: number; 
    f1: number; 
  };
}

interface Toast {
  type: 'success' | 'error';
  message: string;
}

const TOAST_DURATION = 4000;

export default function ListModelAI() {
  const router = useRouter();
  const [models, setModels] = useState<Model[]>([]);
  const [activeModel, setActiveModel] = useState<string | null>(null);
  const [toast, setToast] = useState<Toast | null>(null);
  const [loading, setLoading] = useState(true);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchModels();
    fetchActiveModel();
  }, [apiUrl]);

  const fetchModels = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/models`);
      const data = await response.json();
      setModels(data);
    } catch (err) {
      console.error("Failed to load models", err);
      showToast('error', 'Gagal memuat daftar model');
    } finally {
      setLoading(false);
    }
  };

  const fetchActiveModel = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/models/active`);
      const data = await response.json();
      setActiveModel(data.active_model);
    } catch (err) {
      console.error("Failed to get active model", err);
    }
  };

  const showToast = (type: 'success' | 'error', message: string) => {
    setToast({ type, message });
    setTimeout(() => setToast(null), TOAST_DURATION);
  };

  const handleToggle = async (model: Model) => {
    try {
      if (activeModel === model.version) {
        await fetch(`${apiUrl}/api/models/deactivate`, { method: "POST" });
        setActiveModel("v1");
        showToast('success', `Model ${model.version} dinonaktifkan, kembali ke v1`);
      } else {
        const response = await fetch(`${apiUrl}/api/models/${model.version}/activate`, {
          method: "POST",
        });
        
        if (!response.ok) throw new Error('Failed to activate model');
        
        setActiveModel(model.version);
        showToast('success', `Model berhasil diubah ke ${model.version}`);
      }
    } catch (error) {
      console.error(error);
      showToast('error', 'Gagal berkomunikasi dengan server');
    }
  };

  const getMetricColor = (value: number) => {
    if (value >= 95) return 'from-green-500 to-emerald-500';
    if (value >= 90) return 'from-blue-500 to-cyan-500';
    if (value >= 85) return 'from-yellow-500 to-orange-500';
    return 'from-red-500 to-pink-500';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
        <header className="bg-white shadow-sm">
          <div className="px-8 py-4 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gray-900 rounded-lg flex items-center justify-center text-white text-xl">
                ◉
              </div>
              <div>
                <h1 className="text-base font-semibold">FakeNewsDetector Admin</h1>
                <p className="text-xs text-gray-600">Panel Administrasi</p>
              </div>
            </div>
          </div>
        </header>
        <div className="flex items-center justify-center py-24">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mb-4"></div>
            <p className="text-gray-600 font-medium">Memuat data model...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="px-8 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gray-900 rounded-lg flex items-center justify-center text-white text-xl">
              ◉
            </div>
            <div>
              <h1 className="text-base font-semibold">FakeNewsDetector Admin</h1>
              <p className="text-xs text-gray-600">Panel Administrasi</p>
            </div>
          </div>
          <button
            onClick={() => router.push('/')}
            className="flex items-center gap-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors font-medium"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            <span>Kembali</span>
          </button>
        </div>
      </header>

      {/* Toast Notification */}
      {toast && (
        <div className="fixed top-20 right-6 z-50 animate-slide-in">
          <div className={`px-6 py-4 rounded-lg shadow-lg ${
            toast.type === 'success' 
              ? 'bg-green-500 text-white' 
              : 'bg-red-500 text-white'
          }`}>
            <div className="flex items-center gap-3">
              <span className="text-2xl">
                {toast.type === 'success' ? '✅' : '⚠️'}
              </span>
              <span className="font-medium">{toast.message}</span>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="container max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-800 mb-2">Pilih Model</h2>
          <p className="text-gray-600">Aktifkan model yang ingin digunakan untuk deteksi berita hoax</p>
        </div>

        <div className="grid grid-cols-1 gap-6">
          {models.map((model) => {
            const isActive = activeModel === model.version;
            
            return (
              <div
                key={model.id}
                className={`bg-white rounded-xl p-6 shadow-sm border-2 transition-all cursor-pointer hover:shadow-md ${
                  isActive 
                    ? 'border-blue-500 shadow-lg' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-bold text-gray-800">{model.name}</h3>
                      <span className="px-3 py-1 bg-gray-100 text-gray-700 text-sm font-medium rounded-full">
                        {model.version}
                      </span>
                      {isActive && (
                        <span className="px-3 py-1 bg-blue-500 text-white text-sm font-medium rounded-full flex items-center gap-1">
                          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                          </svg>
                          Aktif
                        </span>
                      )}
                    </div>
                    <p className="text-gray-600 text-sm">{model.description}</p>
                  </div>
                </div>

                {/* Metrics with Progress Bars */}
                <div className="grid grid-cols-2 gap-4 mb-6">
                  {[
                    { label: 'Akurasi', value: model.metrics.accuracy },
                    { label: 'Presisi', value: model.metrics.precision },
                    { label: 'Recall', value: model.metrics.recall },
                    { label: 'F1-Score', value: model.metrics.f1 },
                  ].map((metric) => (
                    <div key={metric.label}>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium text-gray-700">{metric.label}</span>
                        <span className="text-sm font-bold text-gray-900">{metric.value}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
                        <div
                          className={`h-full bg-gradient-to-r ${getMetricColor(metric.value)} transition-all duration-500`}
                          style={{ width: `${metric.value}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>

                {/* Action Button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleToggle(model);
                  }}
                  className={`w-full py-3 px-4 rounded-lg font-medium transition-all shadow-md hover:shadow-lg ${
                    isActive
                      ? 'bg-gradient-to-r from-red-500 to-pink-500 text-white hover:from-red-600 hover:to-pink-600'
                      : 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white hover:from-purple-700 hover:to-indigo-700'
                  }`}
                >
                  {isActive ? "Nonaktifkan" : "Aktifkan"}
                </button>
              </div>
            );
          })}
        </div>

        {/* Save Button - Bottom Fixed */}
        <div className="fixed bottom-6 right-6">
          <button
            onClick={() => showToast('success', 'Perubahan tersimpan otomatis')}
            disabled={!activeModel}
            className="flex items-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-lg font-medium shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed hover:from-blue-700 hover:to-indigo-700"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
            </svg>
            <span>Simpan Perubahan</span>
          </button>
        </div>
      </div>
    </div>
  );
}
