from src.utils.postgres_loader import PostgresDataLoader

with PostgresDataLoader() as loader:
    df = loader.load_gmuds()
    print("Colunas do DataFrame de GMUDs:")
    print(df.columns.tolist())
    print(f"\nTotal de linhas: {len(df)}")
    if not df.empty:
        print("\nPrimeiras colunas:")
        for col in df.columns[:10]:
            print(f"  - {col}")
