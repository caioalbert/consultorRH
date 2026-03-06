#!/bin/bash

# Script de setup completo do DevOps Hub
# Este script instala e configura tudo necessário para rodar o projeto

set -e  # Para em caso de erro

echo "=== Setup DevOps Hub ==="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Verificar Python
echo -e "${YELLOW}[1/7] Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 não encontrado. Instale Python 3.10+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ $PYTHON_VERSION encontrado${NC}"
echo ""

# 2. Criar ambiente virtual
echo -e "${YELLOW}[2/7] Criando ambiente virtual...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓ Ambiente virtual criado${NC}"
else
    echo -e "${GREEN}✓ Ambiente virtual já existe${NC}"
fi
echo ""

# 3. Ativar ambiente virtual e instalar dependências
echo -e "${YELLOW}[3/7] Instalando dependências Python...${NC}"
source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✓ Dependências instaladas${NC}"
echo ""

# 4. Verificar PostgreSQL
echo -e "${YELLOW}[4/7] Verificando PostgreSQL...${NC}"
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}PostgreSQL não encontrado. Instalando...${NC}"
    sudo apt update -qq
    sudo apt install postgresql postgresql-contrib -y -qq
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    echo -e "${GREEN}✓ PostgreSQL instalado e iniciado${NC}"
else
    echo -e "${GREEN}✓ PostgreSQL já instalado${NC}"
    # Garantir que está rodando
    sudo systemctl start postgresql 2>/dev/null || true
fi
echo ""

# 5. Criar banco de dados e usuário
echo -e "${YELLOW}[5/7] Configurando banco de dados...${NC}"
sudo -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname='devops_hub'" | grep -q 1 || \
sudo -u postgres psql << EOF
CREATE DATABASE devops_hub;
CREATE USER devops_user WITH PASSWORD 'devops123';
GRANT ALL PRIVILEGES ON DATABASE devops_hub TO devops_user;
ALTER DATABASE devops_hub OWNER TO devops_user;
EOF
echo -e "${GREEN}✓ Banco de dados configurado${NC}"
echo ""

# 6. Executar migrations
echo -e "${YELLOW}[6/7] Executando migrations...${NC}"
cd migrations
python migrate.py
cd ..
echo -e "${GREEN}✓ Migrations aplicadas${NC}"
echo ""

# 7. Importar dados (se existirem CSVs)
echo -e "${YELLOW}[7/7] Verificando dados para importar...${NC}"
if [ -f "data/inventario_aplicacoes.csv" ]; then
    echo "Importando dados dos CSVs..."
    cd migrations/scripts
    python import_csv_data.py
    cd ../..
    echo -e "${GREEN}✓ Dados importados${NC}"
else
    echo -e "${YELLOW}⚠ Nenhum CSV encontrado em data/. Pulando importação.${NC}"
fi
echo ""

# Finalização
echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}✓ Setup concluído com sucesso!${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""
echo "Para iniciar a aplicação:"
echo -e "${YELLOW}  source .venv/bin/activate${NC}"
echo -e "${YELLOW}  streamlit run app.py${NC}"
echo ""
echo "Ou simplesmente:"
echo -e "${YELLOW}  ./run.sh${NC}"
