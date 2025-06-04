@echo off
echo Iniciando GUI de Análisis de Estabilidad de Taludes...
echo.

REM Intentar diferentes comandos de Python
python gui_app.py
if %errorlevel% neq 0 (
    py gui_app.py
    if %errorlevel% neq 0 (
        python3 gui_app.py
        if %errorlevel% neq 0 (
            echo Error: No se pudo encontrar Python
            echo Asegurese de que Python este instalado y en el PATH
            pause
        )
    )
)
