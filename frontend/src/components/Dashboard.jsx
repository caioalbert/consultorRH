export default function Dashboard({ data }) {
  const { colaboradores, ferias, exames, esocial } = data;

  const feriasVencidas = ferias.filter(f => f.status === 'Vencida' || f.status === 'Em Dobro').length;
  const examesAtrasados = exames.filter(e => e.status === 'Atrasado' || e.status === 'Crítico').length;
  const criticos = colaboradores.filter(c => c.risco === 'Crítico').length;

  const calcPassivo = () => {
    let total = 0;
    [...ferias, ...exames, ...esocial].forEach(item => {
      const val = (item.passivo || '').replace(/[^0-9,]/g, '').replace(',', '.');
      total += parseFloat(val) || 0;
    });
    return total;
  };

  const passivo = calcPassivo();
  const score = colaboradores.length ? Math.max(0, 100 - Math.round((criticos / Math.max(colaboradores.length,1)) * 50)) : 0;

  return (
    <div className="p-7 space-y-6">
      {/* KPIs */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
        <KPI label="Total de Colaboradores" value={colaboradores.length || '—'} color="blue" icon="👥" />
        <KPI label="Passivo Trabalhista" value={passivo ? `R$ ${passivo.toLocaleString('pt-BR', {maximumFractionDigits:0})}` : '—'} color="red" icon="💰" />
        <KPI label="Férias Vencidas" value={feriasVencidas || (ferias.length ? '0' : '—')} color="orange" icon="🏖️" />
        <KPI label="Exames Atrasados" value={examesAtrasados || (exames.length ? '0' : '—')} color="red" icon="🩺" />
        <KPI label="Alertas Críticos" value={criticos || (colaboradores.length ? '0' : '—')} color="yellow" icon="⚠️" />
        <KPI label="Compliance Score" value={colaboradores.length ? `${score}%` : '—'} color="green" icon="✅" />
      </div>

      {/* Main Grid */}
      <div className="grid lg:grid-cols-[1fr_380px] gap-5">
        <Card title="Passivo por Evento eSocial" subtitle="Multas estimadas por tipo de evento em atraso">
          {esocial.length ? (
            <div className="space-y-2.5">
              {esocial.map((s, i) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-lg" style={{background: 'var(--bg3)'}}>
                  <div>
                    <div className="text-sm font-medium font-mono" style={{color: '#93c5fd'}}>{s.evento}</div>
                    <div className="text-xs" style={{color: 'var(--text3)'}}>{s.descricao}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-semibold font-mono">{s.passivo}</div>
                    <div className="text-xs" style={{color: 'var(--text3)'}}>{s.pendencias} pendências</div>
                  </div>
                </div>
              ))}
            </div>
          ) : <EmptyState icon="📊" text="Importe dados eSocial" />}
        </Card>

        <Card title="Alertas Prioritários" subtitle="Pendências que exigem ação imediata" badge={feriasVencidas + examesAtrasados}>
          <div className="space-y-2.5">
            {feriasVencidas > 0 && (
              <Alert type="critical" icon="📅" title={`${feriasVencidas} Férias Vencidas`} desc="Férias vencidas aguardando programação" />
            )}
            {examesAtrasados > 0 && (
              <Alert type="critical" icon="🩺" title={`${examesAtrasados} Exames Atrasados`} desc="ASO periódicos fora do prazo" />
            )}
            {feriasVencidas === 0 && examesAtrasados === 0 && (
              <EmptyState icon="✅" text="Sem alertas críticos" />
            )}
          </div>
        </Card>
      </div>

      {/* Bottom Grid */}
      <div className="grid lg:grid-cols-3 gap-5">
        <Card title="Colaboradores" subtitle={`${colaboradores.length} registros`}>
          <Table
            headers={['Nome', 'Cargo', 'Status']}
            rows={colaboradores.slice(0, 5).map(c => [c.nome, c.cargo, <StatusPill key={c.id} status={c.status} />])}
            empty="Importe colaboradores"
          />
        </Card>

        <Card title="Férias" subtitle={`${ferias.length} registros`}>
          <Table
            headers={['Nome', 'Vencimento', 'Status']}
            rows={ferias.slice(0, 5).map(f => [f.nome, f.vencimento, <StatusPill key={f.id} status={f.status} />])}
            empty="Importe férias"
          />
        </Card>

        <Card title="Exames ASO" subtitle={`${exames.length} registros`}>
          <Table
            headers={['Nome', 'Tipo', 'Status']}
            rows={exames.slice(0, 5).map(e => [e.nome, e.tipoExame, <StatusPill key={e.id} status={e.status} />])}
            empty="Importe exames"
          />
        </Card>
      </div>
    </div>
  );
}

