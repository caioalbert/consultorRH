"""
Modelos de dados para o banco PostgreSQL
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class Produto:
    """Modelo de Produto"""
    id: Optional[int] = None
    nome: str = ""
    descricao: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Produto':
        """Cria instância a partir de dicionário"""
        return cls(
            id=data.get('id'),
            nome=data.get('nome', ''),
            descricao=data.get('descricao'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


@dataclass
class Aplicacao:
    """Modelo de Aplicação"""
    id: Optional[int] = None
    nome_aplicacao: str = ""
    produto_id: Optional[int] = None
    ambiente: str = ""
    tipo_aplicacao: Optional[str] = None
    framework: Optional[str] = None
    ferramenta_versionamento: Optional[str] = None
    tipo_pipeline: Optional[str] = None
    versao: Optional[str] = None
    hospedagem: Optional[str] = None
    sbom: bool = False
    scan_imagens: bool = False
    secret_manager: bool = False
    sast_sonarqube: bool = False
    data_ultima_revisao: Optional[date] = None
    data_criacao: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Campo auxiliar para nome do produto
    produto_nome: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Aplicacao':
        """Cria instância a partir de dicionário"""
        return cls(
            id=data.get('id'),
            nome_aplicacao=data.get('nome_aplicacao', ''),
            produto_id=data.get('produto_id'),
            ambiente=data.get('ambiente', ''),
            tipo_aplicacao=data.get('tipo_aplicacao'),
            framework=data.get('framework'),
            ferramenta_versionamento=data.get('ferramenta_versionamento'),
            tipo_pipeline=data.get('tipo_pipeline'),
            versao=data.get('versao'),
            hospedagem=data.get('hospedagem'),
            sbom=data.get('sbom', False),
            scan_imagens=data.get('scan_imagens', False),
            secret_manager=data.get('secret_manager', False),
            sast_sonarqube=data.get('sast_sonarqube', False),
            data_ultima_revisao=data.get('data_ultima_revisao'),
            data_criacao=data.get('data_criacao'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            produto_nome=data.get('produto_nome')
        )
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id': self.id,
            'nome_aplicacao': self.nome_aplicacao,
            'produto_id': self.produto_id,
            'ambiente': self.ambiente,
            'tipo_aplicacao': self.tipo_aplicacao,
            'framework': self.framework,
            'ferramenta_versionamento': self.ferramenta_versionamento,
            'tipo_pipeline': self.tipo_pipeline,
            'versao': self.versao,
            'hospedagem': self.hospedagem,
            'sbom': self.sbom,
            'scan_imagens': self.scan_imagens,
            'secret_manager': self.secret_manager,
            'sast_sonarqube': self.sast_sonarqube,
            'data_ultima_revisao': self.data_ultima_revisao,
            'data_criacao': self.data_criacao,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'produto_nome': self.produto_nome
        }


@dataclass
class GMUD:
    """Modelo de GMUD"""
    id: Optional[int] = None
    id_item: str = ""
    data_hora_prevista: Optional[datetime] = None
    responsavel_executor: Optional[str] = None
    tempo_estimado: Optional[str] = None
    solicitante_area: Optional[str] = None
    nome_aplicacao: Optional[str] = None
    aplicacao_id: Optional[int] = None
    ambiente: Optional[str] = None
    hostname_namespace: Optional[str] = None
    local_implantacao: Optional[str] = None
    build_release: Optional[str] = None
    configuracoes_alteradas: Optional[str] = None
    tempo_realizado: Optional[str] = None
    ocorrencias: Optional[str] = None
    solucoes_atribuidas: Optional[str] = None
    validacoes_realizadas: Optional[str] = None
    risco_operacao: Optional[str] = None
    impacto: Optional[str] = None
    rca: Optional[str] = None
    controle: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GMUD':
        """Cria instância a partir de dicionário"""
        return cls(
            id=data.get('id'),
            id_item=data.get('id_item', ''),
            data_hora_prevista=data.get('data_hora_prevista'),
            responsavel_executor=data.get('responsavel_executor'),
            tempo_estimado=data.get('tempo_estimado'),
            solicitante_area=data.get('solicitante_area'),
            nome_aplicacao=data.get('nome_aplicacao'),
            aplicacao_id=data.get('aplicacao_id'),
            ambiente=data.get('ambiente'),
            hostname_namespace=data.get('hostname_namespace'),
            local_implantacao=data.get('local_implantacao'),
            build_release=data.get('build_release'),
            configuracoes_alteradas=data.get('configuracoes_alteradas'),
            tempo_realizado=data.get('tempo_realizado'),
            ocorrencias=data.get('ocorrencias'),
            solucoes_atribuidas=data.get('solucoes_atribuidas'),
            validacoes_realizadas=data.get('validacoes_realizadas'),
            risco_operacao=data.get('risco_operacao'),
            impacto=data.get('impacto'),
            rca=data.get('rca'),
            controle=data.get('controle'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            'id': self.id,
            'id_item': self.id_item,
            'data_hora_prevista': self.data_hora_prevista,
            'responsavel_executor': self.responsavel_executor,
            'tempo_estimado': self.tempo_estimado,
            'solicitante_area': self.solicitante_area,
            'nome_aplicacao': self.nome_aplicacao,
            'aplicacao_id': self.aplicacao_id,
            'ambiente': self.ambiente,
            'hostname_namespace': self.hostname_namespace,
            'local_implantacao': self.local_implantacao,
            'build_release': self.build_release,
            'configuracoes_alteradas': self.configuracoes_alteradas,
            'tempo_realizado': self.tempo_realizado,
            'ocorrencias': self.ocorrencias,
            'solucoes_atribuidas': self.solucoes_atribuidas,
            'validacoes_realizadas': self.validacoes_realizadas,
            'risco_operacao': self.risco_operacao,
            'impacto': self.impacto,
            'rca': self.rca,
            'controle': self.controle,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
