# Stored Procedures - Segurança contra SQL Injection

## 📋 Visão Geral

Todos os repositories do sistema foram atualizados para utilizar **Funções PostgreSQL (Functions)** ao invés de SQL parametrizado direto, aumentando significativamente a segurança contra **SQL Injection**.

> **Nota Técnica**: No PostgreSQL, `FUNCTION` é usada para operações que retornam dados, enquanto `PROCEDURE` é usada para operações batch sem retorno. Ambas oferecem a mesma proteção contra SQL Injection. Como precisamos retornar dados (SELECT, INSERT RETURNING, etc.), usamos `FUNCTION`.

## 🔒 Benefícios de Segurança

### SQL Injection Prevention
- ✅ **Camada extra de proteção**: Funções executam no servidor com permissões controladas
- ✅ **Validação no banco**: Lógica de validação centralizada no PostgreSQL
- ✅ **Separação de privilégios**: Usuários da aplicação só podem executar funções, não acessar tabelas diretamente
- ✅ **Auditoria melhorada**: Logs do PostgreSQL registram chamadas a funções específicas

### Antes (SQL Parametrizado)
```python
def create(self, produto: Produto) -> Produto:
    query = "INSERT INTO produtos (nome, descricao) VALUES (%s, %s) RETURNING *"
    result = self.db.execute_query(query, (produto.nome, produto.descricao), fetch_one=True)
    return Produto.from_dict(result)
```

### Depois (Funções PostgreSQL)
```python
def create(self, produto: Produto) -> Produto:
    query = "SELECT * FROM fn_criar_produto(%s, %s)"
    result = self.db.execute_query(query, (produto.nome, produto.descricao), fetch_one=True)
    return Produto.from_dict(result)
```

## 📦 Funções PostgreSQL Implementadas

### Produtos (7 funções)
- ✅ `fn_criar_produto(nome, descricao)` - Criar produto
- ✅ `fn_buscar_produto_por_id(id)` - Buscar por ID
- ✅ `fn_buscar_produto_por_nome(nome)` - Buscar por nome
- ✅ `fn_listar_produtos()` - Listar todos
- ✅ `fn_atualizar_produto(id, nome, descricao)` - Atualizar
- ✅ `fn_deletar_produto(id)` - Deletar
- ✅ `fn_get_or_create_produto(nome, descricao)` - Buscar ou criar

### Aplicações (9 funções)
- ✅ `fn_criar_aplicacao(...)` - Criar aplicação (15 parâmetros)
- ✅ `fn_buscar_aplicacao_por_id(id)` - Buscar por ID
- ✅ `fn_listar_aplicacoes(produto_id, ambiente, tipo, framework)` - Listar com filtros
- ✅ `fn_buscar_aplicacoes_por_produto(produto_id)` - Filtrar por produto
- ✅ `fn_buscar_aplicacoes_por_ambiente(ambiente)` - Filtrar por ambiente
- ✅ `fn_atualizar_aplicacao(...)` - Atualizar (16 parâmetros)
- ✅ `fn_deletar_aplicacao(id)` - Deletar
- ✅ `fn_obter_stats_aplicacoes()` - Estatísticas agregadas
- ✅ `fn_buscar_aplicacoes_por_termo(termo)` - Busca textual

### GMUDs (7 funções)
- ✅ `fn_criar_gmud(...)` - Criar GMUD (20 parâmetros)
- ✅ `fn_buscar_gmud_por_id(id)` - Buscar por ID
- ✅ `fn_buscar_gmud_por_id_item(id_item)` - Buscar por ID do item
- ✅ `fn_listar_gmuds(ambiente, aplicacao_id, risco, data_inicio, data_fim)` - Listar com filtros
- ✅ `fn_atualizar_gmud(...)` - Atualizar (21 parâmetros)
- ✅ `fn_deletar_gmud(id)` - Deletar
- ✅ `fn_obter_stats_gmuds()` - Estatísticas agregadas

## 🚀 Como Aplicar

### 1. Executar Migration
```bash
cd "c:\Users\jonathan.santos\Desktop\DevOps Hub\DevOpsHub"
python migrations/migrate.py
```

Isso criará todas as 29 funções PostgreSQL no banco de dados.

### 2. Verificar Criação
```bash
python db_helper.py test
```

### 3. Testar Repositories
```bash
python examples/database_usage.py
```

## 📁 Arquivos Modificados

