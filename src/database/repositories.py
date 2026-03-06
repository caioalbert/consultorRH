"""
Repositórios para acesso aos dados do PostgreSQL
Pattern: Repository Pattern
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import psycopg2.extras

from .connection import DatabaseConnection
from .models import Produto, Aplicacao, GMUD


class BaseRepository:
    """Classe base para repositórios"""
    
    def __init__(self, db: DatabaseConnection):
        """
        Inicializa o repositório
        
        Args:
            db: Instância de DatabaseConnection
        """
        self.db = db


class ProdutoRepository(BaseRepository):
    """Repositório para operações com Produtos usando Stored Procedures"""
    
    def create(self, produto: Produto) -> Produto:
        """
        Cria um novo produto via stored procedure
        
        Args:
            produto: Instância de Produto
            
        Returns:
            Produto criado com ID
        """
        query = "SELECT * FROM fn_criar_produto(%s, %s)"
        result = self.db.execute_query(
            query,
            (produto.nome, produto.descricao),
            fetch_one=True
        )
        self.db.commit()
        return Produto.from_dict(result)
    
    def get_by_id(self, produto_id: int) -> Optional[Produto]:
        """
        Busca produto por ID via stored procedure
        
        Args:
            produto_id: ID do produto
            
        Returns:
            Produto ou None
        """
        query = "SELECT * FROM fn_buscar_produto_por_id(%s)"
        result = self.db.execute_query(query, (produto_id,), fetch_one=True)
        return Produto.from_dict(result) if result else None
    
    def get_by_nome(self, nome: str) -> Optional[Produto]:
        """
        Busca produto por nome via stored procedure
        
        Args:
            nome: Nome do produto
            
        Returns:
            Produto ou None
        """
        query = "SELECT * FROM fn_buscar_produto_por_nome(%s)"
        result = self.db.execute_query(query, (nome,), fetch_one=True)
        return Produto.from_dict(result) if result else None
    
    def get_all(self) -> List[Produto]:
        """
        Retorna todos os produtos via stored procedure
        
        Returns:
            Lista de Produtos
        """
        query = "SELECT * FROM fn_listar_produtos()"
        results = self.db.execute_query(query)
        return [Produto.from_dict(row) for row in results]
    
    def update(self, produto: Produto) -> Produto:
        """
        Atualiza um produto via stored procedure
        
        Args:
            produto: Instância de Produto com ID
            
        Returns:
            Produto atualizado
        """
        query = "SELECT * FROM fn_atualizar_produto(%s, %s, %s)"
        result = self.db.execute_query(
            query,
            (produto.id, produto.nome, produto.descricao),
            fetch_one=True
        )
        self.db.commit()
        return Produto.from_dict(result)
    
    def delete(self, produto_id: int) -> bool:
        """
        Deleta um produto via stored procedure
        
        Args:
            produto_id: ID do produto
            
        Returns:
            True se deletado com sucesso
        """
        query = "SELECT fn_deletar_produto(%s)"
        result = self.db.execute_query(query, (produto_id,), fetch_one=True)
        self.db.commit()
        return result['fn_deletar_produto'] if result else False
    
    def get_or_create(self, nome: str, descricao: str = None) -> Produto:
        """
        Busca ou cria um produto via stored procedure
        
        Args:
            nome: Nome do produto
            descricao: Descrição do produto
            
        Returns:
            Produto existente ou novo
        """
        query = "SELECT * FROM fn_get_or_create_produto(%s, %s)"
        result = self.db.execute_query(query, (nome, descricao), fetch_one=True)
        self.db.commit()
        return Produto.from_dict(result) if result else None


class AplicacaoRepository(BaseRepository):
    """Repositório para operações com Aplicações usando Stored Procedures"""
    
    def create(self, aplicacao: Aplicacao) -> Aplicacao:
        """
        Cria uma nova aplicação via stored procedure
        
        Args:
            aplicacao: Instância de Aplicacao
            
        Returns:
            Aplicacao criada com ID
        """
        query = "SELECT * FROM fn_criar_aplicacao(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        result = self.db.execute_query(
            query,
            (
                aplicacao.nome_aplicacao, aplicacao.produto_id, aplicacao.ambiente,
                aplicacao.tipo_aplicacao, aplicacao.framework,
                aplicacao.ferramenta_versionamento, aplicacao.tipo_pipeline,
                aplicacao.versao, aplicacao.hospedagem, aplicacao.sbom,
                aplicacao.scan_imagens, aplicacao.secret_manager,
                aplicacao.sast_sonarqube, aplicacao.data_ultima_revisao,
                aplicacao.data_criacao
            ),
            fetch_one=True
        )
        self.db.commit()
        return Aplicacao.from_dict(result)
    
    def get_by_id(self, aplicacao_id: int) -> Optional[Aplicacao]:
        """
        Busca aplicação por ID via stored procedure
        
        Args:
            aplicacao_id: ID da aplicação
            
        Returns:
            Aplicacao ou None
        """
        query = "SELECT * FROM fn_buscar_aplicacao_por_id(%s)"
        result = self.db.execute_query(query, (aplicacao_id,), fetch_one=True)
        return Aplicacao.from_dict(result) if result else None
    
    def get_all(self, filters: Dict[str, Any] = None) -> List[Aplicacao]:
        """
        Retorna todas as aplicações com filtros opcionais via stored procedure
        
        Args:
            filters: Dicionário com filtros (produto_id, ambiente, etc.)
            
        Returns:
            Lista de Aplicacoes
        """
        # Preparar parâmetros para a stored procedure
        produto_id = filters.get('produto_id') if filters else None
        ambiente = filters.get('ambiente') if filters else None
        tipo_aplicacao = filters.get('tipo_aplicacao') if filters else None
        framework = filters.get('framework') if filters else None
        
        query = "SELECT * FROM fn_listar_aplicacoes(%s, %s, %s, %s)"
        results = self.db.execute_query(query, (produto_id, ambiente, tipo_aplicacao, framework))
        return [Aplicacao.from_dict(row) for row in results]
    
    def get_by_produto(self, produto_id: int) -> List[Aplicacao]:
        """
        Retorna aplicações de um produto específico via stored procedure
        
        Args:
            produto_id: ID do produto
            
        Returns:
            Lista de Aplicacoes
        """
        query = "SELECT * FROM sp_buscar_aplicacoes_por_produto(%s)"
        results = self.db.execute_query(query, (produto_id,))
        return [Aplicacao.from_dict(row) for row in results]
    
    def get_by_ambiente(self, ambiente: str) -> List[Aplicacao]:
        """
        Retorna aplicações de um ambiente específico via stored procedure
        
        Args:
            ambiente: Nome do ambiente
            
        Returns:
            Lista de Aplicacoes
        """
        query = "SELECT * FROM sp_buscar_aplicacoes_por_ambiente(%s)"
        results = self.db.execute_query(query, (ambiente,))
        return [Aplicacao.from_dict(row) for row in results]
    
    def update(self, aplicacao: Aplicacao) -> Aplicacao:
        """
        Atualiza uma aplicação via stored procedure
        
        Args:
            aplicacao: Instância de Aplicacao com ID
            
        Returns:
            Aplicacao atualizada
        """
        query = "SELECT * FROM fn_atualizar_aplicacao(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        result = self.db.execute_query(
            query,
            (
                aplicacao.id, aplicacao.nome_aplicacao, aplicacao.produto_id,
                aplicacao.ambiente, aplicacao.tipo_aplicacao, aplicacao.framework,
                aplicacao.ferramenta_versionamento, aplicacao.tipo_pipeline,
                aplicacao.versao, aplicacao.hospedagem, aplicacao.sbom,
                aplicacao.scan_imagens, aplicacao.secret_manager,
                aplicacao.sast_sonarqube, aplicacao.data_ultima_revisao,
                aplicacao.data_criacao
            ),
            fetch_one=True
        )
        self.db.commit()
        return Aplicacao.from_dict(result)
    
    def delete(self, aplicacao_id: int) -> bool:
        """
        Deleta uma aplicação via stored procedure
        
        Args:
            aplicacao_id: ID da aplicação
            
        Returns:
            True se deletado com sucesso
        """
        query = "SELECT fn_deletar_aplicacao(%s)"
        result = self.db.execute_query(query, (aplicacao_id,), fetch_one=True)
        self.db.commit()
        return result['fn_deletar_aplicacao'] if result else False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas das aplicações via stored procedure
        
        Returns:
            Dicionário com estatísticas
        """
        query = "SELECT * FROM fn_obter_stats_aplicacoes()"
        result = self.db.execute_query(query, fetch_one=True)
        return dict(result) if result else {}
    
    def search(self, term: str) -> List[Aplicacao]:
        """
        Busca aplicações por termo via stored procedure
        
        Args:
            term: Termo de busca
            
        Returns:
            Lista de Aplicacoes
        """
        query = "SELECT * FROM sp_buscar_aplicacoes_por_termo(%s)"
        results = self.db.execute_query(query, (term,))
        return [Aplicacao.from_dict(row) for row in results]


