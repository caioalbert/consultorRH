# Plano de Integração Azure DevOps - Multi-Tenant

## Objetivo
Transformar o DevOps Hub em uma plataforma multi-tenant que coleta dados automaticamente do Azure DevOps de cada cliente.

## Arquitetura

### 1. Modelo de Dados

```
clientes (tenants)
├── id
├── nome
├── slug (identificador único)
├── azure_devops_org
├── azure_devops_pat (encrypted)
├── ativo
└── configuracoes (JSON)

projetos
├── id
├── cliente_id (FK)
├── azure_project_id
├── nome
├── descricao
└── url

repositorios
├── id
├── projeto_id (FK)
├── azure_repo_id
├── nome
├── url
├── linguagem_principal
└── tamanho

pipelines
├── id
├── projeto_id (FK)
├── azure_pipeline_id
├── nome
├── tipo (build/release)
├── path
└── configuracao (YAML/Classic)

pipeline_execucoes
├── id
├── pipeline_id (FK)
├── run_id
├── status (succeeded/failed/canceled)
├── data_inicio
├── data_fim
├── duracao_segundos
├── triggered_by
└── branch

deployments
├── id
├── pipeline_id (FK)
├── ambiente (dev/staging/prod)
├── versao
├── status
├── data_deploy
└── deployed_by

work_items
├── id
├── projeto_id (FK)
├── azure_work_item_id
├── tipo (User Story/Bug/Task)
├── titulo
├── estado
├── prioridade
├── assignado_para
├── data_criacao
└── data_conclusao
```

### 2. Azure DevOps API

**Endpoints principais:**

```python
# Organizações e Projetos
GET https://dev.azure.com/{organization}/_apis/projects

# Repositórios
GET https://dev.azure.com/{organization}/{project}/_apis/git/repositories

# Pipelines
GET https://dev.azure.com/{organization}/{project}/_apis/pipelines

# Pipeline Runs
GET https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipelineId}/runs

# Work Items
GET https://dev.azure.com/{organization}/{project}/_apis/wit/workitems

# Releases
GET https://vsrm.dev.azure.com/{organization}/{project}/_apis/release/releases
```

### 3. Autenticação

- **Personal Access Token (PAT)** do Azure DevOps
- Armazenar criptografado no banco
- Permissões necessárias:
  - Code (Read)
  - Build (Read)
  - Release (Read)
  - Work Items (Read)

### 4. Sincronização de Dados

**Estratégias:**

1. **Sincronização Inicial** (Full Sync)
   - Importar todos os dados históricos
   - Executar ao adicionar novo cliente

2. **Sincronização Incremental** (Delta Sync)
   - Atualizar apenas dados novos/modificados
   - Executar periodicamente (ex: a cada hora)

3. **Webhook (Real-time)**
   - Azure DevOps envia eventos
   - Atualização em tempo real

### 5. Dashboards

**Painel por Cliente:**
- Visão geral de todos os projetos
- Métricas agregadas de CI/CD
- Status de deployments
- Work items em andamento

**Painel Consolidado (Consultoria):**
- Visão de todos os clientes
- Comparação de métricas
- Alertas e problemas
- Relatórios executivos

## Métricas e KPIs

### CI/CD
- Taxa de sucesso de builds
- Tempo médio de build
- Frequência de deploys
- Lead time (commit → produção)
- MTTR (Mean Time To Recovery)
- Change Failure Rate

### Desenvolvimento
- Commits por dia/semana
- Pull Requests abertos/fechados
- Tempo médio de review
- Code coverage
- Vulnerabilidades encontradas

### Gestão
- Work items por estado
- Velocity (story points)
- Burndown
- Cycle time

## Fases de Implementação

### Fase 1: Estrutura Base (1-2 semanas)
- [ ] Criar modelo multi-tenant no banco
- [ ] Sistema de autenticação por cliente
- [ ] Interface para cadastro de clientes
- [ ] Armazenamento seguro de PAT

### Fase 2: Integração Azure DevOps (2-3 semanas)
- [ ] Cliente HTTP para Azure DevOps API
- [ ] Coletar projetos e repositórios
- [ ] Coletar pipelines e execuções
- [ ] Coletar work items
- [ ] Sistema de sincronização

### Fase 3: Dashboards (2 semanas)
- [ ] Dashboard por cliente
- [ ] Dashboard consolidado
- [ ] Filtros e drill-down
- [ ] Exportação de relatórios

### Fase 4: Automação (1-2 semanas)
- [ ] Sincronização agendada (cron/celery)
- [ ] Webhooks Azure DevOps
- [ ] Notificações e alertas
- [ ] Cache de dados

### Fase 5: Melhorias (contínuo)
- [ ] Integração com outras ferramentas (GitHub, GitLab)
- [ ] Machine Learning para previsões
- [ ] Recomendações automáticas
- [ ] API REST para integrações

## Stack Tecnológica

### Backend
- **Python 3.10+**
- **FastAPI** (API REST)
- **SQLAlchemy** (ORM)
- **Alembic** (Migrations)
- **Celery** (Tasks assíncronas)
- **Redis** (Cache + Queue)

### Frontend
- **Streamlit** (Dashboards)
- Ou migrar para **React/Next.js** (mais flexível)

### Banco de Dados
- **PostgreSQL** (dados principais)
- **Redis** (cache)

### Infraestrutura
- **Docker** (containerização)
- **Docker Compose** (desenvolvimento)
- **AWS/Azure** (produção)

## Segurança

- Criptografia de PATs (Fernet/AES)
- HTTPS obrigatório
- Rate limiting
- Logs de auditoria
- Backup automático
- Isolamento de dados por tenant

## Próximos Passos

1. Validar arquitetura com você
2. Criar migrations para novo modelo
3. Implementar cliente Azure DevOps
4. Desenvolver sincronização inicial
5. Adaptar dashboards existentes
