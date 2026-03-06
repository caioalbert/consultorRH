"""
Módulo de acesso ao banco de dados PostgreSQL

Exemplo de uso básico:
    from src.database import get_data_service
    
    service = get_data_service()
    aplicacoes = service.get_aplicacoes({'ambiente': 'Produção'})
    df = service.get_aplicacoes_df()

Exemplo com repositórios diretos:
    from src.database import get_connection, AplicacaoRepository
    
    db = get_connection()
    repo = AplicacaoRepository(db)
    apps = repo.get_all()
"""
from .connection import DatabaseConnection, get_connection
from .repositories import (
    ProdutoRepository,
    AplicacaoRepository,
    GMUDRepository
)
from .services import DataService, get_data_service
from .models import Produto, Aplicacao, GMUD

__all__ = [
    'DatabaseConnection',
    'get_connection',
    'ProdutoRepository',
    'AplicacaoRepository',
    'GMUDRepository',
    'DataService',
    'get_data_service',
    'Produto',
    'Aplicacao',
    'GMUD'
]
