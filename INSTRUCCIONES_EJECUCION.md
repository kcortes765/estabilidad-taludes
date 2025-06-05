# Instrucciones para Ejecutar la GUI de Análisis de Estabilidad de Taludes

## Requisitos del Sistema

### 1. Python 3.8 o superior
- Descargar desde: https://www.python.org/downloads/
- **IMPORTANTE**: Durante la instalación, marcar "Add Python to PATH"

### 2. Librerías Requeridas
```bash
pip install customtkinter
pip install matplotlib
pip install numpy
pip install tkinter  # Generalmente incluido con Python
```

## Verificación de Instalación

### Paso 1: Verificar Python
Abrir PowerShell o CMD y ejecutar:
```bash
python --version
```
Debería mostrar algo como: `Python 3.11.x`

### Paso 2: Verificar Librerías
```bash
python -c "import customtkinter; print('CustomTkinter OK')"
python -c "import matplotlib; print('Matplotlib OK')"
python -c "import numpy; print('NumPy OK')"
```

## Ejecución de la GUI

### Método 1: Desde PowerShell/CMD
```bash
cd "c:\Seba\Proyectos paralelos\estabilidad-taludes_model"
python gui_app.py
```

### Método 2: Usando el archivo batch
Hacer doble clic en `run_gui.bat`

### Método 3: Desde Python IDLE
1. Abrir Python IDLE
2. File → Open → seleccionar `gui_app.py`
3. Run → Run Module (F5)

## Funcionalidades de la GUI

### Panel de Parámetros
- **Geometría del Talud**: altura, ángulo
- **Propiedades del Suelo**: cohesión, ángulo de fricción, peso específico
- **Círculo de Falla**: centro X, centro Y, radio
- **Nivel Freático**: activar/desactivar, altura

### Casos de Ejemplo
- Talud Estable - Carretera
- Talud Marginal - Arcilla Blanda
- Talud con Agua - Crítico
- Talud Inestable - Arena Suelta

### Análisis Disponibles
1. **Análisis Simple**: Botón "Analizar Talud"
2. **Búsqueda FS Crítico**: Optimización automática
3. **Análisis Paramétrico**: Variación de parámetros

### Resultados
- Factor de Seguridad Bishop
- Factor de Seguridad Fellenius
- Gráficos de geometría y resultados
- Clasificación de estabilidad

## Solución de Problemas

### Error: "python no se reconoce"
1. Reinstalar Python marcando "Add to PATH"
2. Reiniciar PowerShell/CMD
3. Verificar con `python --version`

### Error: ModuleNotFoundError
```bash
pip install [nombre_modulo]
```

### Error en la GUI
1. Verificar que todos los archivos estén presentes
2. Ejecutar `python diagnostico_rapido.py` para verificar
3. Revisar mensajes de error en consola

## Archivos del Proyecto

### Archivos Principales
- `gui_app.py` - Aplicación principal
- `gui_analysis.py` - Funciones de análisis para GUI
- `gui_components.py` - Componentes de interfaz
- `gui_plotting.py` - Gráficos y visualización

### Archivos Core
- `core/bishop.py` - Método Bishop Modificado
- `core/fellenius.py` - Método Fellenius
- `core/geometry.py` - Funciones geométricas
- `data/models.py` - Clases de datos

### Tests y Ejemplos
- `diagnostico_rapido.py` - Verificación rápida
- `test_gui_simple.py` - Test de GUI
- `examples/` - Casos de ejemplo

## Contacto y Soporte

Si persisten los problemas:
1. Verificar versión de Python: `python --version`
2. Verificar librerías instaladas: `pip list`
3. Ejecutar diagnóstico: `python diagnostico_rapido.py`
4. Revisar archivos de log de errores
