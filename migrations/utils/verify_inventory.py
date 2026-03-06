"""
Confirma os dados do inventário
"""
from src.utils.postgres_loader import PostgresDataLoader

loader = PostgresDataLoader()

print("=" * 80)
print("VERIFICAÇÃO DO INVENTÁRIO DE APLICAÇÕES")
print("=" * 80)

df = loader.load_aplicacoes()
print(f"\n✓ {len(df)} aplicações carregadas do PostgreSQL")
print(f"✓ Produtos únicos: {df['Produto'].nunique()}")
print(f"✓ Ambientes: {list(df['Ambiente'].unique())}")

stats = loader.get_summary_stats()
print(f"\nEstatísticas via Stored Procedures:")
print(f"  - Total de aplicações: {stats.get('total_aplicacoes')}")
print(f"  - Produtos únicos: {stats.get('produtos_unicos')}")
print(f"  - Ambientes únicos: {stats.get('ambientes_unicos')}")
print(f"  - Frameworks únicos: {stats.get('frameworks_unicos')}")
print(f"  - Com SBOM: {stats.get('percentual_sbom', 0):.1f}%")
print(f"  - Com Scan de Imagens: {stats.get('percentual_scan', 0):.1f}%")
print(f"  - Com Secret Manager: {stats.get('percentual_secret_manager', 0):.1f}%")
print(f"  - Com SAST: {stats.get('percentual_sast', 0):.1f}%")

print("\n" + "=" * 80)
print("✓ Inventário funcionando corretamente com PostgreSQL!")
print("=" * 80)

loader.close()
