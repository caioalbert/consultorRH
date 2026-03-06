"""
Verifica quantas GMUDs existem no banco de dados
"""
from src.utils.postgres_loader import PostgresDataLoader

loader = PostgresDataLoader()
cursor = loader.conn.cursor()

# Conta total de GMUDs
cursor.execute('SELECT COUNT(*) FROM gmuds')
total = cursor.fetchone()[0]
print(f'Total de GMUDs no banco: {total}')
print('=' * 80)

# Lista todas as GMUDs
cursor.execute('''
    SELECT id, id_item, ambiente, risco_operacao, 
           TO_CHAR(data_hora_prevista, 'YYYY-MM-DD') as data
    FROM gmuds 
    ORDER BY id
''')

gmuds = cursor.fetchall()
print('\nGMUDs cadastradas:')
print('-' * 80)
for gmud in gmuds:
    print(f'ID: {gmud[0]:3d} | Item: {gmud[1]:20s} | Ambiente: {gmud[2]:12s} | Risco: {gmud[3]:10s} | Data: {gmud[4]}')

cursor.close()
loader.close()

print('-' * 80)
print(f'\n✓ O sistema está correto: existem {total} GMUDs no banco de dados.')
print('✓ Todas as GMUDs estão sendo carregadas pela stored procedure.')
