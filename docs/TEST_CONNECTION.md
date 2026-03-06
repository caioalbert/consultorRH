# Script de Teste de Conexão - DevOps Hub

## 🎯 Objetivo
Testar a conectividade com o banco de dados PostgreSQL na AWS RDS.

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **Dependências instaladas**:
```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Criar arquivo .env

Copie o arquivo de exemplo e configure suas credenciais:

```bash
cp .env.example .env
```

### 2. Editar .env com suas credenciais

Abra o arquivo `.env` e preencha a senha:

```env
DB_HOST=datachapter.cuhww5f4rljb.sa-east-1.rds.amazonaws.com
DB_PORT=5432
DB_NAME=DevOps
DB_USER=jonathan.santos
DB_PASSWORD=SUA_SENHA_AQUI  # ← PREENCHA AQUI
```

> ⚠️ **IMPORTANTE**: O arquivo `.env` está no `.gitignore` e nunca será commitado.

## 🚀 Executar Teste

```bash
python test_connection.py
```

## 📊 O que o script testa

1. ✅ **Carregamento de configurações** do arquivo .env
2. ✅ **Conexão com o banco** de dados RDS
3. ✅ **Versão do PostgreSQL** instalada
4. ✅ **Tabelas existentes** no banco
5. ✅ **Funções PostgreSQL** (fn_*) disponíveis
6. ✅ **Informações da conexão** (database, user, server)

## 📝 Exemplo de Saída

```
======================================================================
  TESTE DE CONEXÃO - PostgreSQL AWS RDS
======================================================================

ℹ Carregando configurações do arquivo .env...
✓ Configurações carregadas com sucesso
ℹ Tentando conectar ao banco de dados...
  Host: datachapter.cuhww5f4rljb.sa-east-1.rds.amazonaws.com
  Database: DevOps
  User: jonathan.santos
  Port: 5432

✓ Conexão estabelecida com sucesso!
✓ PostgreSQL Version: PostgreSQL 15.4 on x86_64-pc-linux-gnu

ℹ Verificando tabelas existentes...
✓ Tabelas encontradas: 3
  - aplicacoes
  - gmuds
  - produtos

Verificando funções PostgreSQL...
✓ Funções encontradas: 23
  - fn_criar_produto (2 parâmetros)
  - fn_buscar_produto_por_id (1 parâmetros)
  ...

Informações da Conexão:
  Database: DevOps
  User: jonathan.santos
  Server: 172.31.xx.xx:5432

======================================================================
  TESTE CONCLUÍDO COM SUCESSO! ✓
======================================================================
```

## ❌ Possíveis Erros

### Erro: "Configurações faltando no .env"
**Solução**: Verifique se o arquivo `.env` existe e contém todas as variáveis necessárias.

### Erro: "Erro de conexão: could not connect to server"
**Possíveis causas**:
1. **Credenciais incorretas** - Verifique usuário/senha
2. **Firewall/Security Group** - Verifique se seu IP está liberado no AWS RDS
3. **Host ou porta incorretos** - Verifique o endpoint do RDS
4. **Banco de dados não existe** - Verifique o nome do database

### Erro: "timeout"
**Solução**: Verifique a configuração de Security Group do RDS e certifique-se de que a porta 5432 está liberada para seu IP.

## 🔒 Segurança

- ✅ Arquivo `.env` está no `.gitignore`
- ✅ Credenciais nunca são commitadas
- ✅ Use `.env.example` como template
- ✅ Nunca compartilhe o arquivo `.env`

## 📚 Próximos Passos

Após teste bem-sucedido:
1. Execute as migrations: `python migrations/migrate.py`
2. Execute o script de importação de dados (se necessário)
3. Inicie a aplicação: `streamlit run app.py`
