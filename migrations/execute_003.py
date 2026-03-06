"""
Script para executar o arquivo 003_stored_procedures.sql no PostgreSQL
"""
import psycopg2
import os
from pathlib import Path
from dotenv import load_dotenv

def execute_sql_file(filepath):
    """Executa um arquivo SQL no PostgreSQL"""
    
    # Carregar variáveis do arquivo .env
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
    
    # Configurações de conexão
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'devops_hub'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', '')
    }
    
    print(f"Conectando ao banco de dados {config['database']} em {config['host']}:{config['port']}...")
    
    try:
        # Conectar ao banco
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Ler o arquivo SQL
        print(f"Lendo arquivo: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Executar o SQL
        print("Executando stored procedures...")
        cursor.execute(sql_content)
        
        print("✓ Stored procedures criadas com sucesso!")
        
        # Listar funções criadas
        cursor.execute("""
            SELECT routine_name, routine_type
            FROM information_schema.routines
            WHERE routine_schema = 'public'
            ORDER BY routine_name;
        """)
        
        functions = cursor.fetchall()
        print(f"\n{len(functions)} funções encontradas no banco:")
        for func_name, func_type in functions:
            print(f"  - {func_name} ({func_type})")
        
        cursor.close()
        conn.close()
        print("\n✓ Execução concluída com sucesso!")
        
    except psycopg2.Error as e:
        print(f"✗ Erro ao executar SQL: {e}")
        raise
    except FileNotFoundError as e:
        print(f"✗ Arquivo não encontrado: {e}")
        raise
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        raise


if __name__ == "__main__":
    # Caminho do arquivo SQL
    sql_file = Path(__file__).parent / "003_stored_procedures.sql"
    
    if not sql_file.exists():
        print(f"✗ Arquivo não encontrado: {sql_file}")
        exit(1)
    
    execute_sql_file(sql_file)
