"""
Script de teste para validar o PostgresDataLoader com stored procedures
"""
from src.utils.postgres_loader import PostgresDataLoader

print("=== TESTE DO SISTEMA COM STORED PROCEDURES ===\n")

try:
    # Conecta ao banco
    loader = PostgresDataLoader()
    print("✓ Conexão estabelecida com sucesso")
    
    # Carrega aplicações
    print("\n1. Testando carregamento de aplicações...")
    df_apps = loader.load_aplicacoes()
    print(f"   ✓ {len(df_apps)} aplicações carregadas")
    if not df_apps.empty:
        print(f"   Colunas: {list(df_apps.columns)[:5]}...")
    
    # Carrega GMUDs
    print("\n2. Testando carregamento de GMUDs...")
    df_gmuds = loader.load_gmuds()
    print(f"   ✓ {len(df_gmuds)} GMUDs carregadas")
    
    # Carrega produtos
    print("\n3. Testando carregamento de produtos...")
    df_produtos = loader.load_produtos()
    print(f"   ✓ {len(df_produtos)} produtos carregados")
    
    # Obtém estatísticas
    print("\n4. Testando estatísticas usando stored procedures...")
    stats = loader.get_summary_stats()
    print(f"   ✓ Estatísticas obtidas:")
    print(f"      - Total de aplicações: {stats.get('total_aplicacoes', 0)}")
    print(f"      - Produtos únicos: {stats.get('produtos_unicos', 0)}")
    print(f"      - Ambientes únicos: {stats.get('ambientes_unicos', 0)}")
    print(f"      - Total de GMUDs: {stats.get('total_gmuds', 0)}")
    print(f"      - Percentual com SBOM: {stats.get('percentual_sbom', 0):.1f}%")
    print(f"      - Percentual com Scan: {stats.get('percentual_scan', 0):.1f}%")
    
    # Fecha conexão
    loader.close()
    print("\n✓ Conexão fechada")
    
    print("\n" + "="*50)
    print("✓✓✓ TODOS OS TESTES PASSARAM COM SUCESSO! ✓✓✓")
    print("="*50)
    print("\nO sistema agora está usando stored procedures do PostgreSQL!")
    
except Exception as e:
    print(f"\n✗ Erro durante os testes: {e}")
    import traceback
    traceback.print_exc()
