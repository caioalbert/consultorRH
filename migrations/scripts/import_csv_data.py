"""
Script para importar dados dos CSVs para o PostgreSQL
Deve ser executado após aplicar as migrations 001 e 002
"""
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.services import get_data_service
from src.database.models import Aplicacao, GMUD


def parse_bool(value):
    """Converte valor para booleano"""
    if pd.isna(value):
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ['sim', 'yes', 'true', '1']
    return False


def parse_date(value):
    """Converte valor para data"""
    if pd.isna(value):
        return None
    try:
        return pd.to_datetime(value).date()
    except:
        return None


def parse_datetime(value):
    """Converte valor para datetime"""
    if pd.isna(value):
        return None
    try:
        return pd.to_datetime(value, format='%d/%m/%y %H:%M')
    except:
        try:
            return pd.to_datetime(value)
        except:
            return None


def import_aplicacoes(csv_path: str, service: any) -> int:
    """
    Importa aplicações do CSV
    
    Args:
        csv_path: Caminho do arquivo CSV
        service: Instância do DataService
        
    Returns:
        Quantidade de aplicações importadas
    """
    print(f"\n📥 Importando aplicações de {csv_path}...")
    
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    print(f"   Encontradas {len(df)} linhas no CSV")
    
    aplicacoes = []
    produtos_cache = {}
    
    for idx, row in df.iterrows():
        # Busca ou cria produto
        produto_nome = row.get('Produto', 'Não Especificado')
        
        if produto_nome not in produtos_cache:
            produto = service.get_or_create_produto(produto_nome)
            produtos_cache[produto_nome] = produto.id
        
        produto_id = produtos_cache[produto_nome]
        
        # Cria objeto Aplicacao
        aplicacao = Aplicacao(
            nome_aplicacao=row.get('Nome_Aplicacao', ''),
            produto_id=produto_id,
            ambiente=row.get('Ambiente', 'Não Especificado'),
            tipo_aplicacao=row.get('Tipo_Aplicacao'),
            framework=row.get('Framework'),
            ferramenta_versionamento=row.get('Ferramenta_Versionamento'),
            tipo_pipeline=row.get('Tipo_Pipeline'),
            versao=row.get('Versao'),
            hospedagem=row.get('Hospedagem'),
            sbom=parse_bool(row.get('SBOM')),
            scan_imagens=parse_bool(row.get('Scan_Imagens')),
            secret_manager=parse_bool(row.get('Secret_Manager')),
            sast_sonarqube=parse_bool(row.get('SAST_SonarCube')),
            data_ultima_revisao=parse_date(row.get('Data_Ultima_Revisao')),
            data_criacao=parse_date(row.get('Data_Criacao'))
        )
        
        aplicacoes.append(aplicacao)
    
    # Importa em lote
    count = service.bulk_create_aplicacoes(aplicacoes)
    print(f"   ✅ {count} aplicações importadas com sucesso!")
    
    return count


def import_gmuds(csv_path: str, service: any) -> int:
    """
    Importa GMUDs do CSV
    
    Args:
        csv_path: Caminho do arquivo CSV
        service: Instância do DataService
        
    Returns:
        Quantidade de GMUDs importadas
    """
    print(f"\n📥 Importando GMUDs de {csv_path}...")
    
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    print(f"   Encontradas {len(df)} linhas no CSV")
    
    gmuds = []
    
    for idx, row in df.iterrows():
        # Cria objeto GMUD
        gmud = GMUD(
            id_item=str(row.get('ID do Item', '')),
            data_hora_prevista=parse_datetime(row.get('Data/hora Prevista')),
            responsavel_executor=row.get('Responsável / Executor'),
            tempo_estimado=row.get('Tempo Estimado'),
            solicitante_area=row.get('Solicitante / área de atuação'),
            nome_aplicacao=row.get('Nome da Aplicação'),
            ambiente=row.get('Ambiente'),
            hostname_namespace=row.get('hostname/namespace'),
            local_implantacao=row.get('Local de Implantação'),
            build_release=row.get('Build/Release'),
            configuracoes_alteradas=row.get('Configurações alteradas'),
            tempo_realizado=row.get('Tempo Realizado'),
            ocorrencias=row.get('Ocorrências'),
            solucoes_atribuidas=row.get('Soluções Atribuídas'),
            validacoes_realizadas=row.get('Validações Realizadas'),
            risco_operacao=row.get('Risco a Operação'),
            impacto=row.get('Impacto'),
            rca=row.get('RCA'),
            controle=row.get('Controle')
        )
        
        gmuds.append(gmud)
    
    # Importa em lote
    count = service.bulk_create_gmuds(gmuds)
    print(f"   ✅ {count} GMUDs importadas com sucesso!")
    
    return count

def main():
    """Função principal de importação"""
    print("=" * 60)
    print("  IMPORTADOR DE DADOS CSV PARA POSTGRESQL")
    print("=" * 60)
    
    # Caminhos dos arquivos
    base_path = Path(__file__).parent.parent.parent / "data"
    aplicacoes_csv = base_path / "inventario_aplicacoes.csv"
    gmuds_csv = base_path / "gmud_dados.csv"
    
    # Inicializa serviço
    print("\n🔌 Conectando ao banco de dados...")
    service = get_data_service()
    
    if not service.test_connection():
        print("❌ Erro: Não foi possível conectar ao banco de dados")
        print("   Verifique as variáveis de ambiente:")
        print("   - DB_HOST")
        print("   - DB_PORT")
        print("   - DB_NAME")
        print("   - DB_USER")
        print("   - DB_PASSWORD")
        return
    
    print("   ✅ Conectado com sucesso!")
    
    # Importar aplicações
    if aplicacoes_csv.exists():
        try:
            aplicacoes_count = import_aplicacoes(str(aplicacoes_csv), service)
        except Exception as e:
            print(f"   ❌ Erro ao importar aplicações: {e}")
            aplicacoes_count = 0
    else:
        print(f"\n⚠️  Arquivo não encontrado: {aplicacoes_csv}")
        aplicacoes_count = 0
    
    # Importar GMUDs
    if gmuds_csv.exists():
        try:
            gmuds_count = import_gmuds(str(gmuds_csv), service)
        except Exception as e:
            print(f"   ❌ Erro ao importar GMUDs: {e}")
            gmuds_count = 0
    else:
        print(f"\n⚠️  Arquivo não encontrado: {gmuds_csv}")
        gmuds_count = 0
    
    # Resumo
    print("\n" + "=" * 60)
    print("  RESUMO DA IMPORTAÇÃO")
    print("=" * 60)
    print(f"  📊 Aplicações importadas: {aplicacoes_count}")
    print(f"  📋 GMUDs importadas: {gmuds_count}")
    print(f"  ✅ Total: {aplicacoes_count + gmuds_count} registros")
    print("=" * 60)
    
    # Fecha conexão
    service.close()
    print("\n✅ Importação concluída!")

if __name__ == "__main__":
    main()
