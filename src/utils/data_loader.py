"""
Módulo para carregamento e processamento de dados do inventário de aplicações
"""
import pandas as pd
from datetime import datetime
from typing import Dict, Any
import os


class InventoryDataLoader:
    """Classe para carregar e processar dados do inventário"""
    
    def __init__(self, file_path: str):
        """
        Inicializa o carregador de dados
        
        Args:
            file_path: Caminho para o arquivo CSV ou Excel
        """
        self.file_path = file_path
        self.df = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Carrega os dados do arquivo CSV ou Excel
        
        Returns:
            DataFrame com os dados do inventário
        """
        # Normaliza o caminho do arquivo
        self.file_path = os.path.abspath(self.file_path)
        
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {self.file_path}")
        
        # Detecta o tipo de arquivo
        file_extension = os.path.splitext(self.file_path)[1].lower()
        
        if not file_extension:
            raise ValueError(f"Arquivo sem extensão. Use .csv, .xlsx ou .xls")
        
        if file_extension == '.csv':
            self.df = pd.read_csv(self.file_path, encoding='utf-8-sig')
        elif file_extension in ['.xlsx', '.xls']:
            self.df = pd.read_excel(self.file_path)
        else:
            raise ValueError(f"Formato de arquivo não suportado: {file_extension}. Use .csv, .xlsx ou .xls")
        
        # Processa os dados
        self._process_data()
        
        return self.df
    
    def _process_data(self):
        """Processa e limpa os dados carregados"""
        if self.df is None:
            return
        
        # Converte datas
        date_columns = ['Data_Ultima_Revisao', 'Data_Criacao']
        for col in date_columns:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        # Preenche valores nulos com valores padrão
        self.df.fillna({
            'Produto': 'Não Especificado',
            'Ambiente': 'Não Especificado',
            'Tipo_Aplicacao': 'Não Especificado',
            'Framework': 'Não Especificado',
            'Ferramenta_Versionamento': 'Não Especificado',
            'Tipo_Pipeline': 'Não Especificado',
            'Versao': 'Não Especificado',
            'Hospedagem': 'Não Especificado',
            'SBOM': 'Não',
            'Scan_Imagens': 'Não',
            'Secret_Manager': 'Não',
            'SAST_SonarCube': 'Não'
        }, inplace=True)
        
        # Adiciona coluna de meses desde última revisão
        if 'Data_Ultima_Revisao' in self.df.columns:
            hoje = datetime.now()
            self.df['Meses_Sem_Revisao'] = self.df['Data_Ultima_Revisao'].apply(
                lambda x: ((hoje - x).days / 30) if pd.notnull(x) else None
            )
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas resumidas do inventário
        
        Returns:
            Dicionário com estatísticas
        """
        if self.df is None:
            return {}
        
        stats = {
            'total_aplicacoes': len(self.df),
            'produtos_unicos': self.df['Produto'].nunique() if 'Produto' in self.df.columns else 0,
            'ambientes_unicos': self.df['Ambiente'].nunique() if 'Ambiente' in self.df.columns else 0,
            'frameworks_unicos': self.df['Framework'].nunique() if 'Framework' in self.df.columns else 0
        }
        
        return stats
    
    def filter_by_column(self, column: str, value: Any) -> pd.DataFrame:
        """
        Filtra o DataFrame por uma coluna específica
        
        Args:
            column: Nome da coluna
            value: Valor para filtrar
            
        Returns:
            DataFrame filtrado
        """
        if self.df is None or column not in self.df.columns:
            return pd.DataFrame()
        
        return self.df[self.df[column] == value]
    
    def get_unique_values(self, column: str) -> list:
        """
        Retorna valores únicos de uma coluna
        
        Args:
            column: Nome da coluna
            
        Returns:
            Lista de valores únicos
        """
        if self.df is None or column not in self.df.columns:
            return []
        
        return sorted(self.df[column].unique().tolist())


def load_gmud_data(file_path: str) -> pd.DataFrame:
    """
    Carrega dados de GMUD do arquivo CSV
    
    Args:
        file_path: Caminho para o arquivo CSV de GMUDs
        
    Returns:
        DataFrame com os dados de GMUD
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        
        # Normalizar nomes das colunas
        df.columns = df.columns.str.strip()
        column_mapping = {
            'ID do Item': 'ID_Item',
            'Data/hora Prevista': 'Data_Prevista',
            'Responsável / Executor': 'Responsavel',
            'Tempo Estimado': 'Tempo_Estimado',
            'Solicitante / área de atuação': 'Solicitante',
            'Nome da Aplicação': 'Nome_Aplicacao',
            'Ambiente': 'Ambiente',
            'hostname/namespace': 'Hostname',
            'Local de Implantação': 'Local_Implantacao',
            'Build/Release': 'Build_Release',
            'Configurações alteradas': 'Configuracoes_Alteradas',
            'Tempo Realizado': 'Tempo_Realizado',
            'Ocorrências': 'Ocorrencias',
            'Soluções Atribuídas': 'Solucoes_Atribuidas',
            'Validações Realizadas': 'Validacoes_Realizadas',
            'Risco a Operação': 'Risco_Operacao',
            'Impacto': 'Impacto',
            'RCA': 'RCA',
            'Controle': 'Controle'
        }
        df = df.rename(columns=column_mapping)
        
        # Converter coluna de data
        if 'Data_Prevista' in df.columns:
            df['Data_Prevista'] = pd.to_datetime(df['Data_Prevista'], format='%d/%m/%y %H:%M', errors='coerce')
            if df['Data_Prevista'].isna().all():
                df['Data_Prevista'] = pd.to_datetime(df['Data_Prevista'], format='%d/%m/%Y %H:%M', errors='coerce')
        
        # Preencher valores nulos
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].fillna('Não informado')
            elif df[col].dtype in ['float64', 'int64']:
                df[col] = df[col].fillna(0)
        
        return df
    except Exception as e:
        print(f"Erro ao carregar dados de GMUD: {str(e)}")
        return pd.DataFrame()
