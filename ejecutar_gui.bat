@echo off
echo ========================================
echo   GUI Análisis de Estabilidad de Taludes
echo ========================================
echo.

REM Ruta específica de Python encontrada en el sistema
set PYTHON_PATH="C:\Users\kevin\AppData\Local\Programs\Python\Python313\python.exe"

echo Verificando Python...
%PYTHON_PATH% --version
if %errorlevel% neq 0 (
    echo Error: No se puede ejecutar Python
    pause
    exit /b 1
)

echo.
echo Instalando dependencias necesarias...
%PYTHON_PATH% -m pip install customtkinter matplotlib numpy
if %errorlevel% neq 0 (
    echo Advertencia: Problemas instalando dependencias
)

echo.
echo Ejecutando GUI...
%PYTHON_PATH% gui_app.py

if %errorlevel% neq 0 (
    echo.
    echo Error ejecutando la GUI
    echo Presione cualquier tecla para ver diagnóstico...
    pause > nul
    echo.
    echo === DIAGNÓSTICO ===
    %PYTHON_PATH% verificar_sistema.py
    pause
)
