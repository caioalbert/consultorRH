export default function Sidebar({ currentPage, onNavigate, onUpload }) {
  const NavItem = ({ icon, label, page, badge }) => (
    <div
      onClick={() => onNavigate(page)}
      className={`flex items-center gap-2.5 px-2.5 py-2 rounded-lg cursor-pointer transition-all mb-0.5 ${
        currentPage === page
          ? 'bg-[rgba(59,130,246,0.15)] text-[#60a5fa] font-medium'
          : 'text-[#8b95a8] hover:bg-[var(--surface)] hover:text-[var(--text)]'
      }`}
      style={{fontSize: '13.5px'}}
    >
      <span className="opacity-70">{icon}</span>
      <span>{label}</span>
      {badge > 0 && (
        <span className="ml-auto bg-[var(--red)] text-white text-[10px] font-semibold px-1.5 rounded-full font-mono">
          {badge}
        </span>
      )}
    </div>
  );

  return (
    <aside className="fixed left-0 top-0 bottom-0 w-[230px] flex flex-col z-50" style={{background: 'var(--bg2)', borderRight: '1px solid var(--border)'}}>
      <div className="px-5 py-6 border-b" style={{borderColor: 'var(--border)'}}>
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg flex items-center justify-center text-[15px]" style={{background: 'linear-gradient(135deg, var(--accent), #8b5cf6)'}}>
            ⚖️
          </div>
          <div className="text-[15px] font-semibold tracking-tight">
            Compliance<span style={{color: 'var(--accent2)'}}>HR</span>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-3 overflow-y-auto">
        <div className="mb-6">
          <div className="text-[10px] font-semibold tracking-wider uppercase px-2 mb-1.5" style={{color: 'var(--text3)'}}>
            Visão Geral
          </div>
          <NavItem icon="📊" label="Dashboard" page="dashboard" />
          <NavItem icon="📄" label="eSocial" page="esocial" badge={0} />
        </div>

        <div className="mb-6">
          <div className="text-[10px] font-semibold tracking-wider uppercase px-2 mb-1.5" style={{color: 'var(--text3)'}}>
            Colaboradores
          </div>
          <NavItem icon="👥" label="Colaboradores" page="employees" />
          <NavItem icon="📅" label="Férias" page="ferias" badge={0} />
          <NavItem icon="🩺" label="Exames ASO" page="exames" badge={0} />
        </div>

        <div>
          <div className="text-[10px] font-semibold tracking-wider uppercase px-2 mb-1.5" style={{color: 'var(--text3)'}}>
            Importação
          </div>
          <NavItem icon="📂" label="Importar CSV" page="upload" />
          <NavItem icon="🕐" label="Histórico" page="historico" />
        </div>
      </nav>

      <div className="p-3 border-t" style={{borderColor: 'var(--border)'}}>
        <div className="flex items-center gap-2.5 px-2.5 py-2 rounded-lg cursor-pointer hover:bg-[var(--surface)] transition">
          <div className="w-[30px] h-[30px] rounded-full flex items-center justify-center text-xs font-semibold" style={{background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)'}}>
            RH
          </div>
          <div className="overflow-hidden">
            <div className="text-[12.5px] font-medium truncate">Admin RH</div>
            <div className="text-[11px]" style={{color: 'var(--text3)'}}>Gestão Trabalhista</div>
          </div>
        </div>
      </div>
    </aside>
  );
}
