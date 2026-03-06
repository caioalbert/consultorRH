#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar dados carregados no banco
"""

import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()


def main():
    print("=" * 70)
    print("  VERIFICAÇÃO DE DADOS - PostgreSQL AWS RDS")
    print("=" * 70)
    
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    cursor = conn.cursor()
    
    # Produtos
    print("\n📦 PRODUTOS:")
    cursor.execute("SELECT id, nome, descricao FROM produtos ORDER BY nome")
    for row in cursor.fetchall():
        print(f"  [{row[0]}] {row[1]} - {row[2]}")
    
    # Aplicações por produto
    print("\n🔧 APLICAÇÕES POR PRODUTO:")
    cursor.execute("""
        SELECT p.nome, COUNT(a.id), 
               COUNT(CASE WHEN a.ambiente = 'Produção' THEN 1 END) as prod,
               COUNT(CASE WHEN a.ambiente = 'Sandbox' THEN 1 END) as sandbox
        FROM produtos p
        LEFT JOIN aplicacoes a ON a.produto_id = p.id
        GROUP BY p.nome
        ORDER BY p.nome
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]} total (Produção: {row[2]}, Sandbox: {row[3]})")
    
    # Aplicações por ambiente
    print("\n🌍 APLICAÇÕES POR AMBIENTE:")
    cursor.execute("""
        SELECT ambiente, COUNT(*) 
        FROM aplicacoes 
        GROUP BY ambiente 
        ORDER BY COUNT(*) DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    # Aplicações por tipo
    print("\n📱 APLICAÇÕES POR TIPO:")
    cursor.execute("""
        SELECT tipo_aplicacao, COUNT(*) 
        FROM aplicacoes 
        WHERE tipo_aplicacao IS NOT NULL
        GROUP BY tipo_aplicacao 
        ORDER BY COUNT(*) DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    # Aplicações por hospedagem
    print("\n☁️ APLICAÇÕES POR HOSPEDAGEM:")
    cursor.execute("""
        SELECT hospedagem, COUNT(*) 
        FROM aplicacoes 
        WHERE hospedagem IS NOT NULL
        GROUP BY hospedagem 
        ORDER BY COUNT(*) DESC
    """)
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    # Security compliance
    print("\n🔒 SEGURANÇA (% de aplicações com cada controle):")
    cursor.execute("""
        SELECT 
            ROUND(AVG(CASE WHEN sbom THEN 100 ELSE 0 END), 1) as sbom_pct,
            ROUND(AVG(CASE WHEN scan_imagens THEN 100 ELSE 0 END), 1) as scan_pct,
            ROUND(AVG(CASE WHEN secret_manager THEN 100 ELSE 0 END), 1) as secret_pct,
            ROUND(AVG(CASE WHEN sast_sonarqube THEN 100 ELSE 0 END), 1) as sast_pct
        FROM aplicacoes
    """)
    row = cursor.fetchone()
    print(f"  SBOM: {row[0]}%")
    print(f"  Scan de Imagens: {row[1]}%")
    print(f"  Secret Manager: {row[2]}%")
    print(f"  SAST (SonarQube): {row[3]}%")
    
    # GMUDs
    print("\n📋 GMUDs:")
    cursor.execute("SELECT COUNT(*) FROM gmuds")
    print(f"  Total: {cursor.fetchone()[0]}")
    
    # GMUDs por risco
    cursor.execute("""
        SELECT risco_operacao, COUNT(*) 
        FROM gmuds 
        WHERE risco_operacao IS NOT NULL
        GROUP BY risco_operacao 
        ORDER BY 
            CASE risco_operacao 
                WHEN 'Baixo' THEN 1 
                WHEN 'Médio' THEN 2 
                WHEN 'Alto' THEN 3 
                WHEN 'Altíssimo' THEN 4 
            END
    """)
    print("\n  Por nível de risco:")
    for row in cursor.fetchall():
        print(f"    {row[0]}: {row[1]}")
    
    # GMUDs por ambiente
    cursor.execute("""
        SELECT ambiente, COUNT(*) 
        FROM gmuds 
        WHERE ambiente IS NOT NULL
        GROUP BY ambiente 
        ORDER BY COUNT(*) DESC
    """)
    print("\n  Por ambiente:")
    for row in cursor.fetchall():
        print(f"    {row[0]}: {row[1]}")
    
    # Últimas GMUDs
    print("\n  📅 Últimas 5 GMUDs:")
    cursor.execute("""
        SELECT g.id_item, g.responsavel_executor, 
               COALESCE(a.nome_aplicacao, g.nome_aplicacao, 'N/A') as app,
               g.ambiente, g.risco_operacao
        FROM gmuds g
        LEFT JOIN aplicacoes a ON a.id = g.aplicacao_id
        ORDER BY g.id DESC
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"    [{row[0]}] {row[1]} - {row[2]} ({row[3]}) - Risco: {row[4]}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
