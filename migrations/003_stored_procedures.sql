-- Migration: 003_stored_procedures
-- Description: Criação de funções (FUNCTION) simplificadas para operações CRUD
-- Date: 2025-12-08
-- Note: Funções retornam SETOF table_name para simplicidade (sem RETURNS TABLE)

-- ============================================================================
-- FUNÇÕES - PRODUTOS
-- ============================================================================

-- Criar produto
CREATE OR REPLACE FUNCTION fn_criar_produto(
    p_nome VARCHAR(100),
    p_descricao TEXT DEFAULT NULL
)
RETURNS SETOF produtos AS $$
BEGIN
    RETURN QUERY
    INSERT INTO produtos (nome, descricao)
    VALUES (p_nome, p_descricao)
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

-- Buscar produto por ID
CREATE OR REPLACE FUNCTION fn_buscar_produto_por_id(p_id INTEGER)
RETURNS SETOF produtos AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM produtos WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

-- Buscar produto por nome
CREATE OR REPLACE FUNCTION fn_buscar_produto_por_nome(p_nome VARCHAR(100))
RETURNS SETOF produtos AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM produtos WHERE nome = p_nome;
END;
$$ LANGUAGE plpgsql;

-- Listar todos os produtos
CREATE OR REPLACE FUNCTION fn_listar_produtos()
RETURNS SETOF produtos AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM produtos ORDER BY nome;
END;
$$ LANGUAGE plpgsql;

-- Atualizar produto
CREATE OR REPLACE FUNCTION fn_atualizar_produto(
    p_id INTEGER,
    p_nome VARCHAR(100),
    p_descricao TEXT DEFAULT NULL
)
RETURNS SETOF produtos AS $$
BEGIN
    RETURN QUERY
    UPDATE produtos
    SET nome = p_nome, descricao = p_descricao
    WHERE id = p_id
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

