# Sistema de Análisis de Estabilidad de Taludes

## Descripción
Sistema completo para análisis de estabilidad de taludes usando los métodos de Fellenius y Bishop Modificado. Incluye interfaz gráfica moderna, análisis paramétrico, y visualización avanzada de resultados.

## Características Principales

### 🔬 Métodos de Análisis
- **Método de Fellenius** (directo)
- **Método de Bishop Modificado** (iterativo)
- Análisis con y sin nivel freático
- Búsqueda automática de factor de seguridad crítico

### 🖥️ Interfaz Gráfica
- GUI moderna con CustomTkinter
- Casos de ejemplo predefinidos
- Visualización en tiempo real
- Análisis paramétrico interactivo

### 📊 Visualización
- Gráficos de geometría del talud
- Visualización de dovelas y fuerzas
- Comparación de métodos
- Gráficos de convergencia

### ✅ Validación Robusta
- Validación de parámetros geotécnicos
- Verificación de geometría
- Detección de errores de convergencia
- Manejo de casos límite

## Instalación Rápida

### 1. Verificar Python
```bash
python --version
```
*Requiere Python 3.8 o superior*

### 2. Instalar Dependencias
```bash
python instalar_dependencias.py
```

### 3. Verificar Sistema
```bash
python verificar_sistema.py
```

### 4. Ejecutar GUI
```bash
python gui_app.py
```

## Estructura del Proyecto

```
estabilidadad-taludes_model/
├── gui_app.py              # Aplicación principal
├── gui_analysis.py         # Funciones wrapper para GUI
├── gui_components.py       # Componentes de interfaz
├── gui_plotting.py         # Visualización y gráficos
├── gui_examples.py         # Casos de ejemplo
├── core/
│   ├── bishop.py           # Método Bishop Modificado
│   ├── fellenius.py        # Método Fellenius
│   └── geometry.py         # Funciones geométricas
├── data/
│   ├── models.py           # Clases de datos
│   ├── validation.py       # Validaciones
│   └── constants.py        # Constantes del sistema
├── tests/                  # Tests unitarios
├── examples/               # Ejemplos de uso
└── docs/                   # Documentación
```

## Casos de Ejemplo Incluidos

### 1. Talud Estable - Carretera
- Altura: 8.0 m
- Ángulo: 35°
- Factor de Seguridad esperado: > 1.5

### 2. Talud Marginal - Arcilla Blanda
- Altura: 10.0 m
- Ángulo: 45°
- Factor de Seguridad esperado: 1.2-1.4

### 3. Talud con Agua - Crítico
- Con nivel freático alto
- Factor de Seguridad esperado: ≈ 1.0-1.2

### 4. Talud Inestable - Arena Suelta
- Sin cohesión
- Factor de Seguridad esperado: < 1.0

## Uso de la GUI

### Panel de Parámetros
1. **Geometría**: Altura y ángulo del talud
2. **Suelo**: Cohesión, ángulo de fricción, peso específico
3. **Círculo**: Centro X, Y y radio del círculo de falla
4. **Agua**: Nivel freático (opcional)

### Análisis Disponibles
1. **Análisis Simple**: Cálculo directo con parámetros actuales
2. **FS Crítico**: Búsqueda automática del factor mínimo
3. **Paramétrico**: Variación sistemática de parámetros

### Interpretación de Resultados
- **FS > 1.5**: Talud ESTABLE
- **1.2 < FS < 1.5**: Talud MARGINAL
- **FS < 1.2**: Talud INESTABLE

## API Programática

### Análisis Básico
```python
from core.bishop import analizar_bishop
from data.models import CirculoFalla, Estrato
from core.geometry import crear_perfil_terreno

# Crear objetos
circulo = CirculoFalla(xc=8.0, yc=14.0, radio=16.0)
estrato = Estrato(cohesion=35.0, phi_grados=30.0, gamma=19.0)
perfil = crear_perfil_terreno(altura=8.0, angulo_grados=35.0)

# Ejecutar análisis
resultado = analizar_bishop(circulo, perfil, estrato)
print(f"Factor de Seguridad: {resultado.factor_seguridad:.3f}")
```

### Análisis desde GUI
```python
from gui_analysis import analizar_desde_gui

params = {
    'altura': 8.0,
    'angulo_talud': 35.0,
    'cohesion': 35.0,
    'phi_grados': 30.0,
    'gamma': 19.0,
    'centro_x': 8.0,
    'centro_y': 14.0,
    'radio': 16.0,
    'con_agua': False
}

resultado = analizar_desde_gui(params)
if resultado['valido']:
    print(f"Bishop FS: {resultado['bishop'].factor_seguridad:.3f}")
    print(f"Fellenius FS: {resultado['fellenius'].factor_seguridad:.3f}")
```

## Validación y Tests

### Ejecutar Diagnóstico Rápido
```bash
python diagnostico_rapido.py
```

### Ejecutar Tests Completos
```bash
python -m pytest tests/
```

### Verificar Sistema Completo
```bash
python verificar_sistema.py
```

## Solución de Problemas

### Error: "python no se reconoce"
1. Instalar Python desde https://python.org
2. Marcar "Add Python to PATH" durante instalación
3. Reiniciar terminal

### Error: ModuleNotFoundError
```bash
pip install customtkinter matplotlib numpy
```

### Error en Análisis
1. Verificar parámetros dentro de rangos válidos
2. Revisar geometría del círculo vs talud
3. Ejecutar diagnóstico para identificar problema

### GUI no Responde
1. Verificar que no hay análisis en ejecución
2. Cerrar y reiniciar aplicación
3. Verificar casos de ejemplo funcionan

## Desarrollo y Contribución

### Estructura de Desarrollo
- Código modular y bien documentado
- Tests unitarios para cada componente
- Validación exhaustiva de parámetros
- Manejo robusto de errores

### Extensiones Futuras
- Métodos adicionales (Spencer, Morgenstern-Price)
- Análisis probabilístico
- Exportación de reportes
- Análisis 3D

## Contacto y Soporte

Para reportar problemas o solicitar funcionalidades:
1. Ejecutar `python verificar_sistema.py`
2. Incluir output completo del diagnóstico
3. Describir pasos para reproducir el problema

## Licencia

Este proyecto está desarrollado para uso académico y profesional en análisis geotécnico.

---

**Versión**: 2.0  
**Última actualización**: Diciembre 2024  
**Compatibilidad**: Python 3.8+, Windows/Linux/Mac
