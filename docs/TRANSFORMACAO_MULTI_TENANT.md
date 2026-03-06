# Transformação para Plataforma Multi-Tenant com Azure DevOps

## 📋 Resumo Executivo

Transformamos o DevOps Hub de um sistema single-tenant com dados estáticos (CSV/Excel) para uma **plataforma multi-tenant dinâmica** que se integra automaticamente com Azure DevOps de múltiplos clientes.

## 🎯 O Que Mudou

### Antes
- ❌ Dados estáticos (CSV/Excel)
- ❌ Single tenant (um único cliente)
- ❌ GMUD manual
- ❌ Atualização manual de dados

### Depois
- ✅ Dados dinâmicos via API Azure DevOps
- ✅ Multi-tenant (múltiplos clientes)
- ✅ Sincronização automática
- ✅ Dados em tempo real

## 🏗️ Arquivos Criados

### 1. Documentação
- `docs/PLANO_INTEGRACAO_AZURE_DEVOPS.md` - Plano completo de implementação

### 2. Integração
- `src/integrations/azure_devops_client.py` - Cliente para Azure DevOps API
  - Coleta projetos, repositórios, pipelines, work items
  - Métricas agregadas
  - Autenticação via PAT

### 3. Serviços
- `src/services/azure_devops_sync.py` - Serviço de sincronização
  - Sincronização full e incremental
  - Controle de execução
  - Tratamento de erros

### 4. Banco de Dados
- `migrations/005_multi_tenant_azure_devops.sql` - Nova estrutura
  - Tabela `clientes` (tenants)
  - Tabela `projetos` (Azure DevOps projects)
  - Tabela `repositorios` (Git repos)
  - Tabela `pipelines` (CI/CD)
  - Tabela `pipeline_execucoes` (histórico)
  - Tabela `deployments` (por ambiente)
  - Tabela `work_items` (User Stories, Bugs, Tasks)
  - Tabela `pull_requests`
  - Tabela `sincronizacoes` (controle)
  - Views para métricas agregadas

## 📊 Dados Coletados do Azure DevOps

### Por Cliente
1. **Projetos**
   - Nome, descrição, URL
   - Estado, visibilidade

2. **Repositórios**
   - Nome, linguagem principal
   - Tamanho, branch padrão
   - Estatísticas

3. **Pipelines CI/CD**
   - Build e Release pipelines
   - Configuração (YAML/Classic)
   - Histórico de execuções
   - Taxa de sucesso/falha
   - Tempo médio de execução

4. **Deployments**
   - Por ambiente (dev/staging/prod)
   - Status, versão
   - Frequência de deploy

5. **Work Items**
   - User Stories, Bugs, Tasks
   - Estado, prioridade
   - Assignee, story points
   - Métricas de velocity

6. **Pull Requests**
   - Status, branches
   - Tempo de review
   - Merge status

## 🚀 Como Usar

### 1. Aplicar Migration

```bash
cd migrations
python migrate.py
```

### 2. Cadastrar Cliente

```python
import psycopg2

conn = psycopg2.connect(...)
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO clientes (nome, slug, azure_devops_org, azure_devops_pat_encrypted, ativo)
    VALUES (%s, %s, %s, %s, TRUE)
""", ('Cliente XYZ', 'cliente-xyz', 'organizacao-azure', 'PAT_AQUI'))

conn.commit()
```

### 3. Sincronizar Dados

```python
from src.services.azure_devops_sync import sync_cliente

# Sincronizar cliente ID 1
sync_cliente(1)
```

### 4. Agendar Sincronização Automática

```python
# Usando Celery (recomendado)
from celery import Celery
from celery.schedules import crontab

app = Celery('devops_hub')

@app.task
def sync_all_clients():
    cursor.execute("SELECT id FROM clientes WHERE ativo = TRUE")
    for (cliente_id,) in cursor.fetchall():
        sync_cliente(cliente_id)

# Executar a cada hora
app.conf.beat_schedule = {
    'sync-every-hour': {
        'task': 'sync_all_clients',
        'schedule': crontab(minute=0),
    },
}
```

## 📈 Dashboards Sugeridos

### 1. Dashboard por Cliente
- Visão geral do cliente
- Projetos ativos
- Taxa de sucesso de pipelines
- Deployments recentes
- Work items em andamento
- Métricas DORA

