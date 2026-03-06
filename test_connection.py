"""
Script de teste de conexão com PostgreSQL
Testa a conectividade com o banco de dados AWS RDS
"""
import os
import sys
from datetime import datetime
import psycopg2
from psycopg2 import OperationalError, sql
from dotenv import load_dotenv

# Cores para output no terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    """Imprime cabeçalho do script"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*70}")
    print(f"  TESTE DE CONEXÃO - PostgreSQL AWS RDS")
    print(f"{'='*70}{Colors.END}\n")

def print_success(message):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.GREEN}✓ {message}{Colors.END}")

def print_error(message):
    """Imprime mensagem de erro"""
    print(f"{Colors.RED}✗ {message}{Colors.END}")

def print_info(message):
    """Imprime mensagem informativa"""
    print(f"{Colors.YELLOW}ℹ {message}{Colors.END}")

def load_config():
    """Carrega configurações do arquivo .env"""
    print_info("Carregando configurações do arquivo .env...")
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    config = {
        'host': os.getenv('DB_HOST'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    # Valida se todas as configurações foram carregadas
    missing = [key for key, value in config.items() if not value]
    if missing:
        print_error(f"Configurações faltando no .env: {', '.join(missing)}")
        print_info("Copie .env.example para .env e preencha as credenciais")
        return None
    
    print_success("Configurações carregadas com sucesso")
    return config

def test_connection(config):
    """Testa a conexão com o banco de dados"""
    print_info("Tentando conectar ao banco de dados...")
    print(f"  Host: {config['host']}")
    print(f"  Database: {config['database']}")
    print(f"  User: {config['user']}")
    print(f"  Port: {config['port']}\n")
    
    try:
        # Tenta estabelecer conexão
        conn = psycopg2.connect(
            host=config['host'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            port=config['port'],
            connect_timeout=10
        )
        
        print_success("Conexão estabelecida com sucesso!")
        
        # Testa query simples
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print_success(f"PostgreSQL Version: {db_version[0]}\n")
        
        # Testa tabelas existentes
        print_info("Verificando tabelas existentes...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print_success(f"Tabelas encontradas: {len(tables)}")
            for table in tables:
                print(f"  - {table[0]}")
        else:
            print_info("Nenhuma tabela encontrada (banco vazio)")
        
        # Testa funções existentes
        print(f"\n{Colors.BLUE}Verificando funções PostgreSQL...{Colors.END}")
        cursor.execute("""
            SELECT proname, pronargs 
            FROM pg_proc 
            WHERE proname LIKE 'fn_%'
            ORDER BY proname;
        """)
        functions = cursor.fetchall()
        
        if functions:
            print_success(f"Funções encontradas: {len(functions)}")
            for func in functions:
                print(f"  - {func[0]} ({func[1]} parâmetros)")
        else:
            print_info("Nenhuma função fn_* encontrada")
        
        # Informações de conexão
        print(f"\n{Colors.BLUE}Informações da Conexão:{Colors.END}")
        cursor.execute("SELECT current_database(), current_user, inet_server_addr(), inet_server_port();")
        conn_info = cursor.fetchone()
        print(f"  Database: {conn_info[0]}")
        print(f"  User: {conn_info[1]}")
        print(f"  Server: {conn_info[2]}:{conn_info[3]}")
        
        cursor.close()
        conn.close()
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*70}")
        print(f"  TESTE CONCLUÍDO COM SUCESSO! ✓")
        print(f"{'='*70}{Colors.END}\n")
        
        return True
        
    except OperationalError as e:
        print_error(f"Erro de conexão: {e}")
        print_info("\nPossíveis causas:")
        print("  1. Credenciais incorretas")
        print("  2. Banco de dados não acessível (firewall/security group)")
        print("  3. Host ou porta incorretos")
        print("  4. Banco de dados não existe")
        return False
        
    except Exception as e:
        print_error(f"Erro inesperado: {e}")
        return False

def main():
    """Função principal"""
    print_header()
    
    # Carrega configurações
    config = load_config()
    if not config:
        sys.exit(1)
    
    # Testa conexão
    success = test_connection(config)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
