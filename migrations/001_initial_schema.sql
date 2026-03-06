-- Migration: 001_initial_schema
-- Description: Criação das tabelas iniciais do banco de dados
-- Date: 2025-12-05

-- Tabela de Produtos
CREATE TABLE IF NOT EXISTS produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Aplicações (Inventário)
CREATE TABLE IF NOT EXISTS aplicacoes (
    id SERIAL PRIMARY KEY,
    nome_aplicacao VARCHAR(200) NOT NULL,
    produto_id INTEGER REFERENCES produtos(id) ON DELETE SET NULL,
    ambiente VARCHAR(50) NOT NULL,
    tipo_aplicacao VARCHAR(100),
    framework VARCHAR(100),
    ferramenta_versionamento VARCHAR(100),
    tipo_pipeline VARCHAR(50),
    versao VARCHAR(50),
    hospedagem VARCHAR(100),
    sbom BOOLEAN DEFAULT FALSE,
    scan_imagens BOOLEAN DEFAULT FALSE,
    secret_manager BOOLEAN DEFAULT FALSE,
    sast_sonarqube BOOLEAN DEFAULT FALSE,
    data_ultima_revisao DATE,
    data_criacao DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_aplicacao_ambiente UNIQUE (nome_aplicacao, ambiente)
);

-- Tabela de GMUDs (Change Management)
CREATE TABLE IF NOT EXISTS gmuds (
    id SERIAL PRIMARY KEY,
    id_item VARCHAR(100) NOT NULL UNIQUE,
    data_hora_prevista TIMESTAMP,
    responsavel_executor VARCHAR(200),
    tempo_estimado VARCHAR(50),
    solicitante_area VARCHAR(200),
    nome_aplicacao VARCHAR(200),
    aplicacao_id INTEGER REFERENCES aplicacoes(id) ON DELETE SET NULL,
    ambiente VARCHAR(50),
    hostname_namespace VARCHAR(200),
    local_implantacao VARCHAR(100),
    build_release TEXT,
    configuracoes_alteradas TEXT,
    tempo_realizado VARCHAR(50),
    ocorrencias TEXT,
    solucoes_atribuidas TEXT,
    validacoes_realizadas TEXT,
    risco_operacao VARCHAR(50),
    impacto TEXT,
    rca TEXT,
    controle VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para melhorar performance
CREATE INDEX idx_aplicacoes_produto ON aplicacoes(produto_id);
CREATE INDEX idx_aplicacoes_ambiente ON aplicacoes(ambiente);
CREATE INDEX idx_aplicacoes_nome ON aplicacoes(nome_aplicacao);
CREATE INDEX idx_gmuds_aplicacao ON gmuds(aplicacao_id);
CREATE INDEX idx_gmuds_ambiente ON gmuds(ambiente);
CREATE INDEX idx_gmuds_data ON gmuds(data_hora_prevista);

-- Função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para atualizar updated_at
CREATE TRIGGER update_produtos_updated_at BEFORE UPDATE ON produtos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_aplicacoes_updated_at BEFORE UPDATE ON aplicacoes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_gmuds_updated_at BEFORE UPDATE ON gmuds
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comentários nas tabelas
COMMENT ON TABLE produtos IS 'Catálogo de produtos/sistemas';
COMMENT ON TABLE aplicacoes IS 'Inventário de aplicações com informações de DevOps e SecOps';
COMMENT ON TABLE gmuds IS 'Registro de mudanças (GMUDs) no ambiente';