-- Deletar produto
CREATE OR REPLACE FUNCTION fn_deletar_produto(p_id INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM produtos WHERE id = p_id;
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

-- Get or Create Produto
CREATE OR REPLACE FUNCTION fn_get_or_create_produto(
    p_nome VARCHAR(100),
    p_descricao TEXT DEFAULT NULL
)
RETURNS SETOF produtos AS $$
DECLARE
    v_produto produtos;
BEGIN
    SELECT * INTO v_produto FROM produtos WHERE nome = p_nome;
    
    IF FOUND THEN
        RETURN NEXT v_produto;
    ELSE
        RETURN QUERY
        INSERT INTO produtos (nome, descricao)
        VALUES (p_nome, p_descricao)
        RETURNING *;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- FUNÇÕES - APLICAÇÕES
-- ============================================================================

-- Criar aplicação
CREATE OR REPLACE FUNCTION fn_criar_aplicacao(
    p_nome_aplicacao VARCHAR(200),
    p_produto_id INTEGER,
    p_ambiente VARCHAR(50),
    p_tipo_aplicacao VARCHAR(100) DEFAULT NULL,
    p_framework VARCHAR(100) DEFAULT NULL,
    p_ferramenta_versionamento VARCHAR(100) DEFAULT NULL,
    p_tipo_pipeline VARCHAR(50) DEFAULT NULL,
    p_versao VARCHAR(50) DEFAULT NULL,
    p_hospedagem VARCHAR(100) DEFAULT NULL,
    p_sbom BOOLEAN DEFAULT FALSE,
    p_scan_imagens BOOLEAN DEFAULT FALSE,
    p_secret_manager BOOLEAN DEFAULT FALSE,
    p_sast_sonarqube BOOLEAN DEFAULT FALSE,
    p_data_ultima_revisao DATE DEFAULT NULL,
    p_data_criacao DATE DEFAULT NULL
)
RETURNS SETOF aplicacoes AS $$
BEGIN
    RETURN QUERY
    INSERT INTO aplicacoes (
        nome_aplicacao, produto_id, ambiente, tipo_aplicacao,
        framework, ferramenta_versionamento, tipo_pipeline, versao,
        hospedagem, sbom, scan_imagens, secret_manager, sast_sonarqube,
        data_ultima_revisao, data_criacao
    )
    VALUES (
        p_nome_aplicacao, p_produto_id, p_ambiente, p_tipo_aplicacao,
        p_framework, p_ferramenta_versionamento, p_tipo_pipeline, p_versao,
        p_hospedagem, p_sbom, p_scan_imagens, p_secret_manager, p_sast_sonarqube,
        p_data_ultima_revisao, p_data_criacao
    )
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

-- Buscar aplicação por ID
CREATE OR REPLACE FUNCTION fn_buscar_aplicacao_por_id(p_id INTEGER)
RETURNS TABLE(
    id INTEGER,
    nome_aplicacao VARCHAR(200),
    produto_id INTEGER,
    ambiente VARCHAR(50),
    tipo_aplicacao VARCHAR(100),
    framework VARCHAR(100),
    ferramenta_versionamento VARCHAR(100),
    tipo_pipeline VARCHAR(50),
    versao VARCHAR(50),
    hospedagem VARCHAR(100),
    sbom BOOLEAN,
    scan_imagens BOOLEAN,
    secret_manager BOOLEAN,
    sast_sonarqube BOOLEAN,
    data_ultima_revisao DATE,
    data_criacao DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    produto_nome VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY
    SELECT a.*, p.nome
    FROM aplicacoes a
    LEFT JOIN produtos p ON a.produto_id = p.id
    WHERE a.id = p_id;
END;
$$ LANGUAGE plpgsql;

-- Listar aplicações com filtros
CREATE OR REPLACE FUNCTION fn_listar_aplicacoes(
    p_produto_id INTEGER DEFAULT NULL,
    p_ambiente VARCHAR(50) DEFAULT NULL,
    p_tipo_aplicacao VARCHAR(100) DEFAULT NULL,
    p_framework VARCHAR(100) DEFAULT NULL
)
RETURNS TABLE(
    id INTEGER,
    nome_aplicacao VARCHAR(200),
    produto_id INTEGER,
    ambiente VARCHAR(50),
    tipo_aplicacao VARCHAR(100),
    framework VARCHAR(100),
    ferramenta_versionamento VARCHAR(100),
    tipo_pipeline VARCHAR(50),
    versao VARCHAR(50),
    hospedagem VARCHAR(100),
    sbom BOOLEAN,
    scan_imagens BOOLEAN,
    secret_manager BOOLEAN,
    sast_sonarqube BOOLEAN,
    data_ultima_revisao DATE,
    data_criacao DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    produto_nome VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY
    SELECT a.*, p.nome
    FROM aplicacoes a
    LEFT JOIN produtos p ON a.produto_id = p.id
    WHERE (p_produto_id IS NULL OR a.produto_id = p_produto_id)
      AND (p_ambiente IS NULL OR a.ambiente = p_ambiente)
      AND (p_tipo_aplicacao IS NULL OR a.tipo_aplicacao = p_tipo_aplicacao)
      AND (p_framework IS NULL OR a.framework = p_framework)
    ORDER BY a.nome_aplicacao;
END;
$$ LANGUAGE plpgsql;

-- Buscar aplicações por produto
CREATE OR REPLACE FUNCTION fn_buscar_aplicacoes_por_produto(p_produto_id INTEGER)
RETURNS TABLE(
    id INTEGER,
    nome_aplicacao VARCHAR(200),
    produto_id INTEGER,
    ambiente VARCHAR(50),
    tipo_aplicacao VARCHAR(100),
    framework VARCHAR(100),
    ferramenta_versionamento VARCHAR(100),
    tipo_pipeline VARCHAR(50),
    versao VARCHAR(50),
    hospedagem VARCHAR(100),
    sbom BOOLEAN,
    scan_imagens BOOLEAN,
    secret_manager BOOLEAN,
    sast_sonarqube BOOLEAN,
    data_ultima_revisao DATE,
    data_criacao DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    produto_nome VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY
    SELECT a.*, p.nome
    FROM aplicacoes a
    LEFT JOIN produtos p ON a.produto_id = p.id
    WHERE a.produto_id = p_produto_id
    ORDER BY a.nome_aplicacao;
END;
$$ LANGUAGE plpgsql;

-- Buscar aplicações por ambiente
CREATE OR REPLACE FUNCTION fn_buscar_aplicacoes_por_ambiente(p_ambiente VARCHAR(50))
RETURNS TABLE(
    id INTEGER,
    nome_aplicacao VARCHAR(200),
    produto_id INTEGER,
    ambiente VARCHAR(50),
    tipo_aplicacao VARCHAR(100),
    framework VARCHAR(100),
    ferramenta_versionamento VARCHAR(100),
    tipo_pipeline VARCHAR(50),
    versao VARCHAR(50),
    hospedagem VARCHAR(100),
    sbom BOOLEAN,
    scan_imagens BOOLEAN,
    secret_manager BOOLEAN,
    sast_sonarqube BOOLEAN,
    data_ultima_revisao DATE,
    data_criacao DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    produto_nome VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY
    SELECT a.*, p.nome
    FROM aplicacoes a
    LEFT JOIN produtos p ON a.produto_id = p.id
    WHERE a.ambiente = p_ambiente
    ORDER BY a.nome_aplicacao;
END;
$$ LANGUAGE plpgsql;

-- Atualizar aplicação
CREATE OR REPLACE FUNCTION fn_atualizar_aplicacao(
    p_id INTEGER,
    p_nome_aplicacao VARCHAR(200),
    p_produto_id INTEGER,
    p_ambiente VARCHAR(50),
    p_tipo_aplicacao VARCHAR(100) DEFAULT NULL,
    p_framework VARCHAR(100) DEFAULT NULL,
    p_ferramenta_versionamento VARCHAR(100) DEFAULT NULL,
    p_tipo_pipeline VARCHAR(50) DEFAULT NULL,
    p_versao VARCHAR(50) DEFAULT NULL,
    p_hospedagem VARCHAR(100) DEFAULT NULL,
    p_sbom BOOLEAN DEFAULT FALSE,
    p_scan_imagens BOOLEAN DEFAULT FALSE,
    p_secret_manager BOOLEAN DEFAULT FALSE,
    p_sast_sonarqube BOOLEAN DEFAULT FALSE,
    p_data_ultima_revisao DATE DEFAULT NULL,
    p_data_criacao DATE DEFAULT NULL
)
RETURNS SETOF aplicacoes AS $$
BEGIN
    RETURN QUERY
    UPDATE aplicacoes
    SET nome_aplicacao = p_nome_aplicacao,
        produto_id = p_produto_id,
        ambiente = p_ambiente,
        tipo_aplicacao = p_tipo_aplicacao,
        framework = p_framework,
        ferramenta_versionamento = p_ferramenta_versionamento,
        tipo_pipeline = p_tipo_pipeline,
        versao = p_versao,
        hospedagem = p_hospedagem,
        sbom = p_sbom,
        scan_imagens = p_scan_imagens,
        secret_manager = p_secret_manager,
        sast_sonarqube = p_sast_sonarqube,
        data_ultima_revisao = p_data_ultima_revisao,
        data_criacao = p_data_criacao
    WHERE id = p_id
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

-- Deletar aplicação
CREATE OR REPLACE FUNCTION fn_deletar_aplicacao(p_id INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM aplicacoes WHERE id = p_id;
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

-- Estatísticas de aplicações
CREATE OR REPLACE FUNCTION fn_obter_stats_aplicacoes()
RETURNS TABLE(
    total_aplicacoes BIGINT,
    total_produtos BIGINT,
    total_ambientes BIGINT,
    total_frameworks BIGINT,
    com_sbom BIGINT,
    com_scan BIGINT,
    com_secret_manager BIGINT,
    com_sast BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(*)::BIGINT,
        COUNT(DISTINCT produto_id)::BIGINT,
        COUNT(DISTINCT ambiente)::BIGINT,
        COUNT(DISTINCT framework)::BIGINT,
        SUM(CASE WHEN sbom THEN 1 ELSE 0 END)::BIGINT,
        SUM(CASE WHEN scan_imagens THEN 1 ELSE 0 END)::BIGINT,
        SUM(CASE WHEN secret_manager THEN 1 ELSE 0 END)::BIGINT,
        SUM(CASE WHEN sast_sonarqube THEN 1 ELSE 0 END)::BIGINT
    FROM aplicacoes;
END;
$$ LANGUAGE plpgsql;

-- Buscar aplicações por termo
CREATE OR REPLACE FUNCTION fn_buscar_aplicacoes_por_termo(p_termo VARCHAR(200))
RETURNS TABLE(
    id INTEGER,
    nome_aplicacao VARCHAR(200),
    produto_id INTEGER,
    ambiente VARCHAR(50),
    tipo_aplicacao VARCHAR(100),
    framework VARCHAR(100),
    ferramenta_versionamento VARCHAR(100),
    tipo_pipeline VARCHAR(50),
    versao VARCHAR(50),
    hospedagem VARCHAR(100),
    sbom BOOLEAN,
    scan_imagens BOOLEAN,
    secret_manager BOOLEAN,
    sast_sonarqube BOOLEAN,
    data_ultima_revisao DATE,
    data_criacao DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    produto_nome VARCHAR(100)
) AS $$
BEGIN
    RETURN QUERY
    SELECT a.*, p.nome
    FROM aplicacoes a
    LEFT JOIN produtos p ON a.produto_id = p.id
    WHERE a.nome_aplicacao ILIKE '%' || p_termo || '%'
    ORDER BY a.nome_aplicacao;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- FUNÇÕES - GMUDS
-- ============================================================================

-- Criar GMUD
CREATE OR REPLACE FUNCTION fn_criar_gmud(
    p_id_item VARCHAR(100),
    p_data_hora_prevista TIMESTAMP DEFAULT NULL,
    p_responsavel_executor VARCHAR(200) DEFAULT NULL,
    p_tempo_estimado VARCHAR(50) DEFAULT NULL,
    p_solicitante_area VARCHAR(200) DEFAULT NULL,
    p_aplicacao_id INTEGER DEFAULT NULL,
    p_ambiente VARCHAR(50) DEFAULT NULL,
    p_hostname_namespace VARCHAR(200) DEFAULT NULL,
    p_local_implantacao VARCHAR(100) DEFAULT NULL,
    p_build_release TEXT DEFAULT NULL,
    p_configuracoes_alteradas TEXT DEFAULT NULL,
    p_tempo_realizado VARCHAR(50) DEFAULT NULL,
    p_ocorrencias TEXT DEFAULT NULL,
    p_solucoes_atribuidas TEXT DEFAULT NULL,
    p_validacoes_realizadas TEXT DEFAULT NULL,
    p_risco_operacao VARCHAR(50) DEFAULT NULL,
    p_impacto TEXT DEFAULT NULL,
    p_rca TEXT DEFAULT NULL,
    p_controle VARCHAR(200) DEFAULT NULL
)
RETURNS SETOF gmuds AS $$
BEGIN
    RETURN QUERY
    INSERT INTO gmuds (
        id_item, data_hora_prevista, responsavel_executor, tempo_estimado,
        solicitante_area, aplicacao_id, ambiente,
        hostname_namespace, local_implantacao, build_release,
        configuracoes_alteradas, tempo_realizado, ocorrencias,
        solucoes_atribuidas, validacoes_realizadas, risco_operacao,
        impacto, rca, controle
    )
    VALUES (
        p_id_item, p_data_hora_prevista, p_responsavel_executor, p_tempo_estimado,
        p_solicitante_area, p_aplicacao_id, p_ambiente,
        p_hostname_namespace, p_local_implantacao, p_build_release,
        p_configuracoes_alteradas, p_tempo_realizado, p_ocorrencias,
        p_solucoes_atribuidas, p_validacoes_realizadas, p_risco_operacao,
        p_impacto, p_rca, p_controle
    )
    RETURNING *;
END;
$$ LANGUAGE plpgsql;

-- Buscar GMUD por ID
CREATE OR REPLACE FUNCTION fn_buscar_gmud_por_id(p_id INTEGER)
RETURNS SETOF gmuds AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM gmuds WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

-- Buscar GMUD por ID do item
CREATE OR REPLACE FUNCTION fn_buscar_gmud_por_id_item(p_id_item VARCHAR(100))
RETURNS SETOF gmuds AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM gmuds WHERE id_item = p_id_item;
END;
$$ LANGUAGE plpgsql;

-- Listar GMUDs com filtros
CREATE OR REPLACE FUNCTION fn_listar_gmuds(
    p_ambiente VARCHAR(50) DEFAULT NULL,
    p_aplicacao_id INTEGER DEFAULT NULL,
    p_risco_operacao VARCHAR(50) DEFAULT NULL,
    p_data_inicio TIMESTAMP DEFAULT NULL,
    p_data_fim TIMESTAMP DEFAULT NULL
)
RETURNS SETOF gmuds AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM gmuds
    WHERE (p_ambiente IS NULL OR ambiente = p_ambiente)
      AND (p_aplicacao_id IS NULL OR aplicacao_id = p_aplicacao_id)
      AND (p_risco_operacao IS NULL OR risco_operacao = p_risco_operacao)
      AND (p_data_inicio IS NULL OR data_hora_prevista >= p_data_inicio)
      AND (p_data_fim IS NULL OR data_hora_prevista <= p_data_fim)
    ORDER BY data_hora_prevista DESC;
END;
$$ LANGUAGE plpgsql;

-- Atualizar GMUD
CREATE OR REPLACE FUNCTION fn_atualizar_gmud(
    p_id INTEGER,
    p_id_item VARCHAR(100),
    p_data_hora_prevista TIMESTAMP DEFAULT NULL,
    p_responsavel_executor VARCHAR(200) DEFAULT NULL,
    p_tempo_estimado VARCHAR(50) DEFAULT NULL,
    p_solicitante_area VARCHAR(200) DEFAULT NULL,
    p_aplicacao_id INTEGER DEFAULT NULL,
    p_ambiente VARCHAR(50) DEFAULT NULL,
    p_hostname_namespace VARCHAR(200) DEFAULT NULL,
    p_local_implantacao VARCHAR(100) DEFAULT NULL,
    p_build_release TEXT DEFAULT NULL,
    p_configuracoes_alteradas TEXT DEFAULT NULL,
    p_tempo_realizado VARCHAR(50) DEFAULT NULL,
    p_ocorrencias TEXT DEFAULT NULL,
    p_solucoes_atribuidas TEXT DEFAULT NULL,
    p_validacoes_realizadas TEXT DEFAULT NULL,
    p_risco_operacao VARCHAR(50) DEFAULT NULL,
    p_impacto TEXT DEFAULT NULL,
    p_rca TEXT DEFAULT NULL,
    p_controle VARCHAR(200) DEFAULT NULL
)
RETURNS SETOF gmuds AS $$
BEGIN
    RETURN QUERY
    UPDATE gmuds
    SET id_item = p_id_item,
        data_hora_prevista = p_data_hora_prevista,
        responsavel_executor = p_responsavel_executor,
        tempo_estimado = p_tempo_estimado,
        solicitante_area = p_solicitante_area,
        aplicacao_id = p_aplicacao_id,
        ambiente = p_ambiente,
        hostname_namespace = p_hostname_namespace,
        local_implantacao = p_local_implantacao,
        build_release = p_build_release,
        configuracoes_alteradas = p_configuracoes_alteradas,
        tempo_realizado = p_tempo_realizado,
        ocorrencias = p_ocorrencias,
        solucoes_atribuidas = p_solucoes_atribuidas,
        validacoes_realizadas = p_validacoes_realizadas,
        risco_operacao = p_risco_operacao,
        impacto = p_impacto,
        rca = p_rca,
        controle = p_controle
    WHERE gmuds.id = p_id
    RETURNING *;
END;
$$ LANGUAGE plpgsql;
-- Deletar GMUD
CREATE OR REPLACE FUNCTION fn_deletar_gmud(p_id INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
    DELETE FROM gmuds WHERE id = p_id;
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;

-- Estatísticas de GMUDs
CREATE OR REPLACE FUNCTION fn_obter_stats_gmuds()
RETURNS TABLE(
    total_gmuds BIGINT,
    total_ambientes BIGINT,
    total_aplicacoes BIGINT,
    risco_alto BIGINT,
    risco_medio BIGINT,
    risco_baixo BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        COUNT(*)::BIGINT,
        COUNT(DISTINCT ambiente)::BIGINT,
        COUNT(DISTINCT nome_aplicacao)::BIGINT,
        SUM(CASE WHEN risco_operacao = 'Alto' THEN 1 ELSE 0 END)::BIGINT,
        SUM(CASE WHEN risco_operacao = 'Médio' THEN 1 ELSE 0 END)::BIGINT,
        SUM(CASE WHEN risco_operacao = 'Baixo' THEN 1 ELSE 0 END)::BIGINT
    FROM gmuds;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- COMENTÁRIOS DAS FUNÇÕES
-- ============================================================================

COMMENT ON FUNCTION fn_criar_produto IS 'Cria um novo produto';
COMMENT ON FUNCTION fn_buscar_produto_por_id IS 'Busca produto por ID';
COMMENT ON FUNCTION fn_buscar_produto_por_nome IS 'Busca produto por nome';
COMMENT ON FUNCTION fn_listar_produtos IS 'Lista todos os produtos';
COMMENT ON FUNCTION fn_atualizar_produto IS 'Atualiza um produto';
COMMENT ON FUNCTION fn_deletar_produto IS 'Deleta um produto';
COMMENT ON FUNCTION fn_get_or_create_produto IS 'Busca ou cria um produto';

COMMENT ON FUNCTION fn_criar_aplicacao IS 'Cria uma nova aplicação';
COMMENT ON FUNCTION fn_buscar_aplicacao_por_id IS 'Busca aplicação por ID com join de produto';
COMMENT ON FUNCTION fn_listar_aplicacoes IS 'Lista aplicações com filtros opcionais';
COMMENT ON FUNCTION fn_atualizar_aplicacao IS 'Atualiza uma aplicação';
COMMENT ON FUNCTION fn_deletar_aplicacao IS 'Deleta uma aplicação';
COMMENT ON FUNCTION fn_buscar_aplicacoes_por_produto IS 'Busca aplicações por produto';
COMMENT ON FUNCTION fn_buscar_aplicacoes_por_ambiente IS 'Busca aplicações por ambiente';
COMMENT ON FUNCTION fn_obter_stats_aplicacoes IS 'Obtém estatísticas de aplicações';
COMMENT ON FUNCTION fn_buscar_aplicacoes_por_termo IS 'Busca aplicações por termo (ILIKE)';

COMMENT ON FUNCTION fn_criar_gmud IS 'Cria uma nova GMUD';
COMMENT ON FUNCTION fn_buscar_gmud_por_id IS 'Busca GMUD por ID';
COMMENT ON FUNCTION fn_buscar_gmud_por_id_item IS 'Busca GMUD por ID do item';
COMMENT ON FUNCTION fn_listar_gmuds IS 'Lista GMUDs com filtros opcionais';
COMMENT ON FUNCTION fn_atualizar_gmud IS 'Atualiza uma GMUD';
COMMENT ON FUNCTION fn_deletar_gmud IS 'Deleta uma GMUD';
COMMENT ON FUNCTION fn_obter_stats_gmuds IS 'Obtém estatísticas de GMUDs';