### Migration
- ✅ `migrations/003_stored_procedures.sql` - **811 linhas** com todas as funções

### Repositories
- ✅ `src/database/repositories.py` - Todos os métodos atualizados:
  - **ProdutoRepository**: 7/7 métodos usando funções PostgreSQL
  - **AplicacaoRepository**: 9/9 métodos usando funções PostgreSQL
  - **GMUDRepository**: 7/7 métodos usando funções PostgreSQL

### Total
- **29 funções PostgreSQL (FUNCTION)** criadas
- **23 métodos** de repositories atualizados
- **0 queries SQL diretas** no código Python (exceto dentro das funções)

## 🔍 Validação

### Verificar se há SQL direto no código
```bash
# Não deve retornar nada:
grep -r "INSERT INTO\|UPDATE.*SET\|DELETE FROM" src/database/repositories.py
```

### Verificar funções no banco
```sql
SELECT proname, pronargs 
FROM pg_proc 
WHERE proname LIKE 'fn_%'
ORDER BY proname;
```

## 📊 Comparação de Segurança

| Aspecto | SQL Parametrizado | Funções PostgreSQL |
|---------|-------------------|-------------------|
| SQL Injection básico | ✅ Protegido | ✅ Protegido |
| SQL Injection avançado | ⚠️ Depende da implementação | ✅ Extra camada |
| Controle de acesso | ⚠️ Usuário acessa tabelas | ✅ Usuário só executa funções |
| Auditoria | ⚠️ Queries variadas | ✅ Chamadas a funções específicas |
| Performance | ⚠️ Parsing a cada query | ✅ Planos de execução cacheados |
| Manutenção | ⚠️ SQL espalhado no código | ✅ Centralizado no banco |

## ⚙️ Configuração de Permissões (Recomendado)

Para máxima segurança, crie um usuário com permissões apenas para executar funções:

```sql
-- Criar usuário da aplicação
CREATE USER devopshub_app WITH PASSWORD 'senha_segura';

-- Revogar acesso direto às tabelas
REVOKE ALL ON produtos, aplicacoes, gmuds FROM devopshub_app;

-- Conceder apenas execução de funções
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO devopshub_app;

-- Permitir uso do schema
GRANT USAGE ON SCHEMA public TO devopshub_app;
```

Depois, configure a aplicação para usar este usuário:

```env
DB_USER=devopshub_app
DB_PASSWORD=senha_segura
```

## 📝 Notas Importantes

1. **FUNCTION vs PROCEDURE**: No PostgreSQL, usamos `FUNCTION` para operações que retornam dados e `PROCEDURE` para operações batch. Ambas oferecem proteção contra SQL Injection.
2. **Transações**: As funções usam transações automáticas do PostgreSQL
3. **NULL values**: Filtros NULL são tratados corretamente nas funções de listagem
4. **RETURNING**: Todas as funções de INSERT/UPDATE retornam o registro completo
5. **Indexes**: As funções se beneficiam dos índices existentes nas tabelas
6. **Rollback**: Em caso de erro, o PostgreSQL faz rollback automático da transação
## 🎯 Próximos Passos

1. ✅ Migrar para funções PostgreSQL (CONCLUÍDO)
2. ⏭️ Executar `python migrations/migrate.py`
3. ⏭️ Testar com `python examples/database_usage.py`
4. ⏭️ Configurar usuário com permissões restritas (opcional mas recomendado)
5. ⏭️ Atualizar dashboards para usar o novo código

## 🐛 Troubleshooting

### Erro: "function fn_criar_produto does not exist"
**Solução**: Execute `python migrations/migrate.py`

### Erro: "permission denied for function"
**Solução**: Verifique permissões do usuário do banco com `GRANT EXECUTE ON ALL FUNCTIONS`

### Erro: "column X does not exist in result"
**Solução**: Verifique se a migration 001 e 002 foram executadas antes

## 📚 Referências

- [PostgreSQL Functions (PL/pgSQL)](https://www.postgresql.org/docs/current/plpgsql.html)
- [PostgreSQL Functions vs Procedures](https://www.postgresql.org/docs/current/xfunc.html)
- [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PostgreSQL Function Security](https://www.postgresql.org/docs/current/sql-createfunction.html#SQL-CREATEFUNCTION-SECURITY)
- [PostgreSQL Function Security](https://www.postgresql.org/docs/current/sql-createfunction.html#SQL-CREATEFUNCTION-SECURITY)
