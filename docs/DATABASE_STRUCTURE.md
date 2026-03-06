# Resumo da Estrutura de Dados PostgreSQL

## 📊 Status Atual

### Banco de Dados
- **Host**: datachapter.cuhww5f4rljb.sa-east-1.rds.amazonaws.com
- **Database**: DevOps
- **Versão**: PostgreSQL 15.12
- **Região**: sa-east-1 (AWS RDS)

### Dados Carregados
- ✅ **3 Produtos**: TOPUP, SPB, Rutas
- ✅ **35 Aplicações**: 25 em Produção, 10 em Sandbox
- ✅ **10 GMUDs**: Registros de mudanças e implantações

---

## 📁 Estrutura das Tabelas

### 1. Tabela: `produtos`
```sql
- id (INTEGER, PK, AUTO_INCREMENT)
- nome (VARCHAR, UNIQUE)
- descricao (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### 2. Tabela: `aplicacoes`
```sql
- id (INTEGER, PK, AUTO_INCREMENT)
- nome_aplicacao (VARCHAR)
- produto_id (INTEGER, FK → produtos)
- ambiente (VARCHAR) -- Produção, Sandbox, etc.
- tipo_aplicacao (VARCHAR) -- Worker, API, Web Application
- framework (VARCHAR) -- NET 6, React
- ferramenta_versionamento (VARCHAR) -- Azure Repos
- tipo_pipeline (VARCHAR) -- YAML, Classic
- versao (VARCHAR)
- hospedagem (VARCHAR) -- EKS, EC2, Cloud Run
- sbom (BOOLEAN) -- Software Bill of Materials
- scan_imagens (BOOLEAN)
- secret_manager (BOOLEAN)
- sast_sonarqube (BOOLEAN) -- Static Application Security Testing
- data_ultima_revisao (DATE)
- data_criacao (DATE)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

