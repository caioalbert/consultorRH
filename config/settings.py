"""
Arquivo de configuração do sistema
"""
import os
from pathlib import Path

# Caminhos
BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data"
ASSETS_PATH = BASE_DIR / "assets"
DOCS_PATH = BASE_DIR / "docs"
STATIC_PATH = BASE_DIR / "static"

# Configurações da aplicação
APP_TITLE = "DevOps Hub"
APP_ICON = str(STATIC_PATH / "logo.png")
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistema de BI para Controle de Inventário de Aplicações"

# Configurações de dados
DEFAULT_CSV_FILE = "inventario_aplicacoes.csv"
DEFAULT_GMUD_FILE = "gmud_dados.csv"

# Configurações do PostgreSQL
USE_POSTGRES = os.getenv('USE_POSTGRES', 'False').lower() == 'true'
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'devops_hub')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

# Configurações de ambiente
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
APP_ENV = os.getenv('APP_ENV', 'development')

# Cache
ENABLE_CACHE = os.getenv('ENABLE_CACHE', 'True').lower() == 'true'
CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))  # segundos

# Logs
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = BASE_DIR / "logs" / "app.log"
