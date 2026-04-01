@echo off
color 0b
title Inicializador - PDF Compressor Premium
cd /d "%~dp0"

echo =======================================================
echo          Inicializando PDF Compressor Premium
echo =======================================================
echo.

echo [1/3] Verificando o ambiente virtual de dependencias...
if not exist "venv\Scripts\activate.bat" (
    echo    - O ambiente nao foi encontrado. Configurando pela primeira vez...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao criar ambiente virtual! Verifique se o Python esta instalado e no PATH.
        pause
        exit /b %errorlevel%
    )
    echo    - Ambiente criado com sucesso.
) else (
    echo    - Ambiente encontrado.
)

echo.
echo [2/3] Ativando ambiente...
call venv\Scripts\activate.bat

echo.
echo [3/3] Checando bibliotecas Python necessarias...
pip install -r requirements.txt --disable-pip-version-check
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependencias do requirements.txt.
    pause
    exit /b %errorlevel%
)

echo.
echo Tudo pronto! Iniciando interface grafica...
echo O Ghostscript deve estar previamente instalado na maquina para compressoes extremas.

:: Inicia usando 'pythonw' para nao manter a janela cmd preta rodando inutilmente em background
start pythonw main.py
exit
