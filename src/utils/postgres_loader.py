"""
Módulo para carregamento de dados do PostgreSQL usando Stored Procedures
"""
import pandas as pd
import psycopg2
import os
from typing import Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class PostgresDataLoader:
    """Classe para carregar dados do PostgreSQL AWS RDS usando Stored Procedures"""
    
    def __init__(self):
        """Inicializa conexão com o banco"""
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Conecta ao banco de dados"""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT', 5432),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
        except Exception as e:
            raise ConnectionError(f"Erro ao conectar ao banco: {e}")
    
    def close(self):
        """Fecha conexão"""
        if self.conn:
            self.conn.close()
    
    def load_aplicacoes(self, produto_id: Optional[int] = None, 
                       ambiente: Optional[str] = None,
                       tipo_aplicacao: Optional[str] = None,
                       framework: Optional[str] = None) -> pd.DataFrame:
        """
        Carrega aplicações do banco usando stored procedure fn_listar_aplicacoes
        
        Args:
            produto_id: Filtrar por produto
            ambiente: Filtrar por ambiente
            tipo_aplicacao: Filtrar por tipo de aplicação
            framework: Filtrar por framework
            
        Returns:
            DataFrame com aplicações
        """
        # Usa a stored procedure fn_listar_aplicacoes
        query = "SELECT * FROM fn_listar_aplicacoes(%s, %s, %s, %s)"
        params = (produto_id, ambiente, tipo_aplicacao, framework)
        
        df = pd.read_sql_query(query, self.conn, params=params)
        
        # Processa dados
        self._process_aplicacoes(df)
        
        return df
    
    def _process_aplicacoes(self, df: pd.DataFrame):
        """Processa DataFrame de aplicações"""
        if df.empty:
            return
        
        # Converte datas
        date_columns = ['data_ultima_revisao', 'data_criacao']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Adiciona coluna de meses desde última revisão
        if 'data_ultima_revisao' in df.columns:
            hoje = datetime.now()
            df['meses_sem_revisao'] = df['data_ultima_revisao'].apply(
                lambda x: ((hoje - x).days / 30) if pd.notnull(x) else None
            )
        
        # Renomeia colunas para compatibilidade com código existente
        df.rename(columns={
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
            'data_criacao': 'Data_Criacao',
            'meses_sem_revisao': 'Meses_Sem_Revisao'
        }, inplace=True)
        
        # Converte booleanos para Sim/Não
        bool_columns = ['SBOM', 'Scan_Imagens', 'Secret_Manager', 'SAST_SonarCube']
        for col in bool_columns:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: 'Sim' if x else 'Não')
        
        # Preenche nulos
        df.fillna({
            'Produto': 'Não Especificado',
            'Ambiente': 'Não Especificado',
            'Tipo_Aplicacao': 'Não Especificado',
            'Framework': 'Não Especificado',
            'Ferramenta_Versionamento': 'Não Especificado',
            'Tipo_Pipeline': 'Não Especificado',
            'Versao': 'Não Especificado',
            'Hospedagem': 'Não Especificado'
        }, inplace=True)
    
    def load_gmuds(self, ambiente: Optional[str] = None,
                   aplicacao_id: Optional[int] = None,
                   risco: Optional[str] = None,
                   data_inicio: Optional[str] = None,
                   data_fim: Optional[str] = None) -> pd.DataFrame:
        """
        Carrega GMUDs do banco usando stored procedure fn_listar_gmuds
        
        Args:
            ambiente: Filtrar por ambiente
            aplicacao_id: Filtrar por aplicação
            risco: Filtrar por risco
            data_inicio: Data inicial
            data_fim: Data final
            
        Returns:
            DataFrame com GMUDs
        """
        # Usa a stored procedure fn_listar_gmuds
        query = "SELECT * FROM fn_listar_gmuds(%s, %s, %s, %s, %s)"
        params = (ambiente, aplicacao_id, risco, data_inicio, data_fim)
        
        df = pd.read_sql_query(query, self.conn, params=params)
        
        # Processa dados
        self._process_gmuds(df)
        
        return df
    
    def _process_gmuds(self, df: pd.DataFrame):
        """Processa DataFrame de GMUDs"""
        if df.empty:
            return
        
        # Converte datas
        if 'data_hora_prevista' in df.columns:
            df['data_hora_prevista'] = pd.to_datetime(df['data_hora_prevista'], errors='coerce')
        
        # Renomeia colunas para compatibilidade com dashboards
        rename_map = {
            'id_item': 'ID_Item',
            'data_hora_prevista': 'Data_Prevista',
            'responsavel_executor': 'Responsavel',
            'tempo_estimado': 'Tempo_Estimado',
            'solicitante_area': 'Solicitante',
            'ambiente': 'Ambiente',
            'hostname_namespace': 'Hostname',
            'local_implantacao': 'Local_Implantacao',
            'build_release': 'Build_Release',
            'configuracoes_alteradas': 'Configuracoes',
            'tempo_realizado': 'Tempo_Realizado',
            'ocorrencias': 'Ocorrencias',
            'solucoes_atribuidas': 'Solucoes',
            'validacoes_realizadas': 'Validacoes',
            'risco_operacao': 'Risco_Operacao',
            'impacto': 'Impacto',
            'rca': 'RCA',
            'controle': 'Controle'
        }
        df.rename(columns=rename_map, inplace=True)
        
        # Adiciona Nome_Aplicacao se não existir
        if 'Nome_Aplicacao' not in df.columns:
            df['Nome_Aplicacao'] = 'N/A'
        
        # Garante que colunas essenciais existam e não sejam nulas
        for col in ['Nome_Aplicacao', 'Ambiente', 'Responsavel', 'Risco_Operacao', 'Local_Implantacao']:
            if col in df.columns:
                df[col].fillna('N/A', inplace=True)
    
    def load_produtos(self) -> pd.DataFrame:
        """Carrega produtos do banco usando stored procedure fn_listar_produtos"""
        query = "SELECT * FROM fn_listar_produtos()"
        return pd.read_sql_query(query, self.conn)
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas resumidas usando stored procedures"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Usa stored procedure para estatísticas de aplicações
        cursor.execute("SELECT * FROM fn_obter_stats_aplicacoes()")
        app_stats = cursor.fetchone()
        if app_stats:
            stats['total_aplicacoes'] = app_stats[0]
            stats['produtos_unicos'] = app_stats[1]
            stats['ambientes_unicos'] = app_stats[2]
            stats['frameworks_unicos'] = app_stats[3]
            
            # Calcula percentuais
            total = app_stats[0]
            stats['percentual_sbom'] = (app_stats[4] / total * 100) if total > 0 else 0
            stats['percentual_scan'] = (app_stats[5] / total * 100) if total > 0 else 0
            stats['percentual_secret_manager'] = (app_stats[6] / total * 100) if total > 0 else 0
            stats['percentual_sast'] = (app_stats[7] / total * 100) if total > 0 else 0
        
        # Usa stored procedure para estatísticas de GMUDs
        cursor.execute("SELECT * FROM fn_obter_stats_gmuds()")
        gmud_stats = cursor.fetchone()
        if gmud_stats:
            stats['total_gmuds'] = gmud_stats[0]
            stats['total_ambientes_gmud'] = gmud_stats[1]
            stats['total_aplicacoes_gmud'] = gmud_stats[2]
            stats['risco_alto'] = gmud_stats[3]
            stats['risco_medio'] = gmud_stats[4]
            stats['risco_baixo'] = gmud_stats[5]
        
        cursor.close()
        
        return stats
    
    def buscar_aplicacao_por_id(self, app_id: int) -> Optional[Dict[str, Any]]:
        """Busca aplicação por ID usando stored procedure fn_buscar_aplicacao_por_id"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM fn_buscar_aplicacao_por_id(%s)", (app_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            columns = ['id', 'nome_aplicacao', 'produto_id', 'ambiente', 'tipo_aplicacao',
                      'framework', 'ferramenta_versionamento', 'tipo_pipeline', 'versao',
                      'hospedagem', 'sbom', 'scan_imagens', 'secret_manager', 'sast_sonarqube',
                      'data_ultima_revisao', 'data_criacao', 'created_at', 'updated_at', 'produto_nome']
            return dict(zip(columns, result))
        return None
    
    def buscar_aplicacoes_por_termo(self, termo: str) -> pd.DataFrame:
        """Busca aplicações por termo usando stored procedure fn_buscar_aplicacoes_por_termo"""
        query = "SELECT * FROM fn_buscar_aplicacoes_por_termo(%s)"
        df = pd.read_sql_query(query, self.conn, params=(termo,))
        self._process_aplicacoes(df)
        return df
    
    def buscar_aplicacoes_por_produto(self, produto_id: int) -> pd.DataFrame:
        """Busca aplicações por produto usando stored procedure fn_buscar_aplicacoes_por_produto"""
        query = "SELECT * FROM fn_buscar_aplicacoes_por_produto(%s)"
        df = pd.read_sql_query(query, self.conn, params=(produto_id,))
        self._process_aplicacoes(df)
        return df
    
    def buscar_aplicacoes_por_ambiente(self, ambiente: str) -> pd.DataFrame:
        """Busca aplicações por ambiente usando stored procedure fn_buscar_aplicacoes_por_ambiente"""
        query = "SELECT * FROM fn_buscar_aplicacoes_por_ambiente(%s)"
        df = pd.read_sql_query(query, self.conn, params=(ambiente,))
        self._process_aplicacoes(df)
        return df
    
    def buscar_gmud_por_id(self, gmud_id: int) -> Optional[Dict[str, Any]]:
        """Busca GMUD por ID usando stored procedure fn_buscar_gmud_por_id"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM fn_buscar_gmud_por_id(%s)", (gmud_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def buscar_gmud_por_id_item(self, id_item: str) -> Optional[Dict[str, Any]]:
        """Busca GMUD por ID do item usando stored procedure fn_buscar_gmud_por_id_item"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM fn_buscar_gmud_por_id_item(%s)", (id_item,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def buscar_produto_por_nome(self, nome: str) -> Optional[Dict[str, Any]]:
        """Busca produto por nome usando stored procedure fn_buscar_produto_por_nome"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM fn_buscar_produto_por_nome(%s)", (nome,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return {'id': result[0], 'nome': result[1], 'descricao': result[2]}
        return None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# Função para manter compatibilidade com código existente
def load_gmud_data(file_path: str = None) -> pd.DataFrame:
    """
    Carrega dados de GMUD (mantém compatibilidade com versão antiga)
    Agora carrega do PostgreSQL usando stored procedures
    """
    with PostgresDataLoader() as loader:
        return loader.load_gmuds()
