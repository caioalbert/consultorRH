# Migrations para PostgreSQL - DevOps Hub

Este diretório contém as migrations do banco de dados PostgreSQL.

## Estrutura

```
migrations/
├── 001_initial_schema.sql      # Schema inicial do banco
├── 002_seed_data.sql            # Dados iniciais (seed)
├── migrate.py                   # Script para executar migrations
└── scripts/
    └── import_csv_data.py       # Script para importar dados dos CSVs
```

## Pré-requisitos

1. PostgreSQL instalado e rodando
2. Criar o banco de dados:
```sql
CREATE DATABASE devops_hub;
```

3. Instalar dependências Python:
```bash
pip install psycopg2-binary pandas
```

## Variáveis de Ambiente

Configure as seguintes variáveis de ambiente (ou use os valores padrão):

```bash
DB_HOST=localhost        # default: localhost
DB_PORT=5432            # default: 5432
DB_NAME=devops_hub      # default: devops_hub
DB_USER=postgres        # default: postgres
DB_PASSWORD=sua_senha   # default: (vazio)
```

## Como usar

### 1. Executar todas as migrations

```bash
cd migrations
python migrate.py
```

Este comando irá:
- Criar a tabela de controle `schema_migrations`
- Aplicar todas as migrations pendentes em ordem
- Registrar cada migration aplicada

### 2. Importar dados dos CSVs

Após aplicar as migrations, importe os dados:

```bash
cd migrations/scripts
python import_csv_data.py
```

Este script irá:
- Importar produtos únicos
- Importar todas as aplicações do inventário
- Importar todas as GMUDs
- Criar relacionamentos entre aplicações e produtos

### 3. Verificar migrations aplicadas

Execute novamente o migrate.py para ver quais migrations já foram aplicadas:

```bash
python migrate.py
```

## Schema do Banco de Dados

### Tabela: produtos
- `id`: Primary key
- `nome`: Nome único do produto
- `descricao`: Descrição do produto
- `created_at`, `updated_at`: Timestamps

### Tabela: aplicacoes
- `id`: Primary key
- `nome_aplicacao`: Nome da aplicação
- `produto_id`: Foreign key para produtos
- `ambiente`: Produção, Sandbox, N/A
- `tipo_aplicacao`: API, Worker, Web Application
- `framework`: NET 6, React, etc.
- `ferramenta_versionamento`: Azure Repos, GitHub, etc.
- `tipo_pipeline`: YAML, Classic
- `versao`: Versão da aplicação
- `hospedagem`: EKS, EC2, Cloud Run, Windows
- `sbom`: Boolean - SBOM implementado
- `scan_imagens`: Boolean - Scan de imagens ativo
- `secret_manager`: Boolean - Secret Manager configurado
- `sast_sonarqube`: Boolean - SAST/SonarCube ativo
- `data_ultima_revisao`: Data da última revisão
- `data_criacao`: Data de criação
- `created_at`, `updated_at`: Timestamps

**Constraint**: UNIQUE (nome_aplicacao, ambiente)

### Tabela: gmuds
- `id`: Primary key
- `id_item`: ID único do item (Azure DevOps/GLPI)
- `data_hora_prevista`: Data/hora prevista da mudança
- `responsavel_executor`: Responsável pela execução
- `tempo_estimado`: Tempo estimado
- `solicitante_area`: Solicitante/área
- `nome_aplicacao`: Nome da aplicação
- `aplicacao_id`: Foreign key para aplicacoes
- `ambiente`: Ambiente da mudança
- `hostname_namespace`: Hostname ou namespace
- `local_implantacao`: Local de implantação
- `build_release`: Link do build/release
- `configuracoes_alteradas`: Configurações alteradas
- `tempo_realizado`: Tempo realizado
- `ocorrencias`: Ocorrências durante a mudança
- `solucoes_atribuidas`: Soluções aplicadas
- `validacoes_realizadas`: Validações realizadas
- `risco_operacao`: Risco da operação
- `impacto`: Impacto da mudança
- `rca`: Root Cause Analysis
- `controle`: Controle/conferência
- `created_at`, `updated_at`: Timestamps

## Índices

Índices criados para otimizar consultas:
- `idx_aplicacoes_produto`: Busca por produto
- `idx_aplicacoes_ambiente`: Busca por ambiente
- `idx_aplicacoes_nome`: Busca por nome de aplicação
- `idx_gmuds_aplicacao`: Busca GMUDs por aplicação
- `idx_gmuds_ambiente`: Busca GMUDs por ambiente
- `idx_gmuds_data`: Busca GMUDs por data

## Triggers

Triggers automáticos para atualizar `updated_at`:
- `update_produtos_updated_at`
- `update_aplicacoes_updated_at`
- `update_gmuds_updated_at`

## Próximos Passos

Após executar as migrations e importar os dados:

1. Atualizar o `data_loader.py` para usar PostgreSQL
2. Criar um arquivo `.env` com as credenciais do banco
3. Implementar camada de acesso a dados (repository pattern)
4. Adicionar cache para consultas frequentes
5. Implementar backup automático do banco

## Troubleshooting

### Erro de conexão
- Verifique se o PostgreSQL está rodando
- Verifique as credenciais e variáveis de ambiente
- Confirme que o banco `devops_hub` foi criado

### Erro de import
- Verifique se os arquivos CSV estão no diretório `data/`
- Confirme que as migrations foram aplicadas antes do import
- Verifique os logs de erro para detalhes específicos

### Recriar o banco do zero
```sql
DROP DATABASE IF EXISTS devops_hub;
CREATE DATABASE devops_hub;
```

Depois execute:
```bash
python migrate.py
python scripts/import_csv_data.py
```
