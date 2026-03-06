"""
Serviço de sincronização de dados do Azure DevOps
Coleta e armazena dados no banco PostgreSQL
"""
import psycopg2
from datetime import datetime
from typing import Dict, List
from src.integrations.azure_devops_client import AzureDevOpsClient


class AzureDevOpsSyncService:
    """Serviço para sincronizar dados do Azure DevOps"""
    
    def __init__(self, db_conn, cliente_id: int, azure_org: str, azure_pat: str):
        self.conn = db_conn
        self.cliente_id = cliente_id
        self.client = AzureDevOpsClient(azure_org, azure_pat)
        self.sync_id = None
    
    def _start_sync(self, tipo: str = 'full'):
        """Registra início da sincronização"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO sincronizacoes (cliente_id, tipo, status, data_inicio)
            VALUES (%s, %s, 'running', %s)
            RETURNING id
        """, (self.cliente_id, tipo, datetime.now()))
        self.sync_id = cursor.fetchone()[0]
        self.conn.commit()
        return self.sync_id
    
    def _end_sync(self, status: str, registros: int = 0, erros: str = None):
        """Registra fim da sincronização"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE sincronizacoes
            SET status = %s,
                data_fim = %s,
                duracao_segundos = EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - data_inicio)),
                registros_processados = %s,
                erros = %s
            WHERE id = %s
        """, (status, datetime.now(), registros, erros, self.sync_id))
        self.conn.commit()
    
    def sync_projetos(self) -> int:
        """Sincroniza projetos do Azure DevOps"""
        cursor = self.conn.cursor()
        projetos = self.client.get_projects()
        count = 0
        
        for projeto in projetos:
            cursor.execute("""
                INSERT INTO projetos (
                    cliente_id, azure_project_id, nome, descricao, 
                    url, visibilidade, estado
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (cliente_id, azure_project_id) 
                DO UPDATE SET
                    nome = EXCLUDED.nome,
                    descricao = EXCLUDED.descricao,
                    url = EXCLUDED.url,
                    visibilidade = EXCLUDED.visibilidade,
                    estado = EXCLUDED.estado,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id
            """, (
                self.cliente_id,
                projeto['id'],
                projeto['name'],
                projeto.get('description', ''),
                projeto.get('url', ''),
                projeto.get('visibility', 'private'),
                projeto.get('state', 'wellFormed')
            ))
            count += 1
        
        self.conn.commit()
        return count
    
    def sync_repositorios(self, projeto_id: int, projeto_name: str) -> int:
        """Sincroniza repositórios de um projeto"""
        cursor = self.conn.cursor()
        repos = self.client.get_repositories(projeto_name)
        count = 0
        
        for repo in repos:
            cursor.execute("""
                INSERT INTO repositorios (
                    projeto_id, azure_repo_id, nome, url, 
                    tamanho_kb, default_branch
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (projeto_id, azure_repo_id)
                DO UPDATE SET
                    nome = EXCLUDED.nome,
                    url = EXCLUDED.url,
                    tamanho_kb = EXCLUDED.tamanho_kb,
                    default_branch = EXCLUDED.default_branch,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                projeto_id,
                repo['id'],
                repo['name'],
                repo.get('webUrl', ''),
                repo.get('size', 0),
                repo.get('defaultBranch', 'main')
            ))
            count += 1
        
        self.conn.commit()
        return count
    
    def sync_pipelines(self, projeto_id: int, projeto_name: str) -> int:
        """Sincroniza pipelines de um projeto"""
        cursor = self.conn.cursor()
        pipelines = self.client.get_pipelines(projeto_name)
        count = 0
        
        for pipeline in pipelines:
            cursor.execute("""
                INSERT INTO pipelines (
                    projeto_id, azure_pipeline_id, nome, 
                    tipo, path, configuracao
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (projeto_id, azure_pipeline_id)
                DO UPDATE SET
                    nome = EXCLUDED.nome,
                    path = EXCLUDED.path,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id
            """, (
                projeto_id,
                pipeline['id'],
                pipeline['name'],
                'yaml',
                pipeline.get('folder', ''),
                'YAML'
            ))
            count += 1
        
        self.conn.commit()
        return count
    
    def sync_pipeline_runs(self, pipeline_db_id: int, projeto_name: str, 
                          pipeline_id: int, days: int = 30) -> int:
        """Sincroniza execuções de um pipeline"""
        cursor = self.conn.cursor()
        runs = self.client.get_pipeline_runs(projeto_name, pipeline_id, days)
        count = 0
        
        for run in runs:
            # Calcular duração
            duracao = None
            if run.get('finishedDate') and run.get('createdDate'):
                start = datetime.fromisoformat(run['createdDate'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(run['finishedDate'].replace('Z', '+00:00'))
                duracao = int((end - start).total_seconds())
            
            cursor.execute("""
                INSERT INTO pipeline_execucoes (
                    pipeline_id, azure_run_id, numero_execucao,
                    status, resultado, data_inicio, data_fim,
                    duracao_segundos, triggered_by, branch, motivo
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (pipeline_id, azure_run_id)
                DO UPDATE SET
                    status = EXCLUDED.status,
                    resultado = EXCLUDED.resultado,
                    data_fim = EXCLUDED.data_fim,
                    duracao_segundos = EXCLUDED.duracao_segundos
            """, (
                pipeline_db_id,
                run['id'],
                run.get('name', ''),
                run.get('state', 'unknown'),
                run.get('result', 'unknown'),
                run.get('createdDate'),
                run.get('finishedDate'),
                duracao,
                run.get('requestedBy', {}).get('displayName', 'Unknown'),
                run.get('sourceBranch', ''),
                run.get('reason', 'manual')
            ))
            count += 1
        
        self.conn.commit()
        return count
    
    def sync_work_items(self, projeto_id: int, projeto_name: str) -> int:
        """Sincroniza work items de um projeto"""
        cursor = self.conn.cursor()
        work_items = self.client.get_active_work_items(projeto_name)
        count = 0
        
        for wi in work_items:
            fields = wi.get('fields', {})
            
            cursor.execute("""
                INSERT INTO work_items (
                    projeto_id, azure_work_item_id, tipo, titulo,
                    descricao, estado, prioridade, assignado_para,
                    criado_por, story_points, data_criacao, data_modificacao
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (projeto_id, azure_work_item_id)
                DO UPDATE SET
                    titulo = EXCLUDED.titulo,
                    estado = EXCLUDED.estado,
                    assignado_para = EXCLUDED.assignado_para,
                    data_modificacao = EXCLUDED.data_modificacao,
                    updated_at = CURRENT_TIMESTAMP
            """, (
                projeto_id,
                wi['id'],
                fields.get('System.WorkItemType', 'Unknown'),
                fields.get('System.Title', ''),
                fields.get('System.Description', ''),
                fields.get('System.State', 'New'),
                fields.get('Microsoft.VSTS.Common.Priority', 2),
                fields.get('System.AssignedTo', {}).get('displayName', None),
                fields.get('System.CreatedBy', {}).get('displayName', 'Unknown'),
                fields.get('Microsoft.VSTS.Scheduling.StoryPoints', None),
                fields.get('System.CreatedDate'),
                fields.get('System.ChangedDate')
            ))
            count += 1
        
        self.conn.commit()
        return count
    
    def sync_full(self) -> Dict:
        """Executa sincronização completa"""
        self._start_sync('full')
        stats = {
            'projetos': 0,
            'repositorios': 0,
            'pipelines': 0,
            'pipeline_runs': 0,
            'work_items': 0
        }
        
        try:
            # 1. Sincronizar projetos
            stats['projetos'] = self.sync_projetos()
            
            # 2. Para cada projeto, sincronizar recursos
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT id, azure_project_id, nome 
                FROM projetos 
                WHERE cliente_id = %s
            """, (self.cliente_id,))
            
            projetos = cursor.fetchall()
            
            for projeto_id, azure_project_id, projeto_name in projetos:
                # Repositórios
                stats['repositorios'] += self.sync_repositorios(projeto_id, projeto_name)
                
                # Pipelines
                stats['pipelines'] += self.sync_pipelines(projeto_id, projeto_name)
                
                # Pipeline runs
                cursor.execute("""
                    SELECT id, azure_pipeline_id 
                    FROM pipelines 
                    WHERE projeto_id = %s
                """, (projeto_id,))
                
                for pipeline_db_id, azure_pipeline_id in cursor.fetchall():
                    stats['pipeline_runs'] += self.sync_pipeline_runs(
                        pipeline_db_id, projeto_name, azure_pipeline_id
                    )
                
                # Work items
                stats['work_items'] += self.sync_work_items(projeto_id, projeto_name)
            
            total = sum(stats.values())
            self._end_sync('completed', total)
            
            return stats
            
        except Exception as e:
            self._end_sync('failed', 0, str(e))
            raise


# ==================== EXEMPLO DE USO ====================

def sync_cliente(cliente_id: int):
    """Sincroniza dados de um cliente"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Conectar ao banco
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    
    # Buscar dados do cliente
    cursor = conn.cursor()
    cursor.execute("""
        SELECT azure_devops_org, azure_devops_pat_encrypted
        FROM clientes
        WHERE id = %s AND ativo = TRUE
    """, (cliente_id,))
    
    result = cursor.fetchone()
    if not result:
        print(f"Cliente {cliente_id} não encontrado ou inativo")
        return
    
    azure_org, azure_pat = result
    
    # Sincronizar
    service = AzureDevOpsSyncService(conn, cliente_id, azure_org, azure_pat)
    stats = service.sync_full()
    
    print(f"Sincronização concluída:")
    print(f"  Projetos: {stats['projetos']}")
    print(f"  Repositórios: {stats['repositorios']}")
    print(f"  Pipelines: {stats['pipelines']}")
    print(f"  Execuções: {stats['pipeline_runs']}")
    print(f"  Work Items: {stats['work_items']}")
    
    conn.close()


if __name__ == "__main__":
    # Exemplo: sincronizar cliente ID 1
    sync_cliente(1)
