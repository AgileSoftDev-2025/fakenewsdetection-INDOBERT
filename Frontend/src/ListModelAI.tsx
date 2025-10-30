import { useState } from 'react';
import styles from './ListModelAI2.module.css';

interface Toast {
  type: 'success' | 'error';
  message: string;
}

interface Model {
  id: number;
  name: string;
  description: string;
}

export default function ListModelAI() {
  const [activeModel, setActiveModel] = useState<string | null>(null);
  const [toast, setToast] = useState<Toast | null>(null);

  const models: Model[] = [
    { id: 1, name: 'Version 1.0', description: 'Stable release for production' },
    { id: 2, name: 'Version 2.0', description: 'Beta release with new features' },
    { id: 3, name: 'Version 3.0', description: 'Experimental model' }
  ];

  const handleToggleModel = (model: Model) => {
    if (activeModel === model.name) {
      setActiveModel(null);
      setToast({ type: 'success', message: 'Model deactivated' });
    } else {
      setActiveModel(model.name);
      setToast({ type: 'success', message: `Model changed to ${model.name}` });
    }
    setTimeout(() => setToast(null), 8000);
  };

  return (
    <div className={styles.container}>
      {toast && (
        <div className={`${styles.toast} ${toast.type === 'success' ? styles.success : styles.error}`}>
          {toast.message}
        </div>
      )}

      <h1 className={styles.title}>Pilih Model AI</h1>

      <div className={styles.cardGrid}>
        {models.map((model) => (
          <div
            key={model.id}
            className={`${styles.card} ${activeModel === model.name ? styles.activeCard : ''}`}
          >
            <h2 className={styles.cardTitle}>
              {model.name}
              {activeModel === model.name && <span className={styles.activeBadge}>Aktif</span>}
            </h2>
            <p className={styles.cardDescription}>{model.description}</p>
            <button
              onClick={() => handleToggleModel(model)}
              className={`${styles.button} ${activeModel === model.name ? styles.deactivateButton : ''}`}
            >
              {activeModel === model.name ? 'Nonaktifkan' : 'Aktifkan'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
