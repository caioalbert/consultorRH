-- Migration 005: Modelo Multi-Tenant com Azure DevOps
-- Remove tabela GMUD e adiciona estrutura para múltiplos clientes

-- ==================== CLIENTES (TENANTS) ====================

CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    azure_devops_org VARCHAR(255),
    azure_devops_pat_encrypted TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    configuracoes JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clientes_slug ON clientes(slug);
CREATE INDEX idx_clientes_ativo ON clientes(ativo);

-- ==================== PROJETOS ====================

CREATE TABLE IF NOT EXISTS projetos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    azure_project_id VARCHAR(255),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    url TEXT,
    visibilidade VARCHAR(50),
    estado VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cliente_id, azure_project_id)
);

CREATE INDEX idx_projetos_cliente ON projetos(cliente_id);
CREATE INDEX idx_projetos_azure_id ON projetos(azure_project_id);

-- ==================== REPOSITÓRIOS ====================

CREATE TABLE IF NOT EXISTS repositorios (
    id SERIAL PRIMARY KEY,
    projeto_id INTEGER NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
    azure_repo_id VARCHAR(255),
    nome VARCHAR(255) NOT NULL,
    url TEXT,
    linguagem_principal VARCHAR(100),
    tamanho_kb INTEGER,
    default_branch VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(projeto_id, azure_repo_id)
);

CREATE INDEX idx_repositorios_projeto ON repositorios(projeto_id);
CREATE INDEX idx_repositorios_linguagem ON repositorios(linguagem_principal);

-- ==================== PIPELINES ====================