function KPI({ label, value, color, icon }) {
  const colors = {
    blue: { border: 'rgba(59,130,246,0.2)', bg: 'rgba(59,130,246,0.12)', text: '#93c5fd', iconBg: 'rgba(59,130,246,0.12)' },
    red: { border: 'rgba(239,68,68,0.2)', bg: 'rgba(239,68,68,0.12)', text: '#fca5a5', iconBg: 'rgba(239,68,68,0.12)' },
    orange: { border: 'rgba(249,115,22,0.2)', bg: 'rgba(249,115,22,0.12)', text: '#fdba74', iconBg: 'rgba(249,115,22,0.12)' },
    yellow: { border: 'rgba(234,179,8,0.2)', bg: 'rgba(234,179,8,0.10)', text: '#fde047', iconBg: 'rgba(234,179,8,0.10)' },
    green: { border: 'rgba(34,197,94,0.2)', bg: 'rgba(34,197,94,0.10)', text: '#86efac', iconBg: 'rgba(34,197,94,0.10)' }
  };

  const c = colors[color];

  return (
    <div className="rounded-xl p-4 border relative overflow-hidden transition hover:-translate-y-0.5" style={{background: 'var(--surface)', borderColor: 'var(--border)'}}>
      <div className="absolute top-0 left-0 right-0 h-0.5" style={{background: `linear-gradient(90deg, ${c.text}, transparent)`}} />
      <div className="flex items-center justify-between mb-3">
        <div className="text-[11.5px] font-medium leading-tight" style={{color: 'var(--text2)'}}>{label}</div>
        <div className="w-8 h-8 rounded-lg flex items-center justify-center text-sm" style={{background: c.iconBg}}>
          {icon}
        </div>
      </div>
      <div className="text-[26px] font-bold leading-none mb-1.5 font-mono" style={{color: c.text}}>{value}</div>
    </div>
  );
}

function Card({ title, subtitle, badge, children }) {
  return (
    <div className="rounded-xl border overflow-hidden" style={{background: 'var(--surface)', borderColor: 'var(--border)'}}>
      <div className="px-5 py-4 border-b flex items-start justify-between" style={{borderColor: 'var(--border)'}}>
        <div>
          <div className="text-sm font-semibold tracking-tight">{title}</div>
          {subtitle && <div className="text-[11.5px] mt-0.5" style={{color: 'var(--text3)'}}>{subtitle}</div>}
        </div>
        {badge > 0 && (
          <div className="w-5 h-5 rounded-full flex items-center justify-center text-[11px] font-bold font-mono text-white" style={{background: 'var(--red)'}}>
            {badge}
          </div>
        )}
      </div>
      <div className="p-5">{children}</div>
    </div>
  );
}

function Table({ headers, rows, empty }) {
  if (!rows.length) {
    return <EmptyState icon="📋" text={empty} />;
  }

  return (
    <div className="overflow-x-auto -mx-1">
      <table className="w-full text-[13px]">
        <thead>
          <tr className="border-b" style={{borderColor: 'var(--border)'}}>
            {headers.map((h, i) => (
              <th key={i} className="text-left py-2.5 px-3.5 text-[11px] font-semibold tracking-wide uppercase" style={{color: 'var(--text3)'}}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} className="border-b hover:bg-white/[0.02] transition" style={{borderColor: 'var(--border)'}}>
              {row.map((cell, j) => (
                <td key={j} className="py-2.5 px-3.5" style={{color: j === 0 ? 'var(--text)' : 'var(--text2)'}}>{cell || '—'}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Alert({ type, icon, title, desc }) {
  const colors = {
    critical: { bg: 'rgba(239,68,68,0.12)', border: 'rgba(239,68,68,0.15)', iconBg: 'rgba(239,68,68,0.2)' }
  };
  const c = colors[type];

  return (
    <div className="flex items-start gap-3 p-3 rounded-lg border cursor-pointer hover:brightness-110 transition" style={{background: c.bg, borderColor: c.border}}>
      <div className="w-7 h-7 rounded-md flex items-center justify-center text-[13px] flex-shrink-0" style={{background: c.iconBg}}>
        {icon}
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-[12.5px] font-medium truncate">{title}</div>
        <div className="text-[11px] leading-snug" style={{color: 'var(--text3)'}}>{desc}</div>
      </div>
    </div>
  );
}

function StatusPill({ status }) {
  const colors = {
    'Ativo': 'green',
    'Vencida': 'red',
    'Em Dobro': 'red',
    'Atrasado': 'orange',
    'Crítico': 'red',
    'Normal': 'green'
  };
  const color = colors[status] || 'gray';
  const styles = {
    green: { bg: 'rgba(34,197,94,0.10)', text: '#86efac', dot: '#22c55e' },
    red: { bg: 'rgba(239,68,68,0.12)', text: '#fca5a5', dot: '#ef4444' },
    orange: { bg: 'rgba(249,115,22,0.12)', text: '#fdba74', dot: '#f97316' }
  };
  const s = styles[color];

  return (
    <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] font-medium whitespace-nowrap" style={{background: s.bg, color: s.text}}>
      <span className="w-1 h-1 rounded-full" style={{background: s.dot}} />
      {status}
    </span>
  );
}

function EmptyState({ icon, text }) {
  return (
    <div className="text-center py-8">
      <div className="text-3xl mb-2 opacity-50">{icon}</div>
      <div className="text-sm" style={{color: 'var(--text3)'}}>{text}</div>
    </div>
  );
}
