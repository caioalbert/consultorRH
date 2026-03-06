#!/bin/bash

echo "🚀 Iniciando ComplianceHR..."
echo ""

cd "$(dirname "$0")"

# Ativa venv se existir
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Instala dependências se necessário
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install streamlit pandas
fi

echo "✅ Iniciando aplicação..."
streamlit run app.py
