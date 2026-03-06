"""
Sistema de Compliance Trabalhista - ConsultorRH
Aplicação principal usando Streamlit
"""
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from database import init_db, load_from_db, save_to_db

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa banco de dados
try:
    init_db()
except Exception as e:
    st.error(f"Erro ao conectar ao banco: {e}")
    st.info("Configure as variáveis de ambiente no arquivo .env")

# Configuração da página
st.set_page_config(
    page_title="ComplianceHR",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="auto"
)

# CSS customizado - Tema Dark do protótipo
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@300;400;500&display=swap');
    
    * { font-family: 'DM Sans', sans-serif; }
    
    .main, .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0b0f1a !important;
        color: #e8edf5 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #111622 !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    
    .main-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #60a5fa;
        margin-bottom: 1rem;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #93c5fd;
        font-family: 'DM Mono', monospace;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 0.75rem;
        color: #8b95a8;
        text-transform: uppercase;
        font-weight: 600;
    }
    
    h1, h2, h3 { color: #e8edf5; font-weight: 700; }
    
    .stAlert, div[data-testid="stExpander"] {
        background-color: #1a2235 !important;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
    }
    
    /* Gráficos com fundo escuro */
    [data-testid="stVegaLiteChart"], [data-testid="stArrowVegaLiteChart"] {
        background-color: #1a2235 !important;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255,255,255,0.06);
    }
    
    /* Canvas dos gráficos */
    canvas {
        background-color: transparent !important;
    }
    
    /* Tabelas */
    .dataframe {
        background-color: #1a2235 !important;
        color: #e8edf5 !important;
    }
    
    thead tr th {
        background-color: #1f2940 !important;
        color: #8b95a8 !important;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    tbody tr {
        background-color: #1a2235 !important;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    
    tbody tr:hover { background-color: rgba(255,255,255,0.02) !important; }
    tbody td { color: #8b95a8 !important; }
    
    /* Inputs */
    .stSelectbox > div > div, .stTextInput > div > div > input, .stFileUploader > div {
        background-color: #1a2235 !important;
        color: #e8edf5 !important;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 8px;
    }
    
    /* Botões */
    .stButton > button {
        background-color: #3b82f6 !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #2563eb !important;
        transform: translateY(-1px);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #111622; }
    ::-webkit-scrollbar-thumb { background: #1f2940; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# Diretório de dados
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(tipo):
    """Carrega dados do banco de dados"""
    try:
        return load_from_db(tipo)
    except:
        return pd.DataFrame()

def save_data(df, tipo):
    """Salva dados no banco de dados"""
    save_to_db(df, tipo)

def main():
    """Função principal"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0; border-bottom: 2px solid rgba(255,255,255,0.2); margin-bottom: 1rem;'>
            <h1 style='color: white; font-size: 1.3rem; margin: 0;'>⚖️ ComplianceHR</h1>
            <p style='color: rgba(255,255,255,0.8); font-size: 0.7rem; margin: 0.3rem 0 0 0;'>Gestão Trabalhista</p>
        </div>
        """, unsafe_allow_html=True)
        
        if 'page' not in st.session_state:
            st.session_state.page = 'dashboard'
        
        st.markdown("<h3 style='color: white; font-size: 0.9rem; margin-bottom: 1rem;'>Menu Principal</h3>", unsafe_allow_html=True)
        
        if st.button("Dashboard", use_container_width=True, type="primary" if st.session_state.page == 'dashboard' else "secondary"):
            st.session_state.page = 'dashboard'
            st.rerun()
        
        if st.button("Colaboradores", use_container_width=True, type="primary" if st.session_state.page == 'colaboradores' else "secondary"):
            st.session_state.page = 'colaboradores'
            st.rerun()
        
        if st.button("Férias", use_container_width=True, type="primary" if st.session_state.page == 'ferias' else "secondary"):
            st.session_state.page = 'ferias'
            st.rerun()
        
        if st.button("Exames ASO", use_container_width=True, type="primary" if st.session_state.page == 'exames' else "secondary"):
            st.session_state.page = 'exames'
            st.rerun()
        
        if st.button("eSocial", use_container_width=True, type="primary" if st.session_state.page == 'esocial' else "secondary"):
            st.session_state.page = 'esocial'
            st.rerun()
        
        if st.button("Importar CSV", use_container_width=True, type="primary" if st.session_state.page == 'upload' else "secondary"):
            st.session_state.page = 'upload'
            st.rerun()
        
        st.markdown("---")
        st.markdown("""
        <div style='color: rgba(255,255,255,0.6); font-size: 0.65rem; text-align: center;'>
            <p style='margin: 0.2rem 0;'>v1.0.0</p>
            <p style='margin: 0.2rem 0;'>© 2026</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Renderiza página
    if st.session_state.page == 'dashboard':
        render_dashboard()
    elif st.session_state.page == 'colaboradores':
        render_colaboradores()
    elif st.session_state.page == 'ferias':
        render_ferias()
    elif st.session_state.page == 'exames':
        render_exames()
    elif st.session_state.page == 'esocial':
        render_esocial()
    elif st.session_state.page == 'upload':
        render_upload()

def render_dashboard():
    """Dashboard principal"""
    st.markdown('<div class="main-header">Dashboard de Compliance</div>', unsafe_allow_html=True)
    
    # Carrega dados
    colaboradores = load_data('colaboradores')
    ferias = load_data('ferias')
    exames = load_data('exames')
    esocial = load_data('esocial')
    
    # KPIs
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Total Colaboradores", len(colaboradores))
    
    with col2:
        passivo = 0
        for df in [ferias, exames, esocial]:
            if 'passivo' in df.columns:
                passivo += df['passivo'].apply(lambda x: float(str(x).replace('R$', '').replace('.', '').replace(',', '.').strip()) if pd.notna(x) else 0).sum()
        st.metric("Passivo Trabalhista", f"R$ {passivo:,.0f}")
    
    with col3:
        feriasVenc = len(ferias[ferias['status'].isin(['Vencida', 'Em Dobro'])]) if 'status' in ferias.columns else 0
        st.metric("Férias Vencidas", feriasVenc)
    
    with col4:
        examesAtr = len(exames[exames['status'].isin(['Atrasado', 'Crítico'])]) if 'status' in exames.columns else 0
        st.metric("Exames Atrasados", examesAtr)
    
    with col5:
        criticos = len(colaboradores[colaboradores['risco'] == 'Crítico']) if 'risco' in colaboradores.columns else 0
        st.metric("Alertas Críticos", criticos)
    
    with col6:
        score = 100 - (criticos * 10) if len(colaboradores) > 0 else 0
        st.metric("Compliance Score", f"{max(0, score)}%")
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Passivo por Evento eSocial")
        if not esocial.empty and 'evento' in esocial.columns and 'passivo' in esocial.columns:
            chart_data = esocial.copy()
            chart_data['valor'] = chart_data['passivo'].apply(lambda x: float(str(x).replace('R$', '').replace('.', '').replace(',', '.').strip()) if pd.notna(x) else 0)
            st.bar_chart(chart_data.set_index('evento')['valor'])
        else:
            st.info("Importe dados eSocial")
    
    with col2:
        st.markdown("### Alertas Prioritários")
        if feriasVenc > 0 or examesAtr > 0:
            alert_data = pd.DataFrame({
                'Tipo': ['Férias Vencidas', 'Exames Atrasados'],
                'Quantidade': [feriasVenc, examesAtr]
            })
            st.bar_chart(alert_data.set_index('Tipo'))
        else:
            st.success("✅ Sem alertas críticos")
    
    st.markdown("---")
    
    # Gráficos adicionais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Colaboradores por Filial")
        if not colaboradores.empty and 'filial' in colaboradores.columns:
            filial_count = colaboradores['filial'].value_counts()
            st.bar_chart(filial_count)
        else:
            st.info("Importe colaboradores")
    
    with col2:
        st.markdown("### Distribuição de Riscos")
        if not colaboradores.empty and 'risco' in colaboradores.columns:
            risco_count = colaboradores['risco'].value_counts()
            st.bar_chart(risco_count)
        else:
            st.info("Importe colaboradores")
    
    with col3:
        st.markdown("### Status de Exames")
        if not exames.empty and 'status' in exames.columns:
            status_count = exames['status'].value_counts()
            st.bar_chart(status_count)
        else:
            st.info("Importe exames")
    
    st.markdown("---")
    
    # Tabelas resumidas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Últimos Colaboradores")
        if not colaboradores.empty:
            st.dataframe(colaboradores.head(5), use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum dado. Importe um CSV.")
    
    with col2:
        st.markdown("### Férias Vencidas")
        if not ferias.empty and 'status' in ferias.columns:
            feriasVencDf = ferias[ferias['status'].isin(['Vencida', 'Em Dobro'])]
            if not feriasVencDf.empty:
                st.dataframe(feriasVencDf.head(5), use_container_width=True, hide_index=True)
            else:
                st.success("✅ Nenhuma férias vencida")
        else:
            st.info("Nenhum dado. Importe um CSV.")

def render_colaboradores():
    """Página de colaboradores"""
    st.markdown('<div class="main-header">Colaboradores</div>', unsafe_allow_html=True)
    
    df = load_data('colaboradores')
    
    if not df.empty:
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", len(df))
        with col2:
            ativos = len(df[df['status'] == 'Ativo']) if 'status' in df.columns else 0
            st.metric("Ativos", ativos)
        with col3:
            criticos = len(df[df['risco'] == 'Crítico']) if 'risco' in df.columns else 0
            st.metric("Risco Crítico", criticos)
        with col4:
            filiais = df['filial'].nunique() if 'filial' in df.columns else 0
            st.metric("Filiais", filiais)
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Por Filial")
            if 'filial' in df.columns:
                st.bar_chart(df['filial'].value_counts())
        
        with col2:
            st.markdown("### Por Risco")
            if 'risco' in df.columns:
                st.bar_chart(df['risco'].value_counts())
        
        st.markdown("---")
        
        # Tabela
        st.dataframe(df, use_container_width=True, hide_index=True, height=400)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "colaboradores.csv", "text/csv")
    else:
        st.info("Nenhum dado. Importe um CSV na página 'Importar CSV'.")

def render_ferias():
    """Página de férias"""
    st.markdown('<div class="main-header">Controle de Férias</div>', unsafe_allow_html=True)
    
    df = load_data('ferias')
    
    if not df.empty:
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", len(df))
        with col2:
            vencidas = len(df[df['status'] == 'Vencida']) if 'status' in df.columns else 0
            st.metric("Vencidas", vencidas)
        with col3:
            dobro = len(df[df['em_dobro'] == 'Sim']) if 'em_dobro' in df.columns else 0
            st.metric("Em Dobro", dobro)
        with col4:
            if 'passivo' in df.columns:
                total_passivo = df['passivo'].apply(lambda x: float(str(x).replace('R$', '').replace('.', '').replace(',', '.').strip()) if pd.notna(x) else 0).sum()
                st.metric("Passivo Total", f"R$ {total_passivo:,.0f}")
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Por Status")
            if 'status' in df.columns:
                st.bar_chart(df['status'].value_counts())
        
        with col2:
            st.markdown("### Por Filial")
            if 'filial' in df.columns:
                st.bar_chart(df['filial'].value_counts())
        
        st.markdown("---")
        
        # Tabela
        st.dataframe(df, use_container_width=True, hide_index=True, height=400)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "ferias.csv", "text/csv")
    else:
        st.info("Nenhum dado. Importe um CSV na página 'Importar CSV'.")

def render_exames():
    """Página de exames"""
    st.markdown('<div class="main-header">Exames ASO</div>', unsafe_allow_html=True)
    
    df = load_data('exames')
    
    if not df.empty:
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total", len(df))
        with col2:
            atrasados = len(df[df['status'] == 'Atrasado']) if 'status' in df.columns else 0
            st.metric("Atrasados", atrasados)
        with col3:
            criticos = len(df[df['status'] == 'Crítico']) if 'status' in df.columns else 0
            st.metric("Críticos", criticos)
        with col4:
            if 'passivo' in df.columns:
                total_passivo = df['passivo'].apply(lambda x: float(str(x).replace('R$', '').replace('.', '').replace(',', '.').strip()) if pd.notna(x) else 0).sum()
                st.metric("Passivo Total", f"R$ {total_passivo:,.0f}")
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Por Status")
            if 'status' in df.columns:
                st.bar_chart(df['status'].value_counts())
        
        with col2:
            st.markdown("### Por Tipo de Exame")
            if 'tipo_exame' in df.columns:
                st.bar_chart(df['tipo_exame'].value_counts())
        
        st.markdown("---")
        
        # Tabela
        st.dataframe(df, use_container_width=True, hide_index=True, height=400)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "exames.csv", "text/csv")
    else:
        st.info("Nenhum dado. Importe um CSV na página 'Importar CSV'.")

def render_esocial():
    """Página de eSocial"""
    st.markdown('<div class="main-header">Eventos eSocial</div>', unsafe_allow_html=True)
    
    df = load_data('esocial')
    
    if not df.empty:
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Eventos", len(df))
        with col2:
            if 'pendencias' in df.columns:
                total_pend = df['pendencias'].sum()
                st.metric("Total Pendências", int(total_pend))
        with col3:
            criticos = len(df[df['criticidade'] == 'Crítico']) if 'criticidade' in df.columns else 0
            st.metric("Eventos Críticos", criticos)
        with col4:
            if 'passivo' in df.columns:
                total_passivo = df['passivo'].apply(lambda x: float(str(x).replace('R$', '').replace('.', '').replace(',', '.').strip()) if pd.notna(x) else 0).sum()
                st.metric("Passivo Total", f"R$ {total_passivo:,.0f}")
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Passivo por Evento")
            if 'evento' in df.columns and 'passivo' in df.columns:
                chart_data = df.copy()
                chart_data['valor'] = chart_data['passivo'].apply(lambda x: float(str(x).replace('R$', '').replace('.', '').replace(',', '.').strip()) if pd.notna(x) else 0)
                st.bar_chart(chart_data.set_index('evento')['valor'])
        
        with col2:
            st.markdown("### Por Criticidade")
            if 'criticidade' in df.columns:
                st.bar_chart(df['criticidade'].value_counts())
        
        st.markdown("---")
        
        # Tabela
        st.dataframe(df, use_container_width=True, hide_index=True, height=400)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "esocial.csv", "text/csv")
    else:
        st.info("Nenhum dado. Importe um CSV na página 'Importar CSV'.")

def render_upload():
    """Página de upload"""
    st.markdown('<div class="main-header">Importar CSV</div>', unsafe_allow_html=True)
    
    tipo = st.selectbox("Tipo de dados", ['colaboradores', 'ferias', 'exames', 'esocial'])
    
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✓ Arquivo carregado: {len(df)} registros")
            
            st.dataframe(df.head(10), use_container_width=True)
            
            if st.button("Confirmar Importação"):
                save_data(df, tipo)
                st.success(f"✓ {len(df)} registros importados com sucesso!")
                st.balloons()
        except Exception as e:
            st.error(f"Erro ao ler arquivo: {e}")
    
    st.markdown("---")
    st.markdown("### Formatos esperados")
    
    if tipo == 'colaboradores':
        st.code("nome,cpf,cargo,filial,setor,data_admissao,status,risco")
    elif tipo == 'ferias':
        st.code("nome,filial,periodo_aquisitivo,dias_devidos,vencimento,em_dobro,passivo,status")
    elif tipo == 'exames':
        st.code("nome,filial,tipo_exame,ultimo_exame,vencimento,dias_atraso,passivo,status")
    elif tipo == 'esocial':
        st.code("evento,descricao,pendencias,passivo,criticidade")

if __name__ == "__main__":
    main()
