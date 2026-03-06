# Camada de Acesso a Dados - PostgreSQL

## 📋 Visão Geral

Esta camada implementa o padrão **Repository Pattern** para acesso aos dados do PostgreSQL, oferecendo uma abstração completa e type-safe para operações no banco de dados.

## 🏗️ Arquitetura

```
src/database/
├── __init__.py          # Exportações públicas
├── connection.py        # Gerenciamento de conexões
├── models.py            # Modelos de dados (dataclasses)
├── repositories.py      # Repositórios (CRUD operations)
└── services.py          # Serviços de negócio
```

## 🔧 Componentes

### 1. Connection (`connection.py`)

Gerencia conexões com PostgreSQL usando padrão Singleton.

**Principais recursos:**
- Pool de conexões
- Context manager para transações
- Suporte a cursors customizados (RealDictCursor)
- Tratamento de erros

**Exemplo:**
```python
from src.database import get_connection

db = get_connection()

# Testar conexão
if db.test_connection():
    print("Conectado!")

# Usar transação
with db.transaction():
    # operações do banco
    pass
```

### 2. Models (`models.py`)

Define os modelos de dados usando `dataclasses`.

**Modelos disponíveis:**
- `Produto` - Produtos/sistemas
- `Aplicacao` - Aplicações do inventário
- `GMUD` - Gestão de mudanças

**Exemplo:**
```python
from src.database.models import Aplicacao

app = Aplicacao(
    nome_aplicacao="API-Payments",
    ambiente="Produção",
    sbom=True,
    scan_imagens=True
)
```

### 3. Repositories (`repositories.py`)

Implementam operações CRUD para cada entidade.

**Repositórios:**
- `ProdutoRepository`
- `AplicacaoRepository`
- `GMUDRepository`

**Métodos comuns:**
- `create()` - Criar registro
- `get_by_id()` - Buscar por ID
- `get_all()` - Listar todos (com filtros)
- `update()` - Atualizar registro
- `delete()` - Deletar registro
- `get_stats()` - Estatísticas

**Exemplo:**
```python
from src.database import get_connection, AplicacaoRepository

db = get_connection()
repo = AplicacaoRepository(db)

# Criar
app = Aplicacao(nome_aplicacao="Test", ambiente="Dev")
nova_app = repo.create(app)

# Buscar
apps = repo.get_all({'ambiente': 'Produção'})

# Estatísticas
stats = repo.get_stats()
print(f"Total: {stats['total_aplicacoes']}")
```

### 4. Services (`services.py`)

Camada de abstração para simplificar o uso dos repositórios.

**Classe principal:** `DataService`

**Exemplo:**
```python
from src.database.services import get_data_service

service = get_data_service()

# Buscar ou criar produto
produto = service.get_or_create_produto("TOPUP")

# Obter aplicações como DataFrame
df = service.get_aplicacoes_df({'ambiente': 'Produção'})

# Estatísticas
stats = service.get_aplicacao_stats()
```

## 🚀 Como Usar

### Passo 1: Configurar Banco de Dados

1. Instale PostgreSQL
2. Crie o banco de dados:
```sql
CREATE DATABASE devops_hub;
```

3. Configure as variáveis de ambiente (`.env`):
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=devops_hub
DB_USER=postgres
DB_PASSWORD=sua_senha
```

### Passo 2: Executar Migrations

```bash
cd migrations
python migrate.py
```

### Passo 3: Importar Dados dos CSVs

```bash
cd migrations/scripts
python import_csv_data.py
```

### Passo 4: Usar na Aplicação

```python
from src.database.services import get_data_service

# Inicializar serviço
service = get_data_service()

# Obter dados
aplicacoes = service.get_aplicacoes()
gmuds = service.get_gmuds({'ambiente': 'Produção'})

# Usar como DataFrame (compatível com código existente)
df_apps = service.get_aplicacoes_df()
df_gmuds = service.get_gmuds_df()
```

## 📊 Integração com Streamlit

Para usar os dados do PostgreSQL no Streamlit, modifique o `data_loader.py`:

```python
from src.database.services import get_data_service

class InventoryDataLoader:
    def __init__(self, use_postgres=False):
        self.use_postgres = use_postgres
        if use_postgres:
            self.service = get_data_service()
    
    def load_data(self) -> pd.DataFrame:
        if self.use_postgres:
            return self.service.get_aplicacoes_df()
        else:
            # Lógica atual do CSV
            pass
```

## 🔍 Exemplos de Consultas

### Buscar aplicações por produto
```python
service = get_data_service()
produto = service.get_produto_by_nome("TOPUP")
apps = service.aplicacoes.get_by_produto(produto.id)
```

### Filtrar GMUDs por período
```python
from datetime import datetime

inicio = datetime(2025, 11, 1)
fim = datetime(2025, 11, 30)
gmuds = service.gmuds.get_by_periodo(inicio, fim)
```

### Buscar aplicações com segurança completa
```python
repo = AplicacaoRepository(db)
query = """
    SELECT * FROM aplicacoes
    WHERE sbom = true
      AND scan_imagens = true
      AND secret_manager = true
      AND sast_sonarqube = true
"""
results = db.execute_query(query)
```

## ⚡ Performance

### Transações em Lote
```python
service = get_data_service()

# Criar múltiplas aplicações
aplicacoes = [Aplicacao(...), Aplicacao(...)]
count = service.bulk_create_aplicacoes(aplicacoes)
```

### Índices
O schema já inclui índices para:
- `produto_id`
- `ambiente`
- `nome_aplicacao`
- `data_hora_prevista`

### Cache
Implemente cache com decorators:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_produtos_cached():
    return service.get_produtos()
```

## 🛡️ Tratamento de Erros

```python
try:
    service = get_data_service()
    app = service.create_aplicacao(aplicacao)
except ConnectionError as e:
    print(f"Erro de conexão: {e}")
except Exception as e:
    print(f"Erro: {e}")
finally:
    service.close()
```

## 📝 Boas Práticas

1. **Use transações** para operações múltiplas
2. **Feche conexões** quando não estiver usando
3. **Use filtros** em vez de trazer todos os dados
4. **Implemente cache** para queries frequentes
5. **Valide dados** antes de inserir

## 🔄 Migração CSV → PostgreSQL

Para migrar gradualmente do CSV para PostgreSQL:

1. **Fase 1:** Configure PostgreSQL e importe dados
2. **Fase 2:** Adicione flag `USE_POSTGRES` nas settings
3. **Fase 3:** Modifique `data_loader.py` para suportar ambos
4. **Fase 4:** Teste em paralelo
5. **Fase 5:** Remova código CSV quando estável

## 📚 Referências

- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Don%27t_Do_This)
