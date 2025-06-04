@echo off
echo Iniciando aplicacion GUI de Estabilidad de Taludes...
echo =====================================================

REM Intentar diferentes comandos de Python
if exist "C:\Python\python.exe" (
    echo Usando Python desde C:\Python\
    "C:\Python\python.exe" start_gui.py
    goto :end
)

if exist "C:\Python39\python.exe" (
    echo Usando Python 3.9
    "C:\Python39\python.exe" start_gui.py
    goto :end
)

if exist "C:\Python310\python.exe" (
    echo Usando Python 3.10
    "C:\Python310\python.exe" start_gui.py
    goto :end
)

REM Intentar con comando python del PATH
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Usando Python del PATH
    python start_gui.py
    goto :end
)

REM Intentar con py launcher
py --version >nul 2>&1
if %errorlevel% == 0 (
    echo Usando py launcher
    py start_gui.py
    goto :end
)

echo ERROR: No se encontro Python instalado
echo Por favor instale Python 3.8 o superior
echo https://www.python.org/downloads/

:end
echo.
echo Presione cualquier tecla para salir...
pause >nul
