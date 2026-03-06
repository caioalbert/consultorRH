# Sistema de BI para Controle de Inventário de Aplicações

Sistema completo de Business Intelligence desenvolvido em Python para análise e monitoramento do inventário de aplicações corporativas.

## 📋 Visão Geral

Este sistema oferece dashboards interativos com visualizações detalhadas sobre:

- **Painel Geral**: Métricas gerais de aplicações, distribuição por produto, ambiente, tipo e framework
- **CI/CD**: Análise de ferramentas de versionamento, tipos de pipeline, versões e hospedagem
- **SecOps**: Score de segurança, práticas de SBOM, scan de imagens, secret manager e SAST
- **Governança**: Controle de revisões, aplicações desatualizadas e conformidade

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit**: Framework para criação de dashboards web interativos
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Visualizações interativas e gráficos avançados
- **OpenPyXL**: Leitura de arquivos Excel

## 📦 Instalação

### 1. Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalação das Dependências

```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

### 1. Preparar os Dados

O sistema aceita arquivos CSV ou Excel com a seguinte estrutura de colunas:

- `Nome_Aplicacao`: Nome da aplicação
- `Produto`: Produto ao qual a aplicação pertence
- `Ambiente`: Ambiente (Produção, Homologação, Desenvolvimento)
- `Tipo_Aplicacao`: Tipo (Web Application, API Rest, Microservice, Mobile App, etc.)
- `Framework`: Framework utilizado (.NET Core, Spring Boot, React, etc.)
- `Ferramenta_Versionamento`: Git provider (Azure DevOps, GitHub, GitLab, etc.)
- `Tipo_Pipeline`: Classic ou YAML
- `Versao`: Versão da aplicação
- `Hospedagem`: Plataforma de hospedagem (Kubernetes, Azure App Service, AWS, etc.)
- `SBOM`: Sim/Não - Se possui Software Bill of Materials
- `Scan_Imagens`: Sim/Não - Se realiza scan de segurança em imagens
- `Secret_Manager`: Sim/Não - Se utiliza gerenciador de secrets
- `SAST_SonarCube`: Sim/Não - Se utiliza análise SAST com SonarCube
- `Data_Ultima_Revisao`: Data da última revisão (formato: YYYY-MM-DD)
- `Data_Criacao`: Data de criação da aplicação (formato: YYYY-MM-DD)

**Arquivo de exemplo:** `inventario_aplicacoes.csv` (incluído no projeto)

### 2. Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador padrão em `http://localhost:8501`

### 3. Navegação

1. **Carregar Dados**: Use a barra lateral para fazer upload ou selecionar um arquivo local
2. **Selecionar Dashboard**: Escolha entre os 4 dashboards disponíveis
3. **Aplicar Filtros**: Filtre por produto e ambiente conforme necessário
4. **Explorar Visualizações**: Interaja com os gráficos para obter insights detalhados

## 📊 Estrutura dos Dashboards

### 🏠 Painel Geral

- Total de aplicações e métricas gerais
- Distribuição por produto (gráfico de barras)
- Distribuição por ambiente (gráfico de pizza)
- Distribuição por tipo de aplicação
- Top frameworks utilizados
- Mapa de calor: ambiente x tipo de aplicação
- Tabela resumo por produto

### 🔄 CI/CD

- Métricas de versionamento e pipeline
- Distribuição de ferramentas de versionamento
- Comparação: Pipeline YAML vs Classic
- Análise de versões por aplicação
- Distribuição por hospedagem
- Gauge de adoção de práticas modernas (% YAML)
- Análise hierárquica de versionamento e pipeline

### 🔒 SecOps

- Métricas de segurança por prática
- Score de segurança geral (0-100)
- Distribuição de scores por faixa
- Adoção de práticas de segurança (barras empilhadas)
- Gráfico radar comparativo
- Análise de segurança por produto
- Top 20 aplicações com maior risco

### ⚖️ Governança

- Aplicações sem data de revisão
- Aplicações com revisão > 3, 6 e 12 meses
- Distribuição por período sem revisão
- Status de conformidade (gráfico de pizza)
- Análise de governança por produto
- Top 20 aplicações com revisão mais antiga
- Timeline visual das aplicações desatualizadas
- Indicadores de criticidade e recomendações

## 📁 Estrutura do Projeto

```
Inventory - DevOps/
│
├── app.py                          # Aplicação principal
├── data_loader.py                  # Módulo de carregamento de dados
├── dashboard_painel_geral.py       # Dashboard Painel Geral
├── dashboard_cicd.py               # Dashboard CI/CD
├── dashboard_secops.py             # Dashboard SecOps
├── dashboard_governanca.py         # Dashboard Governança
├── requirements.txt                # Dependências Python
├── inventario_aplicacoes.csv       # Dados de exemplo
└── README.md                       # Este arquivo
```

## 🔧 Personalização

### Adicionar Novos Gráficos

Edite os arquivos `dashboard_*.py` correspondentes e adicione novos gráficos usando Plotly:

```python
import plotly.express as px

fig = px.bar(data, x='coluna_x', y='coluna_y')
st.plotly_chart(fig, use_container_width=True)
```

### Modificar Filtros

Edite o arquivo `app.py` na seção de filtros da sidebar:

```python
# Adicionar novo filtro
selected_framework = st.selectbox("Framework:", frameworks)
```

### Customizar Estilos

Modifique o CSS customizado no arquivo `app.py`:

```python
st.markdown("""
<style>
    /* Seu CSS aqui */
</style>
""", unsafe_allow_html=True)
```

## 📈 Exemplos de Insights

O sistema permite identificar:

- ✅ Produtos com maior número de aplicações
- ✅ Nível de adoção de pipelines YAML vs Classic
- ✅ Score de segurança por produto
- ✅ Aplicações críticas que precisam de revisão urgente
- ✅ Gaps de segurança (SBOM, Scan, SAST)
- ✅ Distribuição de aplicações por tecnologia
- ✅ Conformidade com políticas de governança

## 🐛 Troubleshooting

### Erro ao carregar dados

- Verifique se o arquivo está no formato correto (CSV ou Excel)
- Confirme se todas as colunas obrigatórias estão presentes
- Verifique o encoding do CSV (UTF-8)

### Gráficos não aparecem

- Confirme que as dependências foram instaladas corretamente
- Verifique se há dados suficientes para gerar os gráficos

### Aplicação não inicia

```bash
# Reinstale as dependências
pip install --upgrade -r requirements.txt

# Execute novamente
streamlit run app.py
```

## 📝 Licença

Este projeto é de uso interno para fins de análise e gestão de inventário de aplicações.

## 👥 Contribuição

Para adicionar novos recursos ou reportar bugs, entre em contato com a equipe de DevOps.

## 📞 Suporte

Para dúvidas ou suporte, entre em contato com o time de desenvolvimento.

---

**Desenvolvido com ❤️ usando Python e Streamlit**
