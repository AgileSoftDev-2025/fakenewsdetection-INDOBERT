import { useState, useEffect } from 'react';
import styles from './ListModelAI3.module.css';
import { FaSignOutAlt } from 'react-icons/fa';

interface Model {
  id: number;
  name: string;
  description: string;
  version: string;
  metrics: { accuracy: number; precision: number; recall: number; f1: number };
}

interface Toast {
  type: 'success' | 'error';
  message: string;
}

export default function ListModelAI() {
  const [models, setModels] = useState<Model[]>([]);
  const [activeModel, setActiveModel] = useState<string | null>(null);
  const [toast, setToast] = useState<Toast | null>(null);

  // === GET MODELS FROM BACKEND ===
  useEffect(() => {
    fetch("http://localhost:8000/api/models")
      .then((res) => res.json())
      .then((data) => setModels(data))
      .catch(() => console.error("Failed to load models"));
  }, []);

  // === GET ACTIVE MODEL ===
  useEffect(() => {
    fetch("http://localhost:8000/api/models/active")
      .then((res) => res.json())
      .then((data) => setActiveModel(data.active_model))
      .catch(() => console.error("Failed to get active model"));
  }, []);

  // === ACTIVATE / DEACTIVATE MODEL ===
  const handleToggle = async (model: Model) => {
    try {
      if (activeModel === model.version) {
        // DEACTIVATE
        await fetch("http://localhost:8000/api/models/deactivate", {
          method: "POST",
        });
        setActiveModel(null);
        setToast({ type: "success", message: `Model ${model.version} deactivated` });
      } else {
        // ACTIVATE
        await fetch(`http://localhost:8000/api/models/${model.version}/activate`, {
          method: "POST",
        });
        setActiveModel(model.version);
        setToast({ type: "success", message: `Model changed to ${model.version}` });
      }

      setTimeout(() => setToast(null), 4000);
    } catch (error) {
      setToast({ type: "error", message: "Failed to communicate with server" });
    }
  };

  return (
    <div className={styles.container}>
      {/* === HEADER === */}
      <header className={styles.header}>
        <h1 className={styles.headerTitle}>FakeNewsDetector Admin</h1>
        <div className={styles.headerActions}>
          <button className={styles.backButton} data-testid="back-btn">← Kembali</button>
          <button className={styles.logoutButton} data-testid="logout-btn">
            <FaSignOutAlt /> Keluar
          </button>
        </div>
      </header>

      {/* === TOAST === */}
      {toast && (
        <div
          data-testid="toast"
          className={`${styles.toast} ${
            toast.type === 'success' ? styles.success : styles.error
          }`}
        >
          {toast.message}
        </div>
      )}

      {/* === PAGE TITLE === */}
      <h2 className={styles.sectionTitle}>Pilih Model</h2>

      {/* === MODEL CARDS === */}
      <div className={styles.cardGrid} data-testid="model-grid">
        {models.map((model) => (
          <div
            key={model.id}
            data-testid={`model-card-${model.version}`}
            className={`${styles.card} card ${
              activeModel === model.version ? styles.activeCard : ''
            }`}
            onClick={() => handleToggle(model)}
          >
            <div className={styles.cardHeader}>
              <h3 className={styles.cardTitle}>{model.name}</h3>
              <p className={styles.modelVersion}>{model.version}</p>

              {activeModel === model.version && (
                <span className={styles.activeBadge} data-testid="active-badge">
                  Aktif
                </span>
              )}
            </div>

            <p className={styles.cardDescription}>{model.description}</p>

            {/* METRICS */}
            <div className={styles.metrics}>
              {[
                { label: 'Akurasi', value: model.metrics.accuracy },
                { label: 'Presisi', value: model.metrics.precision },
                { label: 'Recall', value: model.metrics.recall },
                { label: 'F1-Score', value: model.metrics.f1 },
              ].map((m) => (
                <div key={m.label} className={styles.metricBar}>
                  <label>{m.label}</label>
                  <div className={styles.bar}>
                    <div style={{ width: `${m.value}%` }}></div>
                  </div>
                  <span>{m.value}%</span>
                </div>
              ))}
            </div>

            {/* BUTTON */}
            <button
              className={`${styles.toggleButton} ${
                activeModel === model.version
                  ? styles.deactivateButton
                  : styles.activateButton
              }`}
              data-testid={`toggle-btn-${model.version}`}
              onClick={(e) => {
                e.stopPropagation();
                handleToggle(model);
              }}
            >
              {activeModel === model.version ? "Nonaktifkan" : "Aktifkan"}
            </button>
          </div>
        ))}
      </div>

      {/* === FOOTER === */}
      <div className={styles.footer}>
        <button
          className={styles.saveButton}
          data-testid="save-btn"
          disabled={!activeModel}
        >
          💾 Simpan Perubahan
        </button>
      </div>
    </div>
  );
}
