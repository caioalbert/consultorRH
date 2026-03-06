"""
Verifica todas as tabelas relacionadas a aplicações/inventário
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

cursor = conn.cursor()

print("=" * 80)
print("VERIFICAÇÃO DE TABELAS DE APLICAÇÕES/INVENTÁRIO")
print("=" * 80)

# Busca tabelas relacionadas a aplicações
cursor.execute("""
    SELECT schemaname, tablename 
    FROM pg_tables 
    WHERE schemaname = 'public' 
    AND (tablename LIKE '%aplicac%' OR tablename LIKE '%inventario%' OR tablename LIKE '%app%')
    ORDER BY tablename
""")

tables = cursor.fetchall()
print(f"\nTabelas encontradas: {len(tables)}")
print("-" * 80)

total_geral = 0
for schema, table in tables:
    try:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        total_geral += count
        print(f"{table:<40} {count:>10} registros")
        
        if count > 0 and count <= 5:
            # Mostra exemplo de dados para tabelas pequenas
            cursor.execute(f'SELECT * FROM {table} LIMIT 1')
            print(f"  (Exemplo: {cursor.fetchone()[0] if cursor.rowcount > 0 else 'N/A'})")
    except Exception as e:
        print(f"{table:<40} Erro: {e}")

print("-" * 80)
print(f"TOTAL GERAL: {total_geral} registros")
print("=" * 80)

cursor.close()
conn.close()
