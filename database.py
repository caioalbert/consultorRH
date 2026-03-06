import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import os
from urllib.parse import urlparse

def get_db_connection():
    """Conecta ao PostgreSQL usando DATABASE_URL ou variáveis locais"""
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Parse URL do PostgreSQL (formato Heroku/Vercel)
        url = urlparse(database_url)
        return psycopg2.connect(
            host=url.hostname,
            port=url.port,
            user=url.username,
            password=url.password,
            database=url.path[1:]
        )
    else:
        # Desenvolvimento local
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'postgres'),
            database=os.getenv('DB_NAME', 'consultorrh')
        )

def init_db():
    """Inicializa o banco de dados"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabela colaboradores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS colaboradores (
            id SERIAL PRIMARY KEY,
            nome TEXT,
            cpf TEXT UNIQUE,
            cargo TEXT,
            filial TEXT,
            setor TEXT,
            data_admissao TEXT,
            status TEXT,
            risco TEXT
        )
    """)
    
    # Tabela ferias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ferias (
            id SERIAL PRIMARY KEY,
            nome TEXT,
            filial TEXT,
            periodo_aquisitivo TEXT,
            dias_devidos INTEGER,
            vencimento TEXT,
            em_dobro TEXT,
            passivo TEXT,
            status TEXT
        )
    """)
    
    # Tabela exames
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exames (
            id SERIAL PRIMARY KEY,
            nome TEXT,
            filial TEXT,
            tipo_exame TEXT,
            ultimo_exame TEXT,
            vencimento TEXT,
            dias_atraso INTEGER,
            passivo TEXT,
            status TEXT
        )
    """)
    
    # Tabela esocial
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS esocial (
            id SERIAL PRIMARY KEY,
            evento TEXT,
            descricao TEXT,
            pendencias INTEGER,
            passivo TEXT,
            criticidade TEXT
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def load_from_db(table):
    """Carrega dados do banco"""
    conn = get_db_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

def save_to_db(df, table):
    """Salva dados no banco"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Limpa tabela antes de inserir
    cursor.execute(f"DELETE FROM {table}")
    
    # Insere novos dados
    columns = df.columns.tolist()
    for _, row in df.iterrows():
        placeholders = ','.join(['%s'] * len(columns))
        query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
        cursor.execute(query, tuple(row))
    
    conn.commit()
    cursor.close()
    conn.close()

def import_csv_to_db(csv_path, table):
    """Importa CSV para o banco"""
    df = pd.read_csv(csv_path)
    save_to_db(df, table)
    return len(df)