### 2. Dashboard Consolidado (Consultoria)
- Comparação entre clientes
- Ranking de performance
- Alertas e problemas
- Tendências
- Relatórios executivos

### 3. Dashboard CI/CD
- Pipeline success rate
- Build duration trends
- Deployment frequency
- Lead time for changes
- Change failure rate
- MTTR (Mean Time To Recovery)

### 4. Dashboard de Desenvolvimento
- Commits por período
- Pull requests
- Code review time
- Velocity (story points)
- Burndown charts

## 🔐 Segurança

### Personal Access Token (PAT)
- Armazenar criptografado no banco
- Usar biblioteca `cryptography` (Fernet)
- Nunca expor em logs

```python
from cryptography.fernet import Fernet

# Gerar chave (fazer uma vez, guardar em .env)
key = Fernet.generate_key()

# Criptografar PAT
f = Fernet(key)
encrypted_pat = f.encrypt(pat.encode())

# Descriptografar quando necessário
decrypted_pat = f.decrypt(encrypted_pat).decode()
```

### Permissões Necessárias no PAT
- ✅ Code (Read)
- ✅ Build (Read)
- ✅ Release (Read)
- ✅ Work Items (Read)
- ✅ Project and Team (Read)

## 📦 Dependências Adicionais

Adicionar ao `requirements.txt`:

```
requests==2.31.0
cryptography==41.0.7
celery==5.3.4
redis==5.0.1
```

## 🎯 Próximos Passos

### Fase 1: Implementação Base (2 semanas)
1. ✅ Criar estrutura de banco (FEITO)
2. ✅ Cliente Azure DevOps API (FEITO)
3. ✅ Serviço de sincronização (FEITO)
4. ⏳ Interface para cadastro de clientes
5. ⏳ Criptografia de PATs
6. ⏳ Testes de integração

### Fase 2: Dashboards (2 semanas)
1. ⏳ Adaptar dashboards existentes
2. ⏳ Dashboard por cliente
3. ⏳ Dashboard consolidado
4. ⏳ Filtros e drill-down
5. ⏳ Exportação de relatórios

### Fase 3: Automação (1 semana)
1. ⏳ Celery + Redis
2. ⏳ Sincronização agendada
3. ⏳ Webhooks Azure DevOps
4. ⏳ Notificações

### Fase 4: Melhorias (contínuo)
1. ⏳ Cache inteligente
2. ⏳ Métricas DORA
3. ⏳ Alertas automáticos
4. ⏳ API REST
5. ⏳ Integração GitHub/GitLab

## 💡 Exemplo de Uso Completo

```python
# 1. Cadastrar cliente
from src.services.cliente_service import ClienteService

cliente = ClienteService.criar_cliente(
    nome="Acme Corp",
    slug="acme-corp",
    azure_org="acme-devops",
    azure_pat="seu-pat-aqui"
)

# 2. Sincronizar dados
from src.services.azure_devops_sync import AzureDevOpsSyncService

sync = AzureDevOpsSyncService(conn, cliente.id, "acme-devops", "pat")
stats = sync.sync_full()

print(f"Sincronizados: {stats}")

# 3. Consultar métricas
from src.services.metrics_service import MetricsService

metrics = MetricsService.get_client_metrics(cliente.id)
print(f"Taxa de sucesso: {metrics['pipeline_success_rate']}%")
print(f"Deploys/semana: {metrics['deploys_per_week']}")
```

## 🎨 Exemplo de Dashboard

```python
import streamlit as st
from src.services.metrics_service import MetricsService

st.title("DevOps Hub - Dashboard")

# Seletor de cliente
clientes = get_all_clients()
cliente_id = st.selectbox("Cliente", clientes)

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

metrics = MetricsService.get_client_metrics(cliente_id)

col1.metric("Projetos", metrics['total_projects'])
col2.metric("Pipelines", metrics['total_pipelines'])
col3.metric("Taxa Sucesso", f"{metrics['success_rate']:.1f}%")
col4.metric("Deploys/Semana", metrics['deploys_per_week'])

# Gráfico de tendência
st.line_chart(metrics['pipeline_trend'])

# Tabela de projetos
st.dataframe(metrics['projects_summary'])
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Consultar documentação em `docs/`
2. Verificar logs de sincronização
3. Testar conexão com Azure DevOps

---

**Status:** ✅ Estrutura base criada, pronta para implementação
**Próximo passo:** Aplicar migration e testar sincronização
