"""
Executa o script SQL para atualizar as stored procedures para gmud_fitbank
"""
import psycopg2
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def execute_sql_file(filepath):
    """Executa um arquivo SQL no PostgreSQL"""
    
    config = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }
    
    print(f"Conectando ao banco de dados {config['database']}...")
    
    try:
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print(f"Lendo arquivo: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("Executando atualização das stored procedures...")
        cursor.execute(sql_content)
        
        print("✓ Stored procedures atualizadas para usar gmud_fitbank!")
        
        # Testa a nova função
        cursor.execute("SELECT COUNT(*) FROM fn_listar_gmuds(NULL, NULL, NULL, NULL, NULL)")
        total = cursor.fetchone()[0]
        print(f"✓ Teste: {total} GMUDs disponíveis via stored procedure fn_listar_gmuds()")
        
        cursor.close()
        conn.close()
        print("\n✓ Migração concluída com sucesso!")
        
    except Exception as e:
        print(f"✗ Erro: {e}")
        raise

if __name__ == "__main__":
    sql_file = Path(__file__).parent / "migrations" / "004_update_gmud_functions_fitbank.sql"
    execute_sql_file(sql_file)
