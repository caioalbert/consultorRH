# Scripts de Utilidades para Migrations

Esta pasta contém scripts utilitários para verificação e manutenção do banco de dados PostgreSQL.

## Scripts Disponíveis

### Verificação de Tabelas
- **`list_all_tables.py`** - Lista todas as tabelas do banco de dados com contagem de registros
- **`check_all_app_tables.py`** - Verifica tabelas relacionadas a aplicações/inventário
- **`check_all_gmud_tables.py`** - Verifica todas as tabelas de GMUD (fitbank, easycredio, rodobank)
- **`check_gmud_fitbank_structure.py`** - Exibe estrutura detalhada da tabela gmud_fitbank

### Verificação de Dados
- **`verify_inventory.py`** - Verifica dados do inventário de aplicações
- **`verify_gmuds.py`** - Verifica GMUDs cadastradas na tabela principal
- **`verify_all_gmuds.py`** - Verifica GMUDs em todas as tabelas com detalhes

### Testes e Resumos
- **`test_stored_procedures.py`** - Testa todas as stored procedures criadas
- **`system_summary.py`** - Gera resumo completo do sistema (aplicações, GMUDs, stored procedures)

### Execução de Migrações
- **`execute_004.py`** - Executa migração 004 (atualização para gmud_fitbank)

## Como Usar

Execute os scripts a partir da raiz do projeto:

```powershell
cd "c:\Users\jonathan.santos\Desktop\DevOps Hub\DevOpsHub"
python migrations\utils\<nome_do_script>.py
```

## Requisitos

Todos os scripts requerem:
- Arquivo `.env` configurado na raiz do projeto
- Conexão com PostgreSQL AWS RDS
- Pacotes: `psycopg2-binary`, `python-dotenv`, `pandas`
