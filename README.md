# ComplianceHR - Sistema de Gestão Trabalhista

Sistema completo de compliance trabalhista com interface dark moderna e **banco de dados SQLite**.

## 🚀 Instalação e Execução

```bash
cd ~/projetos/ConsultorRH_v2

# Popular banco de dados (primeira vez)
python3 populate_db.py

# Iniciar aplicação
streamlit run app.py --server.port 8502
```

## 💾 Banco de Dados

- **SQLite** local em `data/consultorrh.db`
- Tabelas: `colaboradores`, `ferias`, `exames`, `esocial`
- Dados persistentes entre sessões
- Import via CSV pela interface

## 📊 Funcionalidades

- ✅ Dashboard com KPIs e gráficos
- ✅ Gestão de Colaboradores
- ✅ Controle de Férias
- ✅ Monitoramento de Exames ASO
- ✅ Eventos eSocial
- ✅ Upload de CSV (popula banco)
- ✅ Tema dark moderno
- ✅ Banco de dados SQLite

## 📁 Estrutura de Dados

### Colaboradores
```csv
nome,cpf,cargo,filial,setor,data_admissao,status,risco
Ana Lima,123.456.789-00,Analista RH,São Paulo,RH,2020-03-15,Ativo,Normal
```

### Férias
```csv
nome,filial,periodo_aquisitivo,dias_devidos,vencimento,em_dobro,passivo,status
Ana Lima,São Paulo,2022/2023,30,2023-11-01,Não,R$ 5000,Vencida
```

### Exames ASO
```csv
nome,filial,tipo_exame,ultimo_exame,vencimento,dias_atraso,passivo,status
Ana Lima,São Paulo,Periódico,2022-01-10,2023-01-10,320,R$ 500,Atrasado
```

### eSocial
```csv
evento,descricao,pendencias,passivo,criticidade
S-1200,Remuneração do Trabalhador,87,R$ 157719,Crítico
```

## 🎨 Design

Interface baseada no protótipo `dashboard_compliance_rh.html` com:
- Tema dark (#0b0f1a)
- Fonte DM Sans
- Sidebar com navegação
- KPIs destacados
- Tabelas responsivas

## 📂 Arquivos CSV de Exemplo

Use o arquivo `exemplo_colaboradores.csv` para testar a importação.

## 🔧 Tecnologias

- Python 3.10+
- Streamlit
- Pandas
- CSV para armazenamento
