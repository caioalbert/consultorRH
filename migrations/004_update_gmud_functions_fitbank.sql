-- Migration: Stored Procedures para gmud_fitbank
-- Description: Altera as stored procedures para usar gmud_fitbank ao invés de gmuds
-- Date: 2025-12-15

-- Remove as funções antigas
DROP FUNCTION IF EXISTS fn_listar_gmuds(VARCHAR, INTEGER, VARCHAR, TIMESTAMP, TIMESTAMP);
DROP FUNCTION IF EXISTS fn_buscar_gmud_por_id(INTEGER);
DROP FUNCTION IF EXISTS fn_buscar_gmud_por_id_item(VARCHAR);
DROP FUNCTION IF EXISTS fn_obter_stats_gmuds();

-- Listar GMUDs do FitBank com filtros
CREATE OR REPLACE FUNCTION fn_listar_gmuds(
    p_ambiente VARCHAR(50) DEFAULT NULL,
    p_aplicacao_id INTEGER DEFAULT NULL,
    p_risco_operacao VARCHAR(50) DEFAULT NULL,
    p_data_inicio TIMESTAMP DEFAULT NULL,
    p_data_fim TIMESTAMP DEFAULT NULL
)
RETURNS SETOF gmud_fitbank AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM gmud_fitbank
    WHERE (p_ambiente IS NULL OR ambiente = p_ambiente)
      AND (p_aplicacao_id IS NULL OR aplicacao_id = p_aplicacao_id)
      AND (p_risco_operacao IS NULL OR risco_operacao = p_risco_operacao)
      AND (p_data_inicio IS NULL OR data_hora_prevista >= p_data_inicio)
      AND (p_data_fim IS NULL OR data_hora_prevista <= p_data_fim)
    ORDER BY data_hora_prevista DESC;
END;
$$ LANGUAGE plpgsql;

-- Buscar GMUD por ID do FitBank
CREATE OR REPLACE FUNCTION fn_buscar_gmud_por_id(p_id INTEGER)
RETURNS SETOF gmud_fitbank AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM gmud_fitbank WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

-- Buscar GMUD por ID do item do FitBank
CREATE OR REPLACE FUNCTION fn_buscar_gmud_por_id_item(p_id_item VARCHAR(100))
RETURNS SETOF gmud_fitbank AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM gmud_fitbank WHERE id_item = p_id_item;
END;
$$ LANGUAGE plpgsql;

-- Estatísticas de GMUDs do FitBank
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
    FROM gmud_fitbank;
END;
$$ LANGUAGE plpgsql;

-- Comentários
COMMENT ON FUNCTION fn_listar_gmuds IS 'Lista GMUDs do FitBank com filtros opcionais';
COMMENT ON FUNCTION fn_buscar_gmud_por_id IS 'Busca GMUD do FitBank por ID';
COMMENT ON FUNCTION fn_buscar_gmud_por_id_item IS 'Busca GMUD do FitBank por ID do item';
COMMENT ON FUNCTION fn_obter_stats_gmuds IS 'Obtém estatísticas de GMUDs do FitBank';
