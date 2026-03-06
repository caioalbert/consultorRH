#!/usr/bin/env python3
"""Script para popular o banco de dados com dados iniciais"""

from database import init_db, import_csv_to_db
import os

print("🔧 Inicializando banco de dados...")
init_db()

print("📊 Importando dados iniciais...")

# Importa CSVs para o banco
tables = ['colaboradores', 'ferias', 'exames', 'esocial']

for table in tables:
    csv_file = f'data/{table}.csv'
    if os.path.exists(csv_file):
        count = import_csv_to_db(csv_file, table)
        print(f"✓ {table}: {count} registros importados")
    else:
        print(f"⚠ {csv_file} não encontrado")

print("\n✅ Banco de dados populado com sucesso!")
print("🚀 Execute: streamlit run app.py")
