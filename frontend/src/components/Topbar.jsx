export default function Topbar({ onUpload }) {
  const today = new Date().toLocaleDateString('pt-BR', { 
    weekday: 'short', 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });

  return (
    <header className="h-[60px] sticky top-0 z-40 flex items-center px-7 gap-4" style={{background: 'var(--bg2)', borderBottom: '1px solid var(--border)'}}>
      <div>
        <div className="text-[15px] font-semibold tracking-tight">Dashboard</div>
        <div className="text-xs ml-0.5" style={{color: 'var(--text3)'}}>Visão geral de compliance trabalhista</div>
      </div>
      
      <div className="ml-auto flex items-center gap-3">
        <div className="text-xs font-mono px-3 py-1.5 rounded-md border" style={{background: 'var(--surface)', color: 'var(--text2)', borderColor: 'var(--border2)'}}>
          {today}
        </div>
        
        <button
          onClick={onUpload}
          className="flex items-center gap-2 px-4 py-1.5 rounded-lg text-[13px] font-medium text-white transition hover:brightness-110"
          style={{background: 'var(--accent)'}}
        >
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="16 16 12 12 8 16"/>
            <line x1="12" y1="12" x2="12" y2="21"/>
            <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/>
          </svg>
          Importar CSV
        </button>
      </div>
    </header>
  );
}
