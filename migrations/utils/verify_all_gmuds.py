"""
Verificação detalhada de todas as GMUDs no banco
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

print("=" * 100)
print("VERIFICAÇÃO COMPLETA DE GMUDs NO BANCO DE DADOS")
print("=" * 100)

# Conta total
cursor.execute('SELECT COUNT(*) FROM gmuds')
total = cursor.fetchone()[0]
print(f"\nTotal de GMUDs na tabela: {total}")

# Lista TODAS as GMUDs com mais detalhes
cursor.execute('''
    SELECT 
        g.id,
        g.id_item,
        g.ambiente,
        g.risco_operacao,
        g.responsavel_executor,
        TO_CHAR(g.data_hora_prevista, 'YYYY-MM-DD HH24:MI') as data,
        g.nome_aplicacao
    FROM gmuds g
    ORDER BY g.id
''')

gmuds = cursor.fetchall()

print(f"\nListagem de TODAS as {len(gmuds)} GMUDs:")
print("-" * 100)
print(f"{'ID':<5} {'Item':<15} {'Ambiente':<15} {'Risco':<12} {'Responsável':<25} {'Data':<17} {'Aplicação'}")
print("-" * 100)

for gmud in gmuds:
    app = gmud[6] if gmud[6] else 'N/A'
    print(f"{gmud[0]:<5} {gmud[1]:<15} {gmud[2]:<15} {gmud[3]:<12} {gmud[4]:<25} {gmud[5]:<17} {app}")

print("-" * 100)
print(f"\n✓ Total confirmado: {len(gmuds)} GMUDs no banco de dados")

# Verifica se há GMUDs em outras tabelas ou schemas
cursor.execute('''
    SELECT schemaname, tablename 
    FROM pg_tables 
    WHERE tablename LIKE '%gmud%'
''')
tables = cursor.fetchall()
print(f"\nTabelas relacionadas a GMUD encontradas: {tables}")

cursor.close()
conn.close()
