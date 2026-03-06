import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Topbar from './components/Topbar';
import Dashboard from './components/Dashboard';
import UploadModal from './components/UploadModal';

const API_URL = import.meta.env.VITE_API_URL || '/api';

function App() {
  const [data, setData] = useState({
    colaboradores: [],
    ferias: [],
    exames: [],
    esocial: [],
    history: []
  });
  const [showUpload, setShowUpload] = useState(false);
  const [currentPage, setCurrentPage] = useState('dashboard');

  const fetchData = async () => {
    try {
      const [col, fer, exa, eso, his] = await Promise.all([
        fetch(`${API_URL}/colaboradores`).then(r => r.json()),
        fetch(`${API_URL}/ferias`).then(r => r.json()),
        fetch(`${API_URL}/exames`).then(r => r.json()),
        fetch(`${API_URL}/esocial`).then(r => r.json()),
        fetch(`${API_URL}/history`).then(r => r.json())
      ]);
      setData({ colaboradores: col, ferias: fer, exames: exa, esocial: eso, history: his });
    } catch (error) {
      console.error('Error:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="flex min-h-screen" style={{background: 'var(--bg)'}}>
      <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} onUpload={() => setShowUpload(true)} />
      
      <div className="flex-1 ml-[230px]">
        <Topbar onUpload={() => setShowUpload(true)} />
        <Dashboard data={data} currentPage={currentPage} />
      </div>

      {showUpload && (
        <UploadModal
          onClose={() => setShowUpload(false)}
          onSuccess={() => { fetchData(); setShowUpload(false); }}
        />
      )}
    </div>
  );
}

export default App;