CREATE TABLE IF NOT EXISTS pipelines (
    id SERIAL PRIMARY KEY,
    projeto_id INTEGER NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
    azure_pipeline_id INTEGER,
    nome VARCHAR(255) NOT NULL,
    tipo VARCHAR(50), -- build, release, yaml
    path VARCHAR(500),
    configuracao VARCHAR(50), -- YAML, Classic
    repositorio_id INTEGER REFERENCES repositorios(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(projeto_id, azure_pipeline_id)
);

CREATE INDEX idx_pipelines_projeto ON pipelines(projeto_id);
CREATE INDEX idx_pipelines_tipo ON pipelines(tipo);

-- ==================== EXECUÇÕES DE PIPELINE ====================

CREATE TABLE IF NOT EXISTS pipeline_execucoes (
    id SERIAL PRIMARY KEY,
    pipeline_id INTEGER NOT NULL REFERENCES pipelines(id) ON DELETE CASCADE,
    azure_run_id INTEGER,
    numero_execucao INTEGER,
    status VARCHAR(50), -- succeeded, failed, canceled, inProgress
    resultado VARCHAR(50), -- succeeded, failed, canceled
    data_inicio TIMESTAMP,
    data_fim TIMESTAMP,
    duracao_segundos INTEGER,
    triggered_by VARCHAR(255),
    branch VARCHAR(255),
    commit_id VARCHAR(255),
    motivo VARCHAR(100), -- manual, schedule, pullRequest, etc
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(pipeline_id, azure_run_id)
);

CREATE INDEX idx_pipeline_execucoes_pipeline ON pipeline_execucoes(pipeline_id);
CREATE INDEX idx_pipeline_execucoes_status ON pipeline_execucoes(status);
CREATE INDEX idx_pipeline_execucoes_data ON pipeline_execucoes(data_inicio DESC);

-- ==================== DEPLOYMENTS ====================

CREATE TABLE IF NOT EXISTS deployments (
    id SERIAL PRIMARY KEY,
    pipeline_id INTEGER NOT NULL REFERENCES pipelines(id) ON DELETE CASCADE,
    execucao_id INTEGER REFERENCES pipeline_execucoes(id),
    ambiente VARCHAR(100), -- dev, staging, production
    versao VARCHAR(100),
    status VARCHAR(50), -- succeeded, failed, inProgress
    data_deploy TIMESTAMP,
    deployed_by VARCHAR(255),
    duracao_segundos INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_deployments_pipeline ON deployments(pipeline_id);
CREATE INDEX idx_deployments_ambiente ON deployments(ambiente);
CREATE INDEX idx_deployments_data ON deployments(data_deploy DESC);

-- ==================== WORK ITEMS ====================

CREATE TABLE IF NOT EXISTS work_items (
    id SERIAL PRIMARY KEY,
    projeto_id INTEGER NOT NULL REFERENCES projetos(id) ON DELETE CASCADE,
    azure_work_item_id INTEGER,
    tipo VARCHAR(100), -- User Story, Bug, Task, Epic, Feature
    titulo TEXT NOT NULL,
    descricao TEXT,
    estado VARCHAR(100), -- New, Active, Resolved, Closed
    prioridade INTEGER,
    severidade VARCHAR(50),
    assignado_para VARCHAR(255),
    criado_por VARCHAR(255),
    area_path VARCHAR(500),
    iteration_path VARCHAR(500),
    story_points DECIMAL(10,2),
    data_criacao TIMESTAMP,
    data_modificacao TIMESTAMP,
    data_conclusao TIMESTAMP,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(projeto_id, azure_work_item_id)
);

CREATE INDEX idx_work_items_projeto ON work_items(projeto_id);
CREATE INDEX idx_work_items_tipo ON work_items(tipo);
CREATE INDEX idx_work_items_estado ON work_items(estado);
CREATE INDEX idx_work_items_assignado ON work_items(assignado_para);

-- ==================== PULL REQUESTS ====================

CREATE TABLE IF NOT EXISTS pull_requests (
    id SERIAL PRIMARY KEY,
    repositorio_id INTEGER NOT NULL REFERENCES repositorios(id) ON DELETE CASCADE,
    azure_pr_id INTEGER,
    titulo TEXT NOT NULL,
    descricao TEXT,
    status VARCHAR(50), -- active, completed, abandoned
    criado_por VARCHAR(255),
    source_branch VARCHAR(255),
    target_branch VARCHAR(255),
    data_criacao TIMESTAMP,
    data_fechamento TIMESTAMP,
    merge_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(repositorio_id, azure_pr_id)
);

CREATE INDEX idx_pull_requests_repositorio ON pull_requests(repositorio_id);
CREATE INDEX idx_pull_requests_status ON pull_requests(status);

-- ==================== SINCRONIZAÇÕES ====================

CREATE TABLE IF NOT EXISTS sincronizacoes (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    tipo VARCHAR(50), -- full, incremental
    status VARCHAR(50), -- running, completed, failed
    data_inicio TIMESTAMP,
    data_fim TIMESTAMP,
    duracao_segundos INTEGER,
    registros_processados INTEGER,
    erros TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sincronizacoes_cliente ON sincronizacoes(cliente_id);
CREATE INDEX idx_sincronizacoes_data ON sincronizacoes(data_inicio DESC);

-- ==================== ATUALIZAR TABELA APLICACOES ====================

-- Adicionar referência a cliente e projeto
ALTER TABLE aplicacoes ADD COLUMN IF NOT EXISTS cliente_id INTEGER REFERENCES clientes(id);
ALTER TABLE aplicacoes ADD COLUMN IF NOT EXISTS projeto_id INTEGER REFERENCES projetos(id);
ALTER TABLE aplicacoes ADD COLUMN IF NOT EXISTS pipeline_id INTEGER REFERENCES pipelines(id);

CREATE INDEX IF NOT EXISTS idx_aplicacoes_cliente ON aplicacoes(cliente_id);
CREATE INDEX IF NOT EXISTS idx_aplicacoes_projeto ON aplicacoes(projeto_id);

-- ==================== REMOVER TABELA GMUD ====================

-- Comentado para não perder dados imediatamente
-- DROP TABLE IF EXISTS gmuds CASCADE;

-- ==================== TRIGGERS ====================

-- Trigger para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_clientes_updated_at BEFORE UPDATE ON clientes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projetos_updated_at BEFORE UPDATE ON projetos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_repositorios_updated_at BEFORE UPDATE ON repositorios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pipelines_updated_at BEFORE UPDATE ON pipelines
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_work_items_updated_at BEFORE UPDATE ON work_items
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ==================== VIEWS PARA MÉTRICAS ====================

-- View: Métricas de Pipeline por Cliente
CREATE OR REPLACE VIEW vw_pipeline_metrics AS
SELECT 
    c.id as cliente_id,
    c.nome as cliente_nome,
    p.id as projeto_id,
    p.nome as projeto_nome,
    pip.id as pipeline_id,
    pip.nome as pipeline_nome,
    COUNT(pe.id) as total_execucoes,
    SUM(CASE WHEN pe.resultado = 'succeeded' THEN 1 ELSE 0 END) as execucoes_sucesso,
    SUM(CASE WHEN pe.resultado = 'failed' THEN 1 ELSE 0 END) as execucoes_falha,
    ROUND(AVG(pe.duracao_segundos), 2) as duracao_media_segundos,
    MAX(pe.data_inicio) as ultima_execucao
FROM clientes c
JOIN projetos p ON p.cliente_id = c.id
JOIN pipelines pip ON pip.projeto_id = p.id
LEFT JOIN pipeline_execucoes pe ON pe.pipeline_id = pip.id
GROUP BY c.id, c.nome, p.id, p.nome, pip.id, pip.nome;

-- View: Work Items por Cliente
CREATE OR REPLACE VIEW vw_work_items_summary AS
SELECT 
    c.id as cliente_id,
    c.nome as cliente_nome,
    p.id as projeto_id,
    p.nome as projeto_nome,
    wi.tipo,
    wi.estado,
    COUNT(*) as quantidade,
    SUM(wi.story_points) as total_story_points
FROM clientes c
JOIN projetos p ON p.cliente_id = c.id
JOIN work_items wi ON wi.projeto_id = p.id
GROUP BY c.id, c.nome, p.id, p.nome, wi.tipo, wi.estado;

-- View: Deployments por Ambiente
CREATE OR REPLACE VIEW vw_deployments_summary AS
SELECT 
    c.id as cliente_id,
    c.nome as cliente_nome,
    d.ambiente,
    COUNT(*) as total_deployments,
    SUM(CASE WHEN d.status = 'succeeded' THEN 1 ELSE 0 END) as deployments_sucesso,
    MAX(d.data_deploy) as ultimo_deployment
FROM clientes c
JOIN projetos p ON p.cliente_id = c.id
JOIN pipelines pip ON pip.projeto_id = p.id
JOIN deployments d ON d.pipeline_id = pip.id
GROUP BY c.id, c.nome, d.ambiente;

COMMENT ON TABLE clientes IS 'Clientes da consultoria (multi-tenant)';
COMMENT ON TABLE projetos IS 'Projetos do Azure DevOps por cliente';
COMMENT ON TABLE pipelines IS 'Pipelines CI/CD do Azure DevOps';
COMMENT ON TABLE pipeline_execucoes IS 'Histórico de execuções de pipelines';
COMMENT ON TABLE deployments IS 'Histórico de deployments por ambiente';
COMMENT ON TABLE work_items IS 'Work items (User Stories, Bugs, Tasks)';
