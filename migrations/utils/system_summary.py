"""
Resumo completo do sistema DevOps Hub
"""
from src.utils.postgres_loader import PostgresDataLoader

print("=" * 100)
print(" " * 30 + "DEVOPS HUB - RESUMO DO SISTEMA")
print("=" * 100)

loader = PostgresDataLoader()

# Dados de Aplicações
print("\n📦 INVENTÁRIO DE APLICAÇÕES")
print("-" * 100)
df_apps = loader.load_aplicacoes()
print(f"✓ {len(df_apps)} aplicações carregadas do PostgreSQL")
print(f"  Tabela: aplicacoes")
print(f"  Stored Procedure: fn_listar_aplicacoes()")
print(f"  Produtos: {df_apps['Produto'].nunique()} ({', '.join(df_apps['Produto'].unique())})")
print(f"  Ambientes: {', '.join(df_apps['Ambiente'].unique())}")

# Dados de GMUDs
print("\n📋 GMUDs (GERENCIAMENTO DE MUDANÇAS)")
print("-" * 100)
df_gmuds = loader.load_gmuds()
print(f"✓ {len(df_gmuds)} GMUDs carregadas do PostgreSQL")
print(f"  Tabela: gmud_fitbank")
print(f"  Stored Procedure: fn_listar_gmuds()")
if not df_gmuds.empty:
    print(f"  Ambientes: {', '.join(df_gmuds['Ambiente'].unique())}")
    print(f"  Distribuição por risco:")
    for risco in df_gmuds['Risco_Operacao'].unique():
        count = len(df_gmuds[df_gmuds['Risco_Operacao'] == risco])
        print(f"    - {risco}: {count}")

# Estatísticas
print("\n📊 ESTATÍSTICAS (VIA STORED PROCEDURES)")
print("-" * 100)
stats = loader.get_summary_stats()
print(f"Aplicações:")
print(f"  - Total: {stats.get('total_aplicacoes')}")
print(f"  - Produtos únicos: {stats.get('produtos_unicos')}")
print(f"  - Ambientes únicos: {stats.get('ambientes_unicos')}")
print(f"  - Frameworks únicos: {stats.get('frameworks_unicos')}")
print(f"\nSegurança & DevSecOps:")
print(f"  - SBOM: {stats.get('percentual_sbom', 0):.1f}%")
print(f"  - Scan de Imagens: {stats.get('percentual_scan', 0):.1f}%")
print(f"  - Secret Manager: {stats.get('percentual_secret_manager', 0):.1f}%")
print(f"  - SAST (SonarQube): {stats.get('percentual_sast', 0):.1f}%")
print(f"\nGMUDs:")
print(f"  - Total: {stats.get('total_gmuds')}")
print(f"  - Risco Alto: {stats.get('risco_alto')}")
print(f"  - Risco Médio: {stats.get('risco_medio')}")
print(f"  - Risco Baixo: {stats.get('risco_baixo')}")

# Stored Procedures disponíveis
print("\n🔧 STORED PROCEDURES DISPONÍVEIS")
print("-" * 100)
cursor = loader.conn.cursor()
cursor.execute("""
    SELECT routine_name 
    FROM information_schema.routines 
    WHERE routine_schema = 'public' 
    AND routine_name LIKE 'fn_%'
    ORDER BY routine_name
""")
functions = cursor.fetchall()
print("Produtos:")
for func in [f[0] for f in functions if 'produto' in f[0]]:
    print(f"  - {func}")
print("\nAplicações:")
for func in [f[0] for f in functions if 'aplicacao' in f[0] or 'aplicacoes' in f[0]]:
    print(f"  - {func}")
print("\nGMUDs:")
for func in [f[0] for f in functions if 'gmud' in f[0]]:
    print(f"  - {func}")
print("\nEstatísticas:")
for func in [f[0] for f in functions if 'stats' in f[0]]:
    print(f"  - {func}")

cursor.close()
loader.close()

print("\n" + "=" * 100)
print("✓ SISTEMA 100% INTEGRADO COM POSTGRESQL VIA STORED PROCEDURES")
print("=" * 100)
