#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para executar a migration 004 e inserir dados iniciais
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from dotenv import load_dotenv
import psycopg2

# Carrega variáveis de ambiente
load_dotenv()


def main():
    """Função principal"""
    print("=" * 70)
    print("  INSERÇÃO DE DADOS INICIAIS - PostgreSQL AWS RDS")
    print("=" * 70)
    
    # Conecta ao banco
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT', 5432),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        print("\n✓ Conexão estabelecida com sucesso!")
    except Exception as e:
        print(f"\n✗ Erro ao conectar: {e}")
        return
    
    # Lê o arquivo SQL
    sql_file = root_dir / "migrations" / "004_insert_data.sql"
    
    if not sql_file.exists():
        print(f"\n✗ Arquivo não encontrado: {sql_file}")
        conn.close()
        return
    
    print(f"\nℹ Executando {sql_file.name}...")
    
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        cursor = conn.cursor()
        cursor.execute(sql_content)
        
        # Pega os resultados da verificação final
        results = cursor.fetchall()
        
        conn.commit()
        cursor.close()
        
        print("\n✓ Migration executada com sucesso!")
        print("\n" + "=" * 70)
        print("  RESUMO DA INSERÇÃO")
        print("=" * 70)
        
        for row in results:
            print(f"  {row[0]} {row[1]}")
        
        print("=" * 70)
        print("\n✓ PROCESSO CONCLUÍDO COM SUCESSO!")
        
    except Exception as e:
        print(f"\n✗ Erro ao executar SQL: {e}")
        conn.rollback()
    
    finally:
        conn.close()
        print("\n✓ Conexão fechada")


if __name__ == "__main__":
    main()