class GMUDRepository(BaseRepository):
    """Repositório para operações com GMUDs usando Stored Procedures"""
    
    def create(self, gmud: GMUD) -> GMUD:
        """
        Cria uma nova GMUD via stored procedure
        
        Args:
            gmud: Instância de GMUD
            
        Returns:
            GMUD criada com ID
        """
        query = "SELECT * FROM fn_criar_gmud(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        result = self.db.execute_query(
            query,
            (
                gmud.id_item, gmud.data_hora_prevista, gmud.responsavel_executor,
                gmud.tempo_estimado, gmud.solicitante_area, gmud.nome_aplicacao,
                gmud.aplicacao_id, gmud.ambiente, gmud.hostname_namespace,
                gmud.local_implantacao, gmud.build_release,
                gmud.configuracoes_alteradas, gmud.tempo_realizado,
                gmud.ocorrencias, gmud.solucoes_atribuidas,
                gmud.validacoes_realizadas, gmud.risco_operacao,
                gmud.impacto, gmud.rca, gmud.controle
            ),
            fetch_one=True
        )
        self.db.commit()
        return GMUD.from_dict(result)
    
    def get_by_id(self, gmud_id: int) -> Optional[GMUD]:
        """
        Busca GMUD por ID via stored procedure
        
        Args:
            gmud_id: ID da GMUD
            
        Returns:
            GMUD ou None
        """
        query = "SELECT * FROM fn_buscar_gmud_por_id(%s)"
        result = self.db.execute_query(query, (gmud_id,), fetch_one=True)
        return GMUD.from_dict(result) if result else None
    
    def get_by_id_item(self, id_item: str) -> Optional[GMUD]:
        """
        Busca GMUD por ID do item via stored procedure
        
        Args:
            id_item: ID do item da GMUD
            
        Returns:
            GMUD ou None
        """
        query = "SELECT * FROM fn_buscar_gmud_por_id_item(%s)"
        result = self.db.execute_query(query, (id_item,), fetch_one=True)
        return GMUD.from_dict(result) if result else None
    
    def get_all(self, filters: Dict[str, Any] = None) -> List[GMUD]:
        """
        Retorna todas as GMUDs com filtros opcionais via stored procedure
        
        Args:
            filters: Dicionário com filtros (ambiente, aplicacao_id, risco_operacao, data_inicio, data_fim)
            
        Returns:
            Lista de GMUDs
        """
        # Extrair valores dos filtros ou usar None
        ambiente = filters.get('ambiente') if filters else None
        aplicacao_id = filters.get('aplicacao_id') if filters else None
        risco = filters.get('risco_operacao') if filters else None
        data_inicio = filters.get('data_inicio') if filters else None
        data_fim = filters.get('data_fim') if filters else None
        
        query = "SELECT * FROM fn_listar_gmuds(%s, %s, %s, %s, %s)"
        results = self.db.execute_query(
            query,
            (ambiente, aplicacao_id, risco, data_inicio, data_fim)
        )
        return [GMUD.from_dict(row) for row in results]
    
    def get_by_periodo(self, data_inicio: datetime, data_fim: datetime) -> List[GMUD]:
        """
        Retorna GMUDs de um período
        
        Args:
            data_inicio: Data inicial
            data_fim: Data final
            
        Returns:
            Lista de GMUDs
        """
        return self.get_all({'data_inicio': data_inicio, 'data_fim': data_fim})
    
    def get_by_ambiente(self, ambiente: str) -> List[GMUD]:
        """
        Retorna GMUDs de um ambiente
        
        Args:
            ambiente: Nome do ambiente
            
        Returns:
            Lista de GMUDs
        """
        return self.get_all({'ambiente': ambiente})
    
    def update(self, gmud: GMUD) -> GMUD:
        """
        Atualiza uma GMUD via stored procedure
        
        Args:
            gmud: Instância de GMUD com ID
            
        Returns:
            GMUD atualizada
        """
        query = "SELECT * FROM fn_atualizar_gmud(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        result = self.db.execute_query(
            query,
            (
                gmud.id, gmud.id_item, gmud.data_hora_prevista,
                gmud.responsavel_executor, gmud.tempo_estimado,
                gmud.solicitante_area, gmud.nome_aplicacao,
                gmud.aplicacao_id, gmud.ambiente, gmud.hostname_namespace,
                gmud.local_implantacao, gmud.build_release,
                gmud.configuracoes_alteradas, gmud.tempo_realizado,
                gmud.ocorrencias, gmud.solucoes_atribuidas,
                gmud.validacoes_realizadas, gmud.risco_operacao,
                gmud.impacto, gmud.rca, gmud.controle
            ),
            fetch_one=True
        )
        self.db.commit()
        return GMUD.from_dict(result)
    
    def delete(self, gmud_id: int) -> bool:
        """
        Deleta uma GMUD via stored procedure
        
        Args:
            gmud_id: ID da GMUD
            
        Returns:
            True se deletado com sucesso
        """
        query = "SELECT fn_deletar_gmud(%s)"
        result = self.db.execute_query(query, (gmud_id,), fetch_one=True)
        self.db.commit()
        return result['fn_deletar_gmud'] if result else False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas das GMUDs via stored procedure
        
        Returns:
            Dicionário com estatísticas
        """
        query = "SELECT * FROM fn_obter_stats_gmuds()"
        result = self.db.execute_query(query, fetch_one=True)
        return dict(result) if result else {}

