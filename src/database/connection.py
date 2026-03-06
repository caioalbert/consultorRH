"""
Gerenciador de conexão com PostgreSQL
"""
import psycopg2
import psycopg2.extras
import os
from typing import Optional
from contextlib import contextmanager


class DatabaseConnection:
    """Classe para gerenciar conexões com PostgreSQL"""
    
    def __init__(self):
        """Inicializa a conexão com o banco de dados"""
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'devops_hub'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        self._connection: Optional[psycopg2.extensions.connection] = None
    
    def connect(self) -> psycopg2.extensions.connection:
        """
        Estabelece conexão com o banco de dados
        
        Returns:
            Objeto de conexão psycopg2
        """
        if self._connection is None or self._connection.closed:
            try:
                self._connection = psycopg2.connect(**self.config)
                self._connection.autocommit = False
            except psycopg2.Error as e:
                raise ConnectionError(f"Erro ao conectar ao PostgreSQL: {e}")
        return self._connection
    
    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self._connection and not self._connection.closed:
            self._connection.close()
            self._connection = None
    
    def get_cursor(self, cursor_factory=None):
        """
        Retorna um cursor para executar queries
        
        Args:
            cursor_factory: Factory para criar cursor customizado (ex: RealDictCursor)
            
        Returns:
            Cursor do psycopg2
        """
        conn = self.connect()
        if cursor_factory:
            return conn.cursor(cursor_factory=cursor_factory)
        return conn.cursor()
    
    def commit(self):
        """Confirma transação"""
        if self._connection and not self._connection.closed:
            self._connection.commit()
    
    def rollback(self):
        """Desfaz transação"""
        if self._connection and not self._connection.closed:
            self._connection.rollback()
    
    @contextmanager
    def transaction(self):
        """
        Context manager para transações
        
        Usage:
            with db.transaction():
                # operações do banco
        """
        try:
            yield self
            self.commit()
        except Exception:
            self.rollback()
            raise
    
    def execute_query(self, query: str, params: tuple = None, fetch_one: bool = False, fetch_all: bool = True):
        """
        Executa uma query e retorna resultados
        
        Args:
            query: SQL query a ser executada
            params: Parâmetros para a query
            fetch_one: Se True, retorna apenas um resultado
            fetch_all: Se True, retorna todos os resultados
            
        Returns:
            Resultado da query ou None
        """
        cursor = self.get_cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cursor.execute(query, params or ())
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            
            return None
        except psycopg2.Error as e:
            self.rollback()
            raise Exception(f"Erro ao executar query: {e}")
        finally:
            cursor.close()
    
    def execute_many(self, query: str, params_list: list):
        """
        Executa múltiplas queries com diferentes parâmetros
        
        Args:
            query: SQL query a ser executada
            params_list: Lista de tuplas com parâmetros
        """
        cursor = self.get_cursor()
        try:
            cursor.executemany(query, params_list)
            self.commit()
        except psycopg2.Error as e:
            self.rollback()
            raise Exception(f"Erro ao executar batch: {e}")
        finally:
            cursor.close()
    
    def test_connection(self) -> bool:
        """
        Testa se a conexão está funcionando
        
        Returns:
            True se conectou com sucesso, False caso contrário
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except Exception:
            return False


# Singleton global
_db_connection: Optional[DatabaseConnection] = None


def get_connection() -> DatabaseConnection:
    """
    Retorna a instância singleton da conexão
    
    Returns:
        DatabaseConnection instance
    """
    global _db_connection
    if _db_connection is None:
        _db_connection = DatabaseConnection()
    return _db_connection
