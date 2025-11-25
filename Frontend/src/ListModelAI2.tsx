import { useState } from 'react';
import styles from './ListModelAI3.module.css';
import { FaSignOutAlt } from 'react-icons/fa';

interface Toast {
  type: 'success' | 'error';
  message: string;
}

interface Model {
  id: number;
  name: string;
  description: string;
  version: string;
  metrics: { accuracy: number; precision: number; recall: number; f1: number };
}

export default function ListModelAI() {
  const [activeModel, setActiveModel] = useState<string | null>(null);
  const [toast, setToast] = useState<Toast | null>(null);

  const models: Model[] = [
    { id: 1, name: 'ML Model', version: 'v1.0', description: 'Stable release for production', metrics: { accuracy: 89, precision: 84, recall: 87, f1: 86 } },
    { id: 2, name: 'ML Model', version: 'v2.0', description: 'Improved contextual accuracy and reduced bias', metrics: { accuracy: 91, precision: 90, recall: 88, f1: 89 } },
    { id: 3, name: 'ML Model', version: 'v3.0', description: 'Added linguistic normalization features', metrics: { accuracy: 93, precision: 92, recall: 91, f1: 92 } },
    { id: 4, name: 'ML Model', version: 'v4.0', description: 'Enhanced IndoBERT fine-tuning for better generalization', metrics: { accuracy: 95, precision: 94, recall: 93, f1: 94 } },
  ];

  const handleToggleModel = (model: Model) => {
    if (activeModel === model.version) {
      setActiveModel(null);
      setToast({ type: 'success', message: `Model ${model.version} deactivated` });
    } else {
      setActiveModel(model.version);
      setToast({ type: 'success', message: `Model changed to ${model.version}` });
    }
    setTimeout(() => setToast(null), 5000);
  };

  return (
    <div className={styles.container}>
      {/* === Header === */}
      <header className={styles.header}>
        <h1 className={styles.headerTitle}>FakeNewsDetector Admin</h1>
        <div className={styles.headerActions}>
          <button className={styles.backButton} data-testid="back-btn">← Kembali</button>
          <button className={styles.logoutButton} data-testid="logout-btn">
            <FaSignOutAlt /> Keluar
          </button>
        </div>
      </header>

      {/* === Toast Feedback === */}
      {toast && (
        <div
          data-testid="toast"
          className={`${styles.toast} ${toast.type === 'success' ? styles.success : styles.error}`}
        >
          {toast.message}
        </div>
      )}

      {/* === Title === */}
      <h2 className={styles.sectionTitle}>Pilih Model</h2>

      {/* === Model Cards === */}
      <div className={styles.cardGrid} data-testid="model-grid">
        {models.map((model) => (
          <div
            key={model.id}
            data-testid={`model-card-${model.version}`}
            className={`${styles.card} card ${activeModel === model.version ? styles.activeCard : ''}`}
            onClick={() => handleToggleModel(model)}
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

            {/* Buttons inside card */}
            <button
              className={`${styles.toggleButton} ${
                activeModel === model.version ? styles.deactivateButton : styles.activateButton
              }`}
              data-testid={`toggle-btn-${model.version}`}
              onClick={(e) => {
                e.stopPropagation();
                handleToggleModel(model);
              }}
            >
              {activeModel === model.version ? 'Nonaktifkan' : 'Aktifkan'}
            </button>
          </div>
        ))}
      </div>

      {/* === Footer === */}
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
