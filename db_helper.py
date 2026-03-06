"""
Script helper para operações do banco de dados
Facilita tarefas comuns de administração
"""
import sys
import argparse
from pathlib import Path

# Adiciona diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import get_data_service


def test_connection():
    """Testa conexão com o banco"""
    print("🔌 Testando conexão com PostgreSQL...")
    service = get_data_service()
    
    if service.test_connection():
        print("✅ Conexão estabelecida com sucesso!")
        
        # Mostrar informações
        try:
            stats_app = service.get_aplicacao_stats()
            stats_gmud = service.get_gmud_stats()
            produtos = service.get_produtos()
            
            print("\n📊 Estatísticas do Banco:")
            print(f"  • Produtos: {len(produtos)}")
            print(f"  • Aplicações: {stats_app.get('total_aplicacoes', 0)}")
            print(f"  • GMUDs: {stats_gmud.get('total_gmuds', 0)}")
            print(f"  • Ambientes: {stats_app.get('total_ambientes', 0)}")
            print(f"  • Frameworks: {stats_app.get('total_frameworks', 0)}")
        except Exception as e:
            print(f"⚠️  Não foi possível obter estatísticas: {e}")
        
        service.close()
        return True
    else:
        print("❌ Falha na conexão!")
        print("\nVerifique:")
        print("  1. PostgreSQL está rodando")
        print("  2. Credenciais no arquivo .env")
        print("  3. Database 'devops_hub' existe")
        return False


def show_stats():
    """Mostra estatísticas detalhadas"""
    print("📊 Estatísticas Detalhadas\n")
    
    service = get_data_service()
    
    if not service.test_connection():
        print("❌ Não foi possível conectar ao banco")
        return
    
    try:
        # Produtos
        produtos = service.get_produtos()
        print(f"📦 PRODUTOS ({len(produtos)})")
        for p in produtos:
            print(f"  • {p.nome}")
        
        # Aplicações
        print(f"\n💻 APLICAÇÕES")
        stats_app = service.get_aplicacao_stats()
        print(f"  • Total: {stats_app.get('total_aplicacoes', 0)}")
        print(f"  • Com SBOM: {stats_app.get('com_sbom', 0)}")
        print(f"  • Com Scan de Imagens: {stats_app.get('com_scan', 0)}")
        print(f"  • Com Secret Manager: {stats_app.get('com_secret_manager', 0)}")
        print(f"  • Com SAST: {stats_app.get('com_sast', 0)}")
        
        # Por ambiente
        print(f"\n🌍 POR AMBIENTE")
        for ambiente in ['Produção', 'Sandbox', 'N/A']:
            apps = service.get_aplicacoes({'ambiente': ambiente})
            print(f"  • {ambiente}: {len(apps)}")
        
        # GMUDs
        print(f"\n📋 GMUDS")
        stats_gmud = service.get_gmud_stats()
        print(f"  • Total: {stats_gmud.get('total_gmuds', 0)}")
        print(f"  • Risco Alto: {stats_gmud.get('risco_alto', 0)}")
        print(f"  • Risco Médio: {stats_gmud.get('risco_medio', 0)}")
        print(f"  • Risco Baixo: {stats_gmud.get('risco_baixo', 0)}")
        
    except Exception as e:
        print(f"❌ Erro ao obter estatísticas: {e}")
    finally:
        service.close()


def list_apps(ambiente=None, produto=None):
    """Lista aplicações"""
    service = get_data_service()
    
    if not service.test_connection():
        print("❌ Não foi possível conectar ao banco")
        return
    
    try:
        filters = {}
        if ambiente:
            filters['ambiente'] = ambiente
        if produto:
            produto_obj = service.get_produto_by_nome(produto)
            if produto_obj:
                filters['produto_id'] = produto_obj.id
            else:
                print(f"❌ Produto '{produto}' não encontrado")
                return
        
        apps = service.get_aplicacoes(filters)
        
        title = "📱 APLICAÇÕES"
        if ambiente:
            title += f" - {ambiente}"
        if produto:
            title += f" - {produto}"
        
        print(f"\n{title} ({len(apps)})\n")
        
        for app in apps:
            produto_nome = app.produto_nome or "N/A"
            print(f"  • {app.nome_aplicacao}")
            print(f"    Produto: {produto_nome} | Ambiente: {app.ambiente}")
            print(f"    Framework: {app.framework or 'N/A'} | Hospedagem: {app.hospedagem or 'N/A'}")
            
            # Segurança
            seguranca = []
            if app.sbom:
                seguranca.append("SBOM")
            if app.scan_imagens:
                seguranca.append("Scan")
            if app.secret_manager:
                seguranca.append("Secrets")
            if app.sast_sonarqube:
                seguranca.append("SAST")
            
            if seguranca:
                print(f"    Segurança: {', '.join(seguranca)}")
            print()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        service.close()


