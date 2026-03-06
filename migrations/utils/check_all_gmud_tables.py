"""
Verifica GMUDs em todas as tabelas
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
print("VERIFICAÇÃO DE TODAS AS TABELAS DE GMUD")
print("=" * 80)

tables = ['gmuds', 'gmud_fitbank', 'gmud_easycredio', 'gmud_rodobank']
total_geral = 0

for table in tables:
    try:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        total_geral += count
        print(f"\n{table}: {count} registros")
        
        if count > 0:
            cursor.execute(f'SELECT * FROM {table} LIMIT 3')
            print(f"  Primeiros registros de {table}:")
            rows = cursor.fetchall()
            for row in rows:
                print(f"    ID: {row[0]}")
    except Exception as e:
        print(f"\n{table}: Erro ao acessar - {e}")

print("\n" + "=" * 80)
print(f"TOTAL GERAL DE GMUDs: {total_geral}")
print("=" * 80)

cursor.close()
conn.close()
