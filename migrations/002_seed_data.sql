-- Migration: 002_seed_data
-- Description: Popular o banco com dados iniciais dos CSVs
-- Date: 2025-12-05

-- Inserir produtos únicos
INSERT INTO produtos (nome, descricao) VALUES
    ('TOPUP', 'Sistema de recarga e top-up'),
    ('SPB', 'Sistema de Pagamentos Brasileiro'),
    ('Rutas', 'Sistema de rotas e logística')
ON CONFLICT (nome) DO NOTHING;

-- Esta migration deve ser seguida por um script Python para importar os dados dos CSVs
-- Ver: migrations/scripts/import_csv_data.py
