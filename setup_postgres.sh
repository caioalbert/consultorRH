#!/bin/bash

echo "🐘 Setup PostgreSQL para ConsultorRH"
echo ""

# Verifica se PostgreSQL está instalado
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL não encontrado"
    echo "Instale com: sudo apt install postgresql postgresql-contrib"
    exit 1
fi

echo "✓ PostgreSQL encontrado"
echo ""

# Cria banco de dados
echo "📦 Criando banco de dados 'consultorrh'..."
sudo -u postgres psql -c "CREATE DATABASE consultorrh;" 2>/dev/null || echo "Banco já existe"

# Cria usuário (opcional)
echo "👤 Configurando usuário postgres..."
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';" 2>/dev/null

echo ""
echo "✅ PostgreSQL configurado!"
echo ""
echo "📝 Configure o arquivo .env:"
echo "   cp .env.example .env"
echo ""
echo "🚀 Instale dependências e inicie:"
echo "   pip install -r requirements.txt"
echo "   python3 populate_db.py"
echo "   streamlit run app.py"
