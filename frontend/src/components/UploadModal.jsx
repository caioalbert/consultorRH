import { useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || '/api';

export default function UploadModal({ onClose, onSuccess }) {
  const [type, setType] = useState('colaboradores');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch(`${API_URL}/upload/${type}`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      
      if (data.success) {
        alert(`✓ ${data.count} registros importados com sucesso!`);
        onSuccess();
      } else {
        alert('Erro ao importar: ' + (data.error || 'Erro desconhecido'));
      }
    } catch (error) {
      alert('Erro ao fazer upload: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="bg-[#111622] border border-white/10 rounded-2xl w-full max-w-2xl">
        <div className="px-6 py-4 border-b border-white/5 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">Importar CSV</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white">✕</button>
        </div>

        <div className="p-6 space-y-4">
          {/* Type selector */}
          <div className="flex gap-2 bg-[#0b0f1a] p-1 rounded-lg">
            {['colaboradores', 'ferias', 'exames', 'esocial'].map(t => (
              <button
                key={t}
                onClick={() => setType(t)}
                className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition ${
                  type === t ? 'bg-[#1a2235] text-white' : 'text-gray-400 hover:text-white'
                }`}
              >
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>

          {/* File upload */}
          <div className="border-2 border-dashed border-white/10 rounded-xl p-8 text-center hover:border-blue-500/50 transition">
            <input
              type="file"
              accept=".csv"
              onChange={(e) => setFile(e.target.files[0])}
              className="hidden"
              id="file-input"
            />
            <label htmlFor="file-input" className="cursor-pointer">
              <div className="text-4xl mb-3">📂</div>
              <div className="text-white font-medium mb-1">
                {file ? file.name : 'Clique para selecionar CSV'}
              </div>
              <div className="text-sm text-gray-400">
                Formato: CSV com separador vírgula ou ponto-e-vírgula
              </div>
            </label>
          </div>

          {/* Template hint */}
          <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-3 text-sm text-blue-300">
            💡 <strong>{type}:</strong> Certifique-se que o CSV contém as colunas corretas
          </div>

          {/* Actions */}
          <div className="flex gap-3 justify-end">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-lg text-sm font-medium text-gray-400 hover:text-white transition"
            >
              Cancelar
            </button>
            <button
              onClick={handleUpload}
              disabled={!file || uploading}
              className="px-4 py-2 rounded-lg text-sm font-medium bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {uploading ? 'Importando...' : '✓ Confirmar'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
