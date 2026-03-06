# Template de Dados para Inventário de Aplicações

## Estrutura do Arquivo CSV

### Colunas Obrigatórias

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| Nome_Aplicacao | Texto | Nome da aplicação | Portal E-commerce |
| Produto | Texto | Produto/Squad | Vendas Online |
| Ambiente | Texto | Ambiente de execução | Produção |
| Tipo_Aplicacao | Texto | Tipo de aplicação | Web Application |
| Framework | Texto | Framework/Tecnologia | .NET Core 6.0 |
| Ferramenta_Versionamento | Texto | Git provider | Azure DevOps |
| Tipo_Pipeline | Texto | Tipo de pipeline CI/CD | YAML |
| Versao | Texto | Versão da aplicação | 6.2.1 |
| Hospedagem | Texto | Onde está hospedada | Azure App Service |
| SBOM | Texto | Possui SBOM? | Sim |
| Scan_Imagens | Texto | Faz scan de imagens? | Sim |
| Secret_Manager | Texto | Usa gerenciador de secrets? | Sim |
| SAST_SonarCube | Texto | Usa SAST/SonarCube? | Sim |
| Data_Ultima_Revisao | Data | Última revisão | 2024-11-15 |
| Data_Criacao | Data | Data de criação | 2023-01-10 |

## Valores Aceitos

### Ambiente
- Produção
- Homologação
- Desenvolvimento
- Teste (opcional)

### Tipo_Aplicacao
- Web Application
- API Rest
- Microservice
- Mobile App
- Desktop App
- API Gateway
- Batch Job
- Service Worker

### Tipo_Pipeline
- YAML
- Classic
- Não possui

### Ferramenta_Versionamento
- Azure DevOps
- GitHub
- GitLab
- Bitbucket
- AWS CodeCommit
- Outros

### Hospedagem
- Azure App Service
- Kubernetes
- AWS EC2
- AWS Lambda
- On-Premise
- Azure Functions
- Google Cloud
- Heroku
- Vercel
- Firebase

### Campos Sim/Não
Para SBOM, Scan_Imagens, Secret_Manager, SAST_SonarCube:
- Sim
- Não

### Formato de Datas
- Formato: YYYY-MM-DD
- Exemplo: 2024-12-04

## Exemplo de Linha CSV

```csv
Nome_Aplicacao,Produto,Ambiente,Tipo_Aplicacao,Framework,Ferramenta_Versionamento,Tipo_Pipeline,Versao,Hospedagem,SBOM,Scan_Imagens,Secret_Manager,SAST_SonarCube,Data_Ultima_Revisao,Data_Criacao
Portal E-commerce,Vendas Online,Produção,Web Application,.NET Core 6.0,Azure DevOps,YAML,6.2.1,Azure App Service,Sim,Sim,Sim,Sim,2024-09-15,2022-03-10
```

## Como Exportar do Excel

### 1. Preparar os Dados
- Organize suas colunas conforme a tabela acima
- Certifique-se de que as datas estão no formato correto
- Preencha todos os campos obrigatórios

### 2. Salvar como CSV
1. Arquivo → Salvar Como
2. Escolha o tipo: **CSV UTF-8 (delimitado por vírgula) (*.csv)**
3. Salve com o nome desejado

### 3. Verificar
- Abra o CSV em um editor de texto
- Confirme que os separadores são vírgulas
- Verifique o encoding (UTF-8)

## Boas Práticas

### 1. Nomenclatura
- Use nomes descritivos para aplicações
- Mantenha consistência nos nomes de produtos
- Padronize nomes de frameworks

### 2. Datas
- Sempre use o formato YYYY-MM-DD
- Mantenha as datas atualizadas
- Registre a última revisão real

### 3. Campos Booleanos
- Use apenas "Sim" ou "Não"
- Não deixe em branco (use "Não" se não aplicável)

### 4. Categorização
- Defina produtos/squads claros
- Use ambientes padronizados
- Mantenha lista de frameworks atualizada

## Validação de Dados

Antes de fazer upload, verifique:

✅ Todas as colunas obrigatórias estão presentes  
✅ Não há células vazias em campos obrigatórios  
✅ Datas estão no formato correto (YYYY-MM-DD)  
✅ Valores Sim/Não estão escritos corretamente  
✅ Não há caracteres especiais problemáticos  
✅ Encoding do arquivo é UTF-8  

## Dicas para Manutenção

### Frequência de Atualização
- **Recomendado:** Mensal
- **Mínimo:** Trimestral
- **Ideal:** Atualização automática via API

### Campos Críticos
Mantenha sempre atualizados:
- Data_Ultima_Revisao
- Versao
- Ambiente
- Práticas de segurança (SBOM, Scan, etc.)

### Auditoria
- Mantenha histórico das versões do CSV
- Registre quem fez as últimas alterações
- Documente mudanças significativas

## Exemplo Completo

Arquivo: `inventario_aplicacoes.csv` (incluído no projeto)

Este arquivo contém 50 aplicações de exemplo com dados realistas para testar o sistema.

## Importação de Outras Fontes

### Do Azure DevOps
```python
# Script de exemplo para exportar do Azure DevOps
# (implementação futura)
```

### Do JIRA
```python
# Script de exemplo para exportar do JIRA
# (implementação futura)
```

### Do ServiceNow
```python
# Script de exemplo para exportar do ServiceNow
# (implementação futura)
```

---

**Nota:** Para questões sobre a estrutura dos dados ou problemas de importação, consulte a equipe de DevOps.
