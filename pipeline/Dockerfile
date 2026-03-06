# Multi-stage build para aplicação Streamlit
FROM python:3.12-slim AS builder

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências Python
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# Stage final
FROM python:3.12-slim

WORKDIR /app

# Copia dependências do builder
COPY --from=builder /root/.local /root/.local

# Define variáveis de ambiente
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Copia código da aplicação
COPY . .

# Expõe porta
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501', timeout=5)"

# Executa a aplicação
CMD ["streamlit", "run", "app.py", "--logger.level=debug"]