def export_to_csv(output_dir="exports"):
    """Exporta dados para CSV"""
    import pandas as pd
    from datetime import datetime
    
    print("📤 Exportando dados para CSV...")
    
    service = get_data_service()
    
    if not service.test_connection():
        print("❌ Não foi possível conectar ao banco")
        return
    
    try:
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Exportar aplicações
        df_apps = service.get_aplicacoes_df()
        apps_file = output_path / f"aplicacoes_{timestamp}.csv"
        df_apps.to_csv(apps_file, index=False, encoding='utf-8-sig')
        print(f"  ✅ Aplicações: {apps_file}")
        
        # Exportar GMUDs
        df_gmuds = service.get_gmuds_df()
        gmuds_file = output_path / f"gmuds_{timestamp}.csv"
        df_gmuds.to_csv(gmuds_file, index=False, encoding='utf-8-sig')
        print(f"  ✅ GMUDs: {gmuds_file}")
        
        print(f"\n✅ Exportação concluída em: {output_path.absolute()}")
        
    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")
    finally:
        service.close()


def search(term):
    """Busca aplicações por termo"""
    print(f"🔍 Buscando por: '{term}'...\n")
    
    service = get_data_service()
    
    if not service.test_connection():
        print("❌ Não foi possível conectar ao banco")
        return
    
    try:
        apps = service.search_aplicacoes(term)
        
        if not apps:
            print("❌ Nenhum resultado encontrado")
            return
        
        print(f"📱 RESULTADOS ({len(apps)})\n")
        
        for app in apps:
            produto_nome = app.produto_nome or "N/A"
            print(f"  • {app.nome_aplicacao}")
            print(f"    Produto: {produto_nome} | Ambiente: {app.ambiente}")
            print()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        service.close()


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Helper para operações do banco de dados PostgreSQL',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python db_helper.py test                    # Testar conexão
  python db_helper.py stats                   # Mostrar estatísticas
  python db_helper.py list                    # Listar todas aplicações
  python db_helper.py list --ambiente Produção # Listar por ambiente
  python db_helper.py list --produto TOPUP    # Listar por produto
  python db_helper.py search api              # Buscar aplicações
  python db_helper.py export                  # Exportar para CSV
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Test
    subparsers.add_parser('test', help='Testar conexão')
    
    # Stats
    subparsers.add_parser('stats', help='Mostrar estatísticas')
    
    # List
    list_parser = subparsers.add_parser('list', help='Listar aplicações')
    list_parser.add_argument('--ambiente', help='Filtrar por ambiente')
    list_parser.add_argument('--produto', help='Filtrar por produto')
    
    # Search
    search_parser = subparsers.add_parser('search', help='Buscar aplicações')
    search_parser.add_argument('term', help='Termo de busca')
    
    # Export
    export_parser = subparsers.add_parser('export', help='Exportar para CSV')
    export_parser.add_argument('--output', default='exports', help='Diretório de saída')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print("=" * 60)
    print("  DATABASE HELPER - DevOps Hub")
    print("=" * 60 + "\n")
    
    if args.command == 'test':
        test_connection()
    elif args.command == 'stats':
        show_stats()
    elif args.command == 'list':
        list_apps(ambiente=args.ambiente, produto=args.produto)
    elif args.command == 'search':
        search(args.term)
    elif args.command == 'export':
        export_to_csv(args.output)
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
