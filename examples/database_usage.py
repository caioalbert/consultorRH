"""
Exemplo de uso da camada de acesso a dados PostgreSQL
Demonstra as principais funcionalidades
"""
import os
from datetime import datetime
from src.database import get_data_service, Aplicacao, GMUD

# Configure as variáveis de ambiente antes
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5432'
os.environ['DB_NAME'] = 'devops_hub'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'sua_senha'


def exemplo_produtos():
    """Exemplo: Gerenciar produtos"""
    print("\n=== EXEMPLO: PRODUTOS ===")
    
    service = get_data_service()
    
    # Listar todos os produtos
    produtos = service.get_produtos()
    print(f"Total de produtos: {len(produtos)}")
    for p in produtos[:5]:
        print(f"  - {p.nome}")
    
    # Buscar ou criar produto
    produto = service.get_or_create_produto("NOVO_PRODUTO", "Descrição do produto")
    print(f"\nProduto: {produto.nome} (ID: {produto.id})")


def exemplo_aplicacoes():
    """Exemplo: Gerenciar aplicações"""
    print("\n=== EXEMPLO: APLICAÇÕES ===")
    
    service = get_data_service()
    
    # Listar todas
    apps = service.get_aplicacoes()
    print(f"Total de aplicações: {len(apps)}")
    
    # Filtrar por ambiente
    apps_prod = service.get_aplicacoes({'ambiente': 'Produção'})
    print(f"Aplicações em Produção: {len(apps_prod)}")
    
    # Obter como DataFrame
    df = service.get_aplicacoes_df({'ambiente': 'Produção'})
    print(f"\nDataFrame shape: {df.shape}")
    print(df.head())
    
    # Estatísticas
    stats = service.get_aplicacao_stats()
    print(f"\nEstatísticas:")
    print(f"  Total: {stats.get('total_aplicacoes')}")
    print(f"  Com SBOM: {stats.get('com_sbom')}")
    print(f"  Com Scan: {stats.get('com_scan')}")
    
    # Buscar por termo
    resultados = service.search_aplicacoes("topup")
    print(f"\nBusca por 'topup': {len(resultados)} resultados")


def exemplo_criar_aplicacao():
    """Exemplo: Criar nova aplicação"""
    print("\n=== EXEMPLO: CRIAR APLICAÇÃO ===")
    
    service = get_data_service()
    
    # Buscar ou criar produto
    produto = service.get_or_create_produto("TESTE")
    
    # Criar aplicação
    nova_app = Aplicacao(
        nome_aplicacao="teste-api",
        produto_id=produto.id,
        ambiente="Desenvolvimento",
        tipo_aplicacao="API",
        framework="Python",
        ferramenta_versionamento="Git",
        tipo_pipeline="YAML",
        versao="1.0.0",
        hospedagem="AWS",
        sbom=True,
        scan_imagens=True,
        secret_manager=True,
        sast_sonarqube=False,
        data_criacao=datetime.now().date()
    )
    
    try:
        app_criada = service.create_aplicacao(nova_app)
        print(f"Aplicação criada: {app_criada.nome_aplicacao} (ID: {app_criada.id})")
    except Exception as e:
        print(f"Erro ao criar aplicação: {e}")


def exemplo_gmuds():
    """Exemplo: Gerenciar GMUDs"""
    print("\n=== EXEMPLO: GMUDS ===")
    
    service = get_data_service()
    
    # Listar todas
    gmuds = service.get_gmuds()
    print(f"Total de GMUDs: {len(gmuds)}")
    
    # Filtrar por ambiente
    gmuds_prod = service.get_gmuds({'ambiente': 'Produção'})
    print(f"GMUDs em Produção: {len(gmuds_prod)}")
    
    # Filtrar por risco
    gmuds_alto_risco = service.get_gmuds({'risco_operacao': 'Alto'})
    print(f"GMUDs de alto risco: {len(gmuds_alto_risco)}")
    
    # Obter como DataFrame
    df = service.get_gmuds_df()
    print(f"\nDataFrame shape: {df.shape}")
    print(df.head())
    
    # Estatísticas
    stats = service.get_gmud_stats()
    print(f"\nEstatísticas:")
    print(f"  Total: {stats.get('total_gmuds')}")
    print(f"  Risco Alto: {stats.get('risco_alto')}")
    print(f"  Risco Médio: {stats.get('risco_medio')}")


def exemplo_transacao():
    """Exemplo: Usar transações"""
    print("\n=== EXEMPLO: TRANSAÇÃO ===")
    
    service = get_data_service()
    
    try:
        with service.db.transaction():
            # Criar produto
            produto = service.get_or_create_produto("TRANSACAO_TESTE")
            
            # Criar aplicações
            for i in range(3):
                app = Aplicacao(
                    nome_aplicacao=f"app-transacao-{i}",
                    produto_id=produto.id,
                    ambiente="Teste"
                )
                service.create_aplicacao(app)
            
            print("Transação concluída com sucesso!")
    except Exception as e:
        print(f"Erro na transação: {e}")
        print("Transação revertida automaticamente")


def exemplo_repositorio_direto():
    """Exemplo: Usar repositório diretamente"""
    print("\n=== EXEMPLO: REPOSITÓRIO DIRETO ===")
    
    from src.database import get_connection, AplicacaoRepository
    
    db = get_connection()
    repo = AplicacaoRepository(db)
    
    # Query personalizada
    apps_com_seguranca = [
        app for app in repo.get_all()
        if app.sbom and app.scan_imagens and app.secret_manager
    ]
    
    print(f"Aplicações com segurança completa: {len(apps_com_seguranca)}")
    
    for app in apps_com_seguranca[:5]:
        print(f"  - {app.nome_aplicacao} ({app.ambiente})")


def main():
    """Executa todos os exemplos"""
    print("=" * 60)
    print("  EXEMPLOS DE USO - CAMADA DE DADOS POSTGRESQL")
    print("=" * 60)
    
    service = get_data_service()
    
    # Testar conexão
    if not service.test_connection():
        print("\n❌ Erro: Não foi possível conectar ao banco de dados")
        print("   Verifique as configurações no código ou arquivo .env")
        return
    
    print("✅ Conectado ao banco de dados com sucesso!\n")
    
    # Executar exemplos
    try:
        exemplo_produtos()
        exemplo_aplicacoes()
        exemplo_gmuds()
        exemplo_criar_aplicacao()
        exemplo_transacao()
        exemplo_repositorio_direto()
    except Exception as e:
        print(f"\n❌ Erro ao executar exemplo: {e}")
    finally:
        service.close()
        print("\n✅ Conexão fechada")
    
    print("\n" + "=" * 60)
    print("  FIM DOS EXEMPLOS")
    print("=" * 60)


if __name__ == "__main__":
    main()
