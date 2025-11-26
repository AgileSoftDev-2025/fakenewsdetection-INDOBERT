'use client';

import { useState, useEffect } from 'react';
import styles from './styles.module.css';

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
  const [models, setModels] = useState<Model[]>([]);
  const [activeModel, setActiveModel] = useState<string | null>(null);
  const [toast, setToast] = useState<Toast | null>(null);
  const [loading, setLoading] = useState(true);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  // Fetch models on mount
  useEffect(() => {
    fetchModels();
  }, [apiUrl]);

  // Fetch active model on mount
  useEffect(() => {
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
        // Deactivate current model
        await fetch(`${apiUrl}/api/models/deactivate`, {
          method: "POST",
        });
        setActiveModel("v1");
        showToast('success', `Model ${model.version} dinonaktifkan, kembali ke v1`);
      } else {
        // Activate selected model
        const response = await fetch(`${apiUrl}/api/models/${model.version}/activate`, {
          method: "POST",
        });
        
        if (!response.ok) {
          throw new Error('Failed to activate model');
        }
        
        setActiveModel(model.version);
        showToast('success', `Model berhasil diubah ke ${model.version}`);
      }
    } catch (error) {
      console.error(error);
      showToast('error', 'Gagal berkomunikasi dengan server');
    }
  };

  if (loading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <div className={styles.spinner}></div>
          <p>Memuat data model...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1 className={styles.headerTitle}>FakeNewsDetector Admin</h1>
      </header>

      {toast && (
        <div className={`${styles.toast} ${toast.type === 'success' ? styles.success : styles.error}`}>
          {toast.message}
        </div>
      )}

      <h2 className={styles.sectionTitle}>Pilih Model</h2>

      <div className={styles.cardGrid}>
        {models.map((model) => {
          const isActive = activeModel === model.version;
          
          return (
            <div
              key={model.id}
              className={`${styles.card} ${isActive ? styles.activeCard : ''}`}
              onClick={() => handleToggle(model)}
            >
              <div className={styles.cardHeader}>
                <h3 className={styles.cardTitle}>{model.name}</h3>
                <p className={styles.modelVersion}>{model.version}</p>
                {isActive && (
                  <span className={styles.activeBadge}>Aktif</span>
                )}
              </div>

              <p className={styles.cardDescription}>{model.description}</p>

              <div className={styles.metrics}>
                {[
                  { label: 'Akurasi', value: model.metrics.accuracy },
                  { label: 'Presisi', value: model.metrics.precision },
                  { label: 'Recall', value: model.metrics.recall },
                  { label: 'F1-Score', value: model.metrics.f1 },
                ].map((metric) => (
                  <div key={metric.label} className={styles.metricBar}>
                    <label>{metric.label}</label>
                    <div className={styles.bar}>
                      <div style={{ width: `${metric.value}%` }} />
                    </div>
                    <span>{metric.value}%</span>
                  </div>
                ))}
              </div>

              <button
                className={`${styles.toggleButton} ${
                  isActive ? styles.deactivateButton : styles.activateButton
                }`}
                onClick={(e) => {
                  e.stopPropagation();
                  handleToggle(model);
                }}
              >
                {isActive ? "Nonaktifkan" : "Aktifkan"}
              </button>
            </div>
          );
        })}
      </div>

      <div className={styles.footer}>
        <button
          className={styles.saveButton}
          disabled={!activeModel}
        >
          💾 Simpan Perubahan
        </button>
      </div>
    </div>
  );
}
