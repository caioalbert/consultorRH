"""
Busca todas as tabelas no banco do FitBank
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
print("TODAS AS TABELAS NO BANCO DE DADOS")
print("=" * 80)

cursor.execute("""
    SELECT schemaname, tablename 
    FROM pg_tables 
    WHERE schemaname = 'public'
    ORDER BY tablename
""")

tables = cursor.fetchall()
print(f"\nTotal de tabelas: {len(tables)}\n")

for schema, table in tables:
    try:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"{table:<45} {count:>10} registros")
    except Exception as e:
        print(f"{table:<45} Erro")

cursor.close()
conn.close()
