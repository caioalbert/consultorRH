"""
Gerenciador de migrations do banco de dados PostgreSQL
"""
import psycopg2
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'devops_hub'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '')
}

def connect_db():
    """Conecta ao banco de dados"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        raise

def create_migrations_table(conn):
    """Cria a tabela de controle de migrations"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id SERIAL PRIMARY KEY,
            version VARCHAR(100) NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            execution_time_ms INTEGER
        )
    """)
    conn.commit()
    print("✓ Tabela de migrations criada")

def get_applied_migrations(conn):
    """Retorna lista de migrations já aplicadas"""
    cursor = conn.cursor()
    cursor.execute("SELECT version FROM schema_migrations ORDER BY version")
    return [row[0] for row in cursor.fetchall()]

def apply_migration(conn, migration_file):
    """Aplica uma migration específica"""
    cursor = conn.cursor()
    version = migration_file.stem
    
    print(f"\nAplicando migration: {version}")
    
    # Ler arquivo SQL
    with open(migration_file, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Executar migration
    start_time = datetime.now()
    try:
        cursor.execute(sql)
        
        # Registrar migration
        execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
        cursor.execute(
            "INSERT INTO schema_migrations (version, execution_time_ms) VALUES (%s, %s)",
            (version, execution_time)
        )
        
        conn.commit()
        print(f"✓ Migration {version} aplicada com sucesso ({execution_time}ms)")
        return True
    except Exception as e:
        conn.rollback()
        print(f"❌ Erro ao aplicar migration {version}: {e}")
        return False

def run_migrations():
    """Executa todas as migrations pendentes"""
    print("=== Gerenciador de Migrations ===\n")
    
    # Conectar ao banco
    print("Conectando ao banco de dados...")
    conn = connect_db()
    print("✓ Conectado com sucesso\n")
    
    # Criar tabela de controle
    create_migrations_table(conn)
    
    # Obter migrations aplicadas
    applied = get_applied_migrations(conn)
    print(f"Migrations já aplicadas: {len(applied)}")
    
    # Listar arquivos de migration
    migrations_dir = Path(__file__).parent
    migration_files = sorted(migrations_dir.glob("*.sql"))
    
    if not migration_files:
        print("\n⚠️  Nenhuma migration encontrada")
        return
    
    print(f"Migrations disponíveis: {len(migration_files)}\n")
    
    # Aplicar migrations pendentes
    pending = [f for f in migration_files if f.stem not in applied]
    
    if not pending:
        print("✅ Todas as migrations já foram aplicadas!")
        conn.close()
        return
    
    print(f"Migrations pendentes: {len(pending)}\n")
    
    success_count = 0
    for migration_file in pending:
        if apply_migration(conn, migration_file):
            success_count += 1
        else:
            print("\n⚠️  Parando execução devido a erro na migration")
            break
    
    conn.close()
    
    print(f"\n✅ {success_count} migration(s) aplicada(s) com sucesso!")
    
    if success_count < len(pending):
        print(f"⚠️  {len(pending) - success_count} migration(s) falharam")

def rollback_migration(version):
    """Reverte uma migration específica (implementar conforme necessidade)"""
    print(f"⚠️  Rollback não implementado para version: {version}")
    print("Por favor, crie manualmente a migration de rollback se necessário")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        if len(sys.argv) > 2:
            rollback_migration(sys.argv[2])
        else:
            print("❌ Uso: python migrate.py rollback <version>")
    else:
        run_migrations()
