"""
Cliente para Azure DevOps REST API
Coleta dados de projetos, pipelines, repositórios, etc.
"""
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import base64


class AzureDevOpsClient:
    """Cliente para interagir com Azure DevOps API"""
    
    def __init__(self, organization: str, personal_access_token: str):
        """
        Inicializa cliente Azure DevOps
        
        Args:
            organization: Nome da organização no Azure DevOps
            personal_access_token: PAT com permissões de leitura
        """
        self.organization = organization
        self.base_url = f"https://dev.azure.com/{organization}"
        self.vsrm_url = f"https://vsrm.dev.azure.com/{organization}"
        
        # Autenticação via PAT
        auth_string = f":{personal_access_token}"
        encoded = base64.b64encode(auth_string.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json"
        }
    
    def _get(self, url: str, params: Dict = None) -> Dict:
        """Faz requisição GET"""
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    # ==================== PROJETOS ====================
    
    def get_projects(self) -> List[Dict]:
        """Lista todos os projetos da organização"""
        url = f"{self.base_url}/_apis/projects?api-version=7.0"
        data = self._get(url)
        return data.get('value', [])
    
    def get_project(self, project_id: str) -> Dict:
        """Obtém detalhes de um projeto específico"""
        url = f"{self.base_url}/_apis/projects/{project_id}?api-version=7.0"
        return self._get(url)
    
    # ==================== REPOSITÓRIOS ====================
    
    def get_repositories(self, project: str) -> List[Dict]:
        """Lista repositórios de um projeto"""
        url = f"{self.base_url}/{project}/_apis/git/repositories?api-version=7.0"
        data = self._get(url)
        return data.get('value', [])
    
    def get_repository_stats(self, project: str, repo_id: str) -> Dict:
        """Obtém estatísticas de um repositório"""
        url = f"{self.base_url}/{project}/_apis/git/repositories/{repo_id}/stats/branches?api-version=7.0"
        return self._get(url)
    
    # ==================== PIPELINES ====================
    
    def get_pipelines(self, project: str) -> List[Dict]:
        """Lista pipelines de um projeto"""
        url = f"{self.base_url}/{project}/_apis/pipelines?api-version=7.0"
        data = self._get(url)
        return data.get('value', [])
    
    def get_pipeline_runs(self, project: str, pipeline_id: int, 
                         days: int = 30) -> List[Dict]:
        """
        Lista execuções de um pipeline
        
        Args:
            project: Nome do projeto
            pipeline_id: ID do pipeline
            days: Número de dias para buscar histórico
        """
        url = f"{self.base_url}/{project}/_apis/pipelines/{pipeline_id}/runs?api-version=7.0"
        data = self._get(url)
        return data.get('value', [])
    
    def get_pipeline_run_details(self, project: str, pipeline_id: int, 
                                 run_id: int) -> Dict:
        """Obtém detalhes de uma execução específica"""
        url = f"{self.base_url}/{project}/_apis/pipelines/{pipeline_id}/runs/{run_id}?api-version=7.0"
        return self._get(url)
    
    # ==================== BUILDS ====================
    
    def get_builds(self, project: str, days: int = 30) -> List[Dict]:
        """Lista builds recentes"""
        min_time = (datetime.now() - timedelta(days=days)).isoformat()
        url = f"{self.base_url}/{project}/_apis/build/builds?api-version=7.0"
        params = {"minTime": min_time}
        data = self._get(url, params)
        return data.get('value', [])
    
    def get_build_details(self, project: str, build_id: int) -> Dict:
        """Obtém detalhes de um build"""
        url = f"{self.base_url}/{project}/_apis/build/builds/{build_id}?api-version=7.0"
        return self._get(url)
    
    # ==================== RELEASES ====================
    
    def get_releases(self, project: str) -> List[Dict]:
        """Lista releases de um projeto"""
        url = f"{self.vsrm_url}/{project}/_apis/release/releases?api-version=7.0"
        data = self._get(url)
        return data.get('value', [])
    
    def get_release_definitions(self, project: str) -> List[Dict]:
        """Lista definições de release"""
        url = f"{self.vsrm_url}/{project}/_apis/release/definitions?api-version=7.0"
        data = self._get(url)
        return data.get('value', [])
    
    # ==================== WORK ITEMS ====================
    
    def get_work_items_by_query(self, project: str, wiql: str) -> List[Dict]:
        """
        Busca work items usando WIQL (Work Item Query Language)
        
        Exemplo de WIQL:
        SELECT [System.Id], [System.Title], [System.State]
        FROM WorkItems
        WHERE [System.TeamProject] = @project
        AND [System.State] <> 'Closed'
        """
        url = f"{self.base_url}/{project}/_apis/wit/wiql?api-version=7.0"
        response = requests.post(url, headers=self.headers, json={"query": wiql})
        response.raise_for_status()
        data = response.json()
        
        # Obter detalhes dos work items
        work_item_ids = [item['id'] for item in data.get('workItems', [])]
        if not work_item_ids:
            return []
        
        return self.get_work_items(work_item_ids)
    
    def get_work_items(self, ids: List[int]) -> List[Dict]:
        """Obtém detalhes de múltiplos work items"""
        ids_str = ','.join(map(str, ids))
        url = f"{self.base_url}/_apis/wit/workitems?ids={ids_str}&api-version=7.0"
        data = self._get(url)
        return data.get('value', [])
    
    def get_active_work_items(self, project: str) -> List[Dict]:
        """Obtém work items ativos (não fechados)"""
        wiql = f"""
        SELECT [System.Id], [System.Title], [System.State], [System.WorkItemType]
        FROM WorkItems
        WHERE [System.TeamProject] = '{project}'
        AND [System.State] <> 'Closed'
        AND [System.State] <> 'Removed'
        """
        return self.get_work_items_by_query(project, wiql)
    
    # ==================== MÉTRICAS AGREGADAS ====================
    
    def get_project_summary(self, project: str) -> Dict:
        """Obtém resumo completo de um projeto"""
        summary = {
            'project': project,
            'repositories': [],
            'pipelines': [],
            'recent_builds': [],
            'active_work_items': [],
            'metrics': {}
        }
        
        # Repositórios
        repos = self.get_repositories(project)
        summary['repositories'] = repos
        summary['metrics']['total_repositories'] = len(repos)
        
        # Pipelines
        pipelines = self.get_pipelines(project)
        summary['pipelines'] = pipelines
        summary['metrics']['total_pipelines'] = len(pipelines)
        
        # Builds recentes (últimos 7 dias)
        builds = self.get_builds(project, days=7)
        summary['recent_builds'] = builds
        summary['metrics']['builds_last_7_days'] = len(builds)
        
        # Calcular taxa de sucesso
        if builds:
            successful = sum(1 for b in builds if b.get('result') == 'succeeded')
            summary['metrics']['build_success_rate'] = (successful / len(builds)) * 100
        
        # Work items ativos
        work_items = self.get_active_work_items(project)
        summary['active_work_items'] = work_items
        summary['metrics']['active_work_items'] = len(work_items)
        
        return summary
    
    def get_organization_summary(self) -> Dict:
        """Obtém resumo de toda a organização"""
        projects = self.get_projects()
        
        summary = {
            'organization': self.organization,
            'total_projects': len(projects),
            'projects': []
        }
        
        for project in projects:
            project_name = project['name']
            try:
                project_summary = self.get_project_summary(project_name)
                summary['projects'].append(project_summary)
            except Exception as e:
                print(f"Erro ao processar projeto {project_name}: {e}")
        
        return summary


# ==================== EXEMPLO DE USO ====================

def example_usage():
    """Exemplo de como usar o cliente"""
    
    # Inicializar cliente
    client = AzureDevOpsClient(
        organization="sua-organizacao",
        personal_access_token="seu-pat-aqui"
    )
    
    # Listar projetos
    projects = client.get_projects()
    print(f"Projetos encontrados: {len(projects)}")
    
    for project in projects:
        print(f"\nProjeto: {project['name']}")
        
        # Repositórios
        repos = client.get_repositories(project['name'])
        print(f"  Repositórios: {len(repos)}")
        
        # Pipelines
        pipelines = client.get_pipelines(project['name'])
        print(f"  Pipelines: {len(pipelines)}")
        
        # Builds recentes
        builds = client.get_builds(project['name'], days=7)
        print(f"  Builds (7 dias): {len(builds)}")
        
        if builds:
            successful = sum(1 for b in builds if b.get('result') == 'succeeded')
            success_rate = (successful / len(builds)) * 100
            print(f"  Taxa de sucesso: {success_rate:.1f}%")


if __name__ == "__main__":
    example_usage()
