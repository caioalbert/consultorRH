"""
Serviços de negócio para acesso aos dados
Abstração dos repositórios para uso simplificado
"""
from typing import List, Optional, Dict, Any
import pandas as pd
from datetime import datetime

from .connection import get_connection
from .repositories import ProdutoRepository, AplicacaoRepository, GMUDRepository
from .models import Produto, Aplicacao, GMUD


class DataService:
    """Serviço principal para acesso aos dados"""
    
    def __init__(self):
        """Inicializa o serviço de dados"""
        self.db = get_connection()
        self.produtos = ProdutoRepository(self.db)
        self.aplicacoes = AplicacaoRepository(self.db)
        self.gmuds = GMUDRepository(self.db)
    
    def test_connection(self) -> bool:
        """
        Testa conexão com banco
        
        Returns:
            True se conectado
        """
        return self.db.test_connection()
    
    def close(self):
        """Fecha conexão"""
        self.db.close()
    
    # === Métodos de Produtos ===
    
    def get_produtos(self) -> List[Produto]:
        """Retorna todos os produtos"""
        return self.produtos.get_all()
    
    def get_produto_by_nome(self, nome: str) -> Optional[Produto]:
        """Busca produto por nome"""
        return self.produtos.get_by_nome(nome)
    
    def create_produto(self, nome: str, descricao: str = None) -> Produto:
        """Cria novo produto"""
        produto = Produto(nome=nome, descricao=descricao)
        return self.produtos.create(produto)
    
    def get_or_create_produto(self, nome: str, descricao: str = None) -> Produto:
        """Busca ou cria produto"""
        return self.produtos.get_or_create(nome, descricao)
    
    # === Métodos de Aplicações ===
    
    def get_aplicacoes(self, filters: Dict[str, Any] = None) -> List[Aplicacao]:
        """Retorna aplicações com filtros opcionais"""
        return self.aplicacoes.get_all(filters)
    
    def get_aplicacoes_df(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Retorna aplicações como DataFrame
        
        Args:
            filters: Filtros opcionais
            
        Returns:
            DataFrame com aplicações
        """
        aplicacoes = self.get_aplicacoes(filters)
        if not aplicacoes:
            return pd.DataFrame()
        
        data = [app.to_dict() for app in aplicacoes]
        df = pd.DataFrame(data)
        
        # Renomeia colunas para padrão do sistema
        rename_map = {
            'nome_aplicacao': 'Nome_Aplicacao',
            'produto_nome': 'Produto',
            'ambiente': 'Ambiente',
            'tipo_aplicacao': 'Tipo_Aplicacao',
            'framework': 'Framework',
            'ferramenta_versionamento': 'Ferramenta_Versionamento',
            'tipo_pipeline': 'Tipo_Pipeline',
            'versao': 'Versao',
            'hospedagem': 'Hospedagem',
            'sbom': 'SBOM',
            'scan_imagens': 'Scan_Imagens',
            'secret_manager': 'Secret_Manager',
            'sast_sonarqube': 'SAST_SonarCube',
            'data_ultima_revisao': 'Data_Ultima_Revisao',
            'data_criacao': 'Data_Criacao'
        }
        
        df = df.rename(columns=rename_map)
        
        # Converte booleanos para Sim/Não
        bool_columns = ['SBOM', 'Scan_Imagens', 'Secret_Manager', 'SAST_SonarCube']
        for col in bool_columns:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: 'Sim' if x else 'Não')
        
        return df
    
    def create_aplicacao(self, aplicacao: Aplicacao) -> Aplicacao:
        """Cria nova aplicação"""
        return self.aplicacoes.create(aplicacao)
    
    def update_aplicacao(self, aplicacao: Aplicacao) -> Aplicacao:
        """Atualiza aplicação"""
        return self.aplicacoes.update(aplicacao)
    
    def delete_aplicacao(self, aplicacao_id: int) -> bool:
        """Deleta aplicação"""
        return self.aplicacoes.delete(aplicacao_id)
    
    def get_aplicacao_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas das aplicações"""
        return self.aplicacoes.get_stats()
    
    def search_aplicacoes(self, term: str) -> List[Aplicacao]:
        """Busca aplicações por termo"""
        return self.aplicacoes.search(term)
    
    # === Métodos de GMUDs ===
    
    def get_gmuds(self, filters: Dict[str, Any] = None) -> List[GMUD]:
        """Retorna GMUDs com filtros opcionais"""
        return self.gmuds.get_all(filters)
    
    def get_gmuds_df(self, filters: Dict[str, Any] = None) -> pd.DataFrame:
        """
        Retorna GMUDs como DataFrame
        
        Args:
            filters: Filtros opcionais
            
        Returns:
            DataFrame com GMUDs
        """
        gmuds = self.get_gmuds(filters)
        if not gmuds:
            return pd.DataFrame()
        
        data = [g.to_dict() for g in gmuds]
        df = pd.DataFrame(data)
        
        # Renomeia colunas para padrão do sistema
        rename_map = {
            'id_item': 'ID_Item',
            'data_hora_prevista': 'Data_Prevista',
            'responsavel_executor': 'Responsavel',
            'tempo_estimado': 'Tempo_Estimado',
            'solicitante_area': 'Solicitante',
            'nome_aplicacao': 'Nome_Aplicacao',
            'ambiente': 'Ambiente',
            'hostname_namespace': 'Hostname',
            'local_implantacao': 'Local_Implantacao',
            'build_release': 'Build_Release',
            'configuracoes_alteradas': 'Configuracoes_Alteradas',
            'tempo_realizado': 'Tempo_Realizado',
            'ocorrencias': 'Ocorrencias',
            'solucoes_atribuidas': 'Solucoes_Atribuidas',
            'validacoes_realizadas': 'Validacoes_Realizadas',
            'risco_operacao': 'Risco_Operacao',
            'impacto': 'Impacto',
            'rca': 'RCA',
            'controle': 'Controle'
        }
        
        df = df.rename(columns=rename_map)
        
        return df
    
    def create_gmud(self, gmud: GMUD) -> GMUD:
        """Cria nova GMUD"""
        return self.gmuds.create(gmud)
    
    def update_gmud(self, gmud: GMUD) -> GMUD:
        """Atualiza GMUD"""
        return self.gmuds.update(gmud)
    
    def delete_gmud(self, gmud_id: int) -> bool:
        """Deleta GMUD"""
        return self.gmuds.delete(gmud_id)
    
    def get_gmud_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas das GMUDs"""
        return self.gmuds.get_stats()
    
    # === Métodos Utilitários ===
    
    def bulk_create_aplicacoes(self, aplicacoes: List[Aplicacao]) -> int:
        """
        Cria múltiplas aplicações em lote
        
        Args:
            aplicacoes: Lista de aplicações
            
        Returns:
            Quantidade de aplicações criadas
        """
        count = 0
        with self.db.transaction():
            for aplicacao in aplicacoes:
                try:
                    self.aplicacoes.create(aplicacao)
                    count += 1
                except Exception as e:
                    print(f"Erro ao criar aplicação {aplicacao.nome_aplicacao}: {e}")
        
        return count
    
    def bulk_create_gmuds(self, gmuds: List[GMUD]) -> int:
        """
        Cria múltiplas GMUDs em lote
        
        Args:
            gmuds: Lista de GMUDs
            
        Returns:
            Quantidade de GMUDs criadas
        """
        count = 0
        with self.db.transaction():
            for gmud in gmuds:
                try:
                    self.gmuds.create(gmud)
                    count += 1
                except Exception as e:
                    print(f"Erro ao criar GMUD {gmud.id_item}: {e}")
        
        return count


# Função helper para facilitar acesso
_service_instance = None

def get_data_service() -> DataService:
    """
    Retorna instância singleton do serviço de dados
    
    Returns:
        DataService instance
    """
    global _service_instance
    if _service_instance is None:
        _service_instance = DataService()
    return _service_instance
