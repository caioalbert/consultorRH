@echo off
echo ========================================
echo Sistema de BI - Inventario de Aplicacoes
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.8 ou superior.
    pause
    exit /b 1
)

echo [1/3] Verificando Python...
python --version

echo.
echo [2/3] Instalando dependencias...
cd /d "%~dp0\.."
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo [3/3] Iniciando aplicacao...
echo.
echo ========================================
echo A aplicacao sera aberta no navegador
echo Pressione Ctrl+C para encerrar
echo ========================================
echo.

python -m streamlit run app.py

pause
