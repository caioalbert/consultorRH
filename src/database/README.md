# Database Layer - PostgreSQL

Camada de acesso a dados implementando **Repository Pattern** para PostgreSQL.

## 📁 Estrutura

```
src/database/
├── __init__.py          # Exportações e exemplo de uso
├── connection.py        # Gerenciamento de conexões (Singleton)
├── models.py            # Modelos de dados (dataclasses)
├── repositories.py      # Repositórios CRUD
└── services.py          # Camada de serviços (abstração)
```

## 🚀 Quick Start

### 1. Configurar ambiente

Crie arquivo `.env` na raiz do projeto:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=devops_hub
DB_USER=postgres
DB_PASSWORD=sua_senha
USE_POSTGRES=true
```

### 2. Executar migrations

```bash
cd migrations
python migrate.py
```

### 3. Importar dados

```bash
cd migrations/scripts
python import_csv_data.py
```

### 4. Usar no código

```python
from src.database import get_data_service

service = get_data_service()

# Obter dados como DataFrame (compatível com código existente)
df_aplicacoes = service.get_aplicacoes_df()
df_gmuds = service.get_gmuds_df()

# Ou trabalhar com objetos
aplicacoes = service.get_aplicacoes({'ambiente': 'Produção'})
```

## 📚 Componentes

### Connection (`connection.py`)

Gerencia conexões com PostgreSQL.

```python
from src.database import get_connection

db = get_connection()

# Testar conexão
if db.test_connection():
    print("Conectado!")

# Context manager para transações
with db.transaction():
    # suas operações aqui
    pass
```

### Models (`models.py`)

Dataclasses representando as entidades do banco.

- `Produto` - Produtos/sistemas
- `Aplicacao` - Aplicações do inventário
- `GMUD` - Gestão de mudanças

```python
from src.database import Aplicacao

app = Aplicacao(
    nome_aplicacao="api-test",
    ambiente="Produção",
    sbom=True
)
```

### Repositories (`repositories.py`)

Implementam operações CRUD.

**Métodos disponíveis:**
- `create()` - Criar
- `get_by_id()` - Buscar por ID
- `get_all(filters)` - Listar com filtros
- `update()` - Atualizar
- `delete()` - Deletar
- `get_stats()` - Estatísticas

```python
from src.database import get_connection, AplicacaoRepository

db = get_connection()
repo = AplicacaoRepository(db)

# Listar com filtro
apps = repo.get_all({'ambiente': 'Produção'})

# Estatísticas
stats = repo.get_stats()
```

### Services (`services.py`)

Abstração dos repositórios para uso simplificado.

```python
from src.database import get_data_service

service = get_data_service()

# Produtos
produtos = service.get_produtos()
produto = service.get_or_create_produto("NOVO")

# Aplicações
apps = service.get_aplicacoes({'ambiente': 'Produção'})
df = service.get_aplicacoes_df()  # Como DataFrame
stats = service.get_aplicacao_stats()

# GMUDs
gmuds = service.get_gmuds({'risco_operacao': 'Alto'})
df = service.get_gmuds_df()
```

## 🔍 Exemplos

Veja `examples/database_usage.py` para exemplos completos.

### Criar aplicação

```python
service = get_data_service()
produto = service.get_or_create_produto("MEU_PRODUTO")

app = Aplicacao(
    nome_aplicacao="minha-api",
    produto_id=produto.id,
    ambiente="Produção",
    sbom=True,
    scan_imagens=True
)

app_criada = service.create_aplicacao(app)
```

### Filtrar dados

```python
# Por ambiente
apps_prod = service.get_aplicacoes({'ambiente': 'Produção'})

# Por produto
produto = service.get_produto_by_nome("TOPUP")
apps = service.aplicacoes.get_by_produto(produto.id)

# GMUDs por risco
gmuds = service.get_gmuds({'risco_operacao': 'Alto'})
```

### Usar transações

```python
with service.db.transaction():
    produto = service.create_produto("TESTE")
    app = Aplicacao(produto_id=produto.id, ...)
    service.create_aplicacao(app)
    # Commit automático ou rollback em caso de erro
```

### Importação em lote

```python
aplicacoes = [Aplicacao(...), Aplicacao(...)]
count = service.bulk_create_aplicacoes(aplicacoes)
print(f"{count} aplicações criadas")
```

## 🔄 Integração com Streamlit

Modifique `data_loader.py` para suportar PostgreSQL:

```python
from config.settings import USE_POSTGRES
from src.database import get_data_service

def load_data():
    if USE_POSTGRES:
        service = get_data_service()
        return service.get_aplicacoes_df()
    else:
        # lógica CSV existente
        pass
```

## ⚡ Performance

- **Índices:** Schema inclui índices em colunas chave
- **Batch operations:** Use `bulk_create_*` para múltiplos registros
- **Transações:** Agrupe operações relacionadas
- **Cache:** Implemente cache para queries frequentes

## 🛡️ Segurança

- Usa **parametrized queries** (prevenção SQL injection)
- Suporta **transações ACID**
- **Context managers** garantem fechamento de conexões
- Validação de tipos com **dataclasses**

## 📖 Documentação Completa

Veja `docs/DATABASE_LAYER.md` para documentação detalhada.

## 🔧 Troubleshooting

### Erro de conexão

Verifique:
1. PostgreSQL está rodando
2. Credenciais corretas no `.env`
3. Database foi criado
4. Firewall permite conexão

### Tabelas não existem

Execute as migrations:
```bash
cd migrations
python migrate.py
```

### Dados não aparecem

Importe os dados:
```bash
cd migrations/scripts
python import_csv_data.py
```

## 📝 Licença

Parte do projeto DevOps Hub © 2025