### 3. Tabela: `gmuds`
```sql
- id (INTEGER, PK, AUTO_INCREMENT)
- id_item (VARCHAR) -- ID do Azure DevOps/GLPI
- data_hora_prevista (TIMESTAMP)
- responsavel_executor (VARCHAR)
- tempo_estimado (VARCHAR)
- solicitante_area (VARCHAR)
- nome_aplicacao (VARCHAR) -- Nome da aplicação (campo legado)
- aplicacao_id (INTEGER, FK → aplicacoes)
- ambiente (VARCHAR)
- hostname_namespace (VARCHAR)
- local_implantacao (VARCHAR)
- build_release (TEXT) -- URL do build/release
- configuracoes_alteradas (TEXT)
- tempo_realizado (VARCHAR)
- ocorrencias (TEXT)
- solucoes_atribuidas (TEXT)
- validacoes_realizadas (TEXT)
- risco_operacao (VARCHAR) -- Baixo, Médio, Alto, Altíssimo
- impacto (TEXT)
- rca (TEXT) -- Root Cause Analysis
- controle (VARCHAR) -- Quem validou/conferiu
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

---

## 🔧 Funções PostgreSQL Disponíveis

### Produtos (7 funções)
- `fn_criar_produto(nome, descricao)` → SETOF produtos
- `fn_buscar_produto_por_id(id)` → SETOF produtos
- `fn_buscar_produto_por_nome(nome)` → SETOF produtos
- `fn_listar_produtos()` → SETOF produtos
- `fn_atualizar_produto(id, nome, descricao)` → SETOF produtos
- `fn_deletar_produto(id)` → BOOLEAN
- `fn_get_or_create_produto(nome, descricao)` → SETOF produtos

### Aplicações (9 funções)
- `fn_criar_aplicacao(...)` → SETOF aplicacoes
- `fn_buscar_aplicacao_por_id(id)` → TABLE com join de produto
- `fn_listar_aplicacoes(produto_id, ambiente, tipo_aplicacao, framework)` → TABLE
- `fn_buscar_aplicacoes_por_produto(produto_id)` → TABLE
- `fn_buscar_aplicacoes_por_ambiente(ambiente)` → TABLE
- `fn_atualizar_aplicacao(...)` → SETOF aplicacoes
- `fn_deletar_aplicacao(id)` → BOOLEAN
- `fn_obter_stats_aplicacoes()` → TABLE com estatísticas
- `fn_buscar_aplicacoes_por_termo(termo)` → TABLE

### GMUDs (7 funções)
- `fn_criar_gmud(...)` → SETOF gmuds
- `fn_buscar_gmud_por_id(id)` → SETOF gmuds
- `fn_buscar_gmud_por_id_item(id_item)` → SETOF gmuds
- `fn_listar_gmuds(aplicacao_id, risco, data_inicio, data_fim)` → SETOF gmuds
- `fn_atualizar_gmud(...)` → SETOF gmuds
- `fn_deletar_gmud(id)` → BOOLEAN
- `fn_obter_stats_gmuds()` → TABLE com estatísticas

---

## 📝 Scripts Disponíveis

### 1. Teste de Conexão
```bash
python test_connection.py
```
Valida conectividade com AWS RDS e lista tabelas/funções.

### 2. Inserir Dados Iniciais
```bash
python scripts/insert_data.py
```
Executa migration 004 para carregar dados dos CSVs.

### 3. Carregar Dados dos CSVs (alternativo)
```bash
python scripts/load_data_from_csv.py
```
Lê CSVs e usa funções fn_* para inserir dados.

### 4. Verificar Dados
```bash
python scripts/verify_data.py
```
Exibe estatísticas detalhadas dos dados carregados.

---

## 🔒 Segurança

### Indicadores de Segurança (% de aplicações)
- **SBOM**: 74.3% têm Software Bill of Materials
- **Scan de Imagens**: 65.7% fazem scan de vulnerabilidades
- **Secret Manager**: 100% usam gerenciamento de secrets
- **SAST (SonarQube)**: 34.3% têm análise estática de código

### Boas Práticas Implementadas
✅ Stored Functions para prevenir SQL Injection  
✅ Triggers automáticos para updated_at  
✅ Foreign Keys com integridade referencial  
✅ Campos NOT NULL onde apropriado  
✅ Índices em colunas-chave (nome, produto_id)  

---

## 📊 Estatísticas dos Dados

### Aplicações
- **Total**: 35 aplicações
- **Por Ambiente**:
  - Produção: 25 (71.4%)
  - Sandbox: 10 (28.6%)
- **Por Tipo**:
  - Workers: 26 (74.3%)
  - APIs: 7 (20%)
  - Web Applications: 2 (5.7%)
- **Por Hospedagem**:
  - EKS: 13 (37.1%)
  - EC2: 13 (37.1%)
  - Cloud Run: 9 (25.7%)

### GMUDs
- **Total**: 10 mudanças registradas
- **Por Risco**:
  - Alto: 6 (60%)
  - Baixo: 4 (40%)
- **Por Ambiente**:
  - Produção: 5
  - Sandbox: 4
  - Preprodução: 1

---

## 🚀 Próximos Passos

### Recomendações
1. ✅ Criar migration 003 no banco (funções PostgreSQL)
2. ✅ Executar migration 004 (dados iniciais)
3. ⏳ Implementar dashboard Streamlit usando as funções
4. ⏳ Adicionar mais GMUDs históricas dos CSVs
5. ⏳ Criar views materializadas para relatórios
6. ⏳ Implementar cache Redis para consultas frequentes
7. ⏳ Adicionar testes automatizados

### Melhorias Futuras
- [ ] Adicionar índices GIN para busca full-text
- [ ] Implementar particionamento da tabela GMUDs por data
- [ ] Criar função de auditoria (log de alterações)
- [ ] Adicionar validações de domínio (CHECK constraints)
- [ ] Implementar soft delete (deleted_at)

---

## 📚 Documentação Adicional

- **Migrations**: `migrations/README.md`
- **Funções**: `docs/STORED_PROCEDURES.md`
- **Teste de Conexão**: `docs/TEST_CONNECTION.md`
- **Estrutura do Projeto**: `docs/ESTRUTURA_PROJETO.md`

---

**Última Atualização**: 2025-12-08  
**Status**: ✅ Estrutura de dados validada e funcionando
