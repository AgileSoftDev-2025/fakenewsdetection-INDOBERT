import { useState } from 'react';

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

  const handleToggleModel = (model:Model) => {
    if (activeModel === model.name) {
      setActiveModel(null);
      setToast({ type: 'success', message: `Model deactivated` });
    } else {
      setActiveModel(model.name);
      setToast({ type: 'success', message: `Model changed to version ${model.name}` });
    }
    setTimeout(() => setToast(null), 3000);
  };

  const models = [
    { id: 1, name: 'Version 1.0', description: 'Stable release for production' },
    { id: 2, name: 'Version 2.0', description: 'Beta release with new features' },
    { id: 3, name: 'Version 3.0', description: 'Experimental model' }
  ];

  return (
    <div className="min-h-screen p-6 bg-gray-50 relative">
      {toast && (
        <div className={`fixed top-4 right-4 px-4 py-2 rounded shadow-lg ${toast.type === 'success' ? 'bg-green-500' : 'bg-red-500'} text-white animate-slide-in-right`}>
          {toast.message}
        </div>
      )}
      <h1 className="text-2xl font-bold mb-4">Select Model</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {models.map((model) => (
          <div
            key={model.id}
            className={`p-4 rounded-xl border shadow-sm transition-transform transform hover:scale-[1.02] hover:shadow-md cursor-pointer ${
              activeModel === model.name ? 'border-blue-500 bg-blue-50' : 'border-gray-300 bg-white'
            }`}
          >
            <h2 className="text-lg font-semibold flex justify-between items-center">
              {model.name}
              {activeModel === model.name && <span className="text-sm bg-blue-500 text-white px-2 py-1 rounded">Currently Active</span>}
            </h2>
            <p className="text-sm text-gray-600 mt-2">{model.description}</p>
            <button
              onClick={() => handleToggleModel(model)}
              className="mt-4 px-4 py-2 rounded-lg border transition-all hover:bg-blue-500 hover:text-white text-sm"
            >
              {activeModel === model.name ? 'Deactivate' : 'Activate'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
