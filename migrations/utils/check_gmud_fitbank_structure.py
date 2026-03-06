"""
Verifica estrutura da tabela gmud_fitbank
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

print("Estrutura da tabela gmud_fitbank:")
print("=" * 60)
cursor.execute("""
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns 
    WHERE table_name = 'gmud_fitbank' 
    ORDER BY ordinal_position
""")

columns = cursor.fetchall()
for col in columns:
    print(f"{col[0]:<30} {col[1]:<20} NULL: {col[2]}")

print("\n" + "=" * 60)
print(f"Total de colunas: {len(columns)}")

# Mostra alguns dados de exemplo
cursor.execute("SELECT * FROM gmud_fitbank LIMIT 3")
print("\nExemplo de dados:")
rows = cursor.fetchall()
if rows:
    print(f"Primeira GMUD: ID={rows[0][0]}")

cursor.close()
conn.close()
