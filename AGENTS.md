# AGENTS.MD - Proyecto Estabilidad de Taludes

## 1. Información del Proyecto
- **Tipo:** Aplicación de escritorio (Desktop GUI)
- **Stack Principal:** Python, CustomTkinter, Matplotlib, NumPy
- **Arquitectura:** Monolito con estructura modular.
- **Objetivo Principal Actual y Filosofía del Proyecto:**
        - **Prioridad Absoluta:** Asegurar la **correctitud física y matemática** de los métodos de Fellenius y Bishop. La aplicación debe ser **sólida, robusta y confiable** para su uso en ingeniería.
        - **Responsabilidad del Agente IA:** Realizar **pruebas exhaustivas y verificaciones internas continuas** para garantizar el funcionamiento completo y preciso de todos los cálculos y funcionalidades. La IA debe ser proactiva en la identificación y corrección de cualquier desviación de los principios geotécnicos.
        - **Desarrollo Actual:** Resolver bugs críticos en la GUI, completar la integración de módulos avanzados (`core/circle_constraints.py`) para asegurar un funcionamiento robusto y resultados geotécnicamente realistas, y añadir funcionalidades clave solicitadas.

## 2. Estructura de Directorios Clave
```
estabilidadad-taludes_model/
├── gui_app.py              # Aplicación GUI principal (CustomTkinter)
├── gui_analysis.py         # Lógica de enlace entre GUI y el core
├── gui_components.py       # Componentes reutilizables de la GUI (ParameterPanel, etc.)
├── gui_plotting.py         # Funciones de graficación para la GUI
├── core/                   # Lógica central de cálculo y análisis
│   ├── bishop.py           # Método de Bishop Modificado
│   ├── fellenius.py        # Método de Fellenius
│   ├── geometry.py         # Geometría del talud, círculo, dovelas
│   ├── circle_constraints.py # Límites geométricos inteligentes para círculos
│   └── smart_circle_optimizer.py # Optimización de círculo crítico
├── data/                   # Modelos de datos y validaciones
│   ├── models.py           # Clases: PerfilTerreno, Estrato, CirculoFalla, etc.
│   └── constants.py        # Constantes físicas y de cálculo
├── tests/                  # Pruebas (Pytest)
│   ├── test_core_bishop.py
│   ├── test_core_geometry.py
│   └── ... (más tests para core y GUI)
├── examples/               # Scripts de ejemplo y casos de prueba
├── (docs/*.md)             # Documentación adicional (CONTEXTO_COMPLETO_PROYECTO.md, etc.)
└── requirements.txt        # Dependencias del proyecto
```

## 3. Stack Tecnológico y Dependencias Críticas
- **Lenguaje:** Python 3.8+
- **GUI:** CustomTkinter (`customtkinter`)
- **Cálculo Numérico:** NumPy (`numpy`)
- **Visualización:** Matplotlib (`matplotlib`)
- **Imágenes (GUI):** Pillow (`Pillow`)
- **Tooltips (GUI):** Tkinter Tooltip (`tkinter-tooltip`)
- **Pruebas:** Pytest (`pytest`, `pytest-cov`)

## 4. Convenciones de Código Esenciales

### Python General
- ✅ **Estilo:** Seguir PEP 8 estrictamente. Usar Black para formateo y Flake8 para linting.
- ✅ **Type Hints:** Obligatorio para todas las definiciones de funciones y métodos, y para variables donde la inferencia no sea obvia. Usar el módulo `typing`.
  ```python
  from typing import List, Tuple, Optional

  def calcular_fuerzas(dovelas: List[Dovela], nf_activo: bool) -> Tuple[float, float]:
      # ...
      pass
  ```
- ✅ **Nomenclatura:**
    - Clases: `PascalCase` (ej. `CirculoFalla`, `ParameterPanel`)
    - Funciones y Variables: `snake_case` (ej. `calcular_fs_bishop`, `perfil_terreno`)
    - Constantes: `UPPER_SNAKE_CASE` (ej. `TOLERANCIA_FS` en `data/constants.py`)
- ✅ **Documentación:** Docstrings en estilo Google o NumPy para todos los módulos, clases, funciones y métodos públicos.
  ```python
  def mi_funcion(param1: int, param2: str) -> bool:
      """Descripción breve de la función.

      Args:
          param1: Descripción del primer parámetro.
          param2: Descripción del segundo parámetro.

      Returns:
          True si la operación fue exitosa, False en caso contrario.
      """
      # ...
      pass
  ```
- ✅ **Manejo de Errores:** Usar excepciones personalizadas que hereden de una `BaseGeotechnicalError`.
  ```python
  # En core/exceptions.py o data/models.py
  class BaseGeotechnicalError(Exception):
      """Clase base para errores geotécnicos."""
      pass

  class InvalidGeometryError(BaseGeotechnicalError):
      """Error para geometría inválida."""
      pass

  class ConvergenceError(BaseGeotechnicalError):
      """Error si el cálculo no converge."""
      pass
  ```
- ✅ **Logging:** Usar el módulo `logging` de Python. Configurar un logger principal en `gui_app.py` y obtener loggers específicos por módulo (`logger = logging.getLogger(__name__)`).

### Unidades y Constantes
- ✅ **Unidades en `core`:**
    - Fuerza: kN (kilonewtons)
    - Longitud/Distancia: m (metros)
    - Presión/Cohesión: kPa (kilopascales)
    - Peso Específico: kN/m³
    - Ángulos: Radianes para cálculos (`math.sin()`, etc.), Grados para entrada/salida de usuario (convertir explícitamente).
- ✅ **Constantes:** Definir en `data/constants.py` (ej. `GRAVEDAD = 9.81`, `TOLERANCIA_CONVERGENCIA_BISHOP = 0.001`).

### GUI (CustomTkinter)
- ✅ **Modularidad:** Separar componentes de la GUI en clases (ej. `ParameterPanel`, `ResultsPanel` en `gui_components.py`).
- ✅ **Callbacks:** Mantener la lógica de los callbacks de la GUI lo más simple posible, delegando tareas complejas a métodos de la clase principal de la app o a módulos de `gui_analysis.py`.

## 5. Patrones de Código Específicos

### Clase de Modelo de Datos Típica (`data/models.py`)
```python
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

@dataclass
class Estrato:
    """Representa un estrato de suelo."""
    espesor: float  # m
    cohesion: float  # kPa
    phi_grados: float  # Grados
    gamma: float     # kN/m³
    nombre: Optional[str] = None

    @property
    def phi_rad(self) -> float:
        return math.radians(self.phi_grados)

@dataclass
class CirculoFalla:
    """Representa un círculo de falla potencial."""
    xc: float
    yc: float
    radio: float
    id_calculo: Optional[str] = None
```

### Función de Cálculo Típica (`core/bishop.py`)
```python
from typing import List, Tuple
from data.models import Dovela, ResultadoAnalisisBishop, Estrato, CirculoFalla
from data.constants import TOLERANCIA_CONVERGENCIA_BISHOP, MAX_ITER_BISHOP
import math

def calcular_fs_bishop_iteracion(
    dovelas: List[Dovela],
    fs_actual: float,
    perfil: List[Tuple[float, float]], # Para info adicional si es necesaria
    # ... otros parámetros relevantes
) -> Tuple[float, List[Dovela]]:
    """Realiza una iteración del cálculo de Bishop.

    Args:
        dovelas: Lista de dovelas con sus propiedades geométricas y de material.
        fs_actual: Factor de seguridad de la iteración anterior.
        # ...

    Returns:
        Nuevo factor de seguridad calculado y lista de dovelas actualizadas.
    """
    momento_resistente_total = 0.0
    momento_actuante_total = 0.0

    for i, dov in enumerate(dovelas):
        # ... cálculos de m_alpha, fuerzas, etc. ...
        # asegurar que dov.m_alpha > 0
        if dov.m_alpha <= 0:
            # logger.warning(f"Dovela {i} con m_alpha <= 0 ({dov.m_alpha:.3f}). Revisar geometría.")
            # Considerar lanzar InvalidGeometryError o devolver un FS inválido
            pass # Manejo de error aquí
        
        # ... acumular momentos ...
    
    nuevo_fs = momento_resistente_total / momento_actuante_total if momento_actuante_total else float('inf')
    return nuevo_fs, dovelas
```

## 6. Comandos Críticos (Ejecutar desde raíz del proyecto)

- **Ejecutar la Aplicación GUI:**
  ```bash
  python gui_app.py
  ```
- **Ejecutar Todos los Tests (Pytest):**
  ```bash
  python -m pytest
  ```
- **Ejecutar Tests de un Archivo Específico:**
  ```bash
  python -m pytest tests/test_core_bishop.py
  ```
- **Ejecutar Tests con Cobertura:**
  ```bash
  python -m pytest --cov=core --cov=data --cov=gui_components tests/
  ```
- **Formatear Código (Black):** (Asumiendo que Black está configurado)
  ```bash
  black .
  ```
- **Verificar Estilo (Flake8):** (Asumiendo que Flake8 está configurado)
  ```bash
  flake8 .
  ```
- **Instalar Dependencias:**
  ```bash
  pip install -r requirements.txt
  ```

## 7. Flujo de Desarrollo y Git

- **Ramas:**
    - `main`: Código de producción estable.
    - `develop`: (Opcional) Rama de integración para features antes de `main`.
    - `feature/[ticket-id]-[descripcion-corta]`: Para nuevas funcionalidades (ej. `feature/GH-12-optimizar-busqueda-circulos`).
    - `fix/[ticket-id]-[descripcion-corta]`: Para corrección de bugs (ej. `fix/GH-15-corregir-error-convergencia`).
- **Commits:**
    - Mensajes descriptivos y en presente (ej. `feat: Add circle validation to GUI analysis flow`).
    - Usar prefijos: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.
- **Antes de cada Commit/Push a una rama de feature/fix:**
    - ✅ Ejecutar `python -m pytest` - TODOS los tests deben pasar.
    - ✅ (Si configurado) Ejecutar `black .` y `flake8 .` - Sin errores de formato/estilo.
- **Pull Requests (PRs) a `main` (o `develop`):**
    - Descripción clara del cambio.
    - Vincular al issue/ticket correspondiente.
    - Asegurar que los tests pasen en la pipeline de CI (si existe).
    - Esperar revisión (si aplica).

## 8. Patrones de Pruebas (Pytest)

### Test Unitario para una Función del Core
```python
# tests/test_core_geometry.py
from core.geometry import calcular_ancho_dovela # Ejemplo
import pytest

def test_calcular_ancho_dovela_simple():
    # Arrange
    x_izq, x_der = 0.0, 1.0
    # Act
    ancho = calcular_ancho_dovela(x_izq, x_der) # Asumiendo que existe esta función
    # Assert
    assert ancho == pytest.approx(1.0)

# Ejemplo con parametrización
@pytest.mark.parametrize(
    "x_izq, x_der, esperado",
    [
        (0.0, 1.0, 1.0),
        (-0.5, 0.5, 1.0),
        (10.0, 10.0, 0.0),
    ]
)
def test_calcular_ancho_dovela_multiples_casos(x_izq, x_der, esperado):
    ancho = calcular_ancho_dovela(x_izq, x_der)
    assert ancho == pytest.approx(esperado)
```

### Test para un Modelo de Datos
```python
# tests/test_data_models.py
from data.models import Estrato
import math

def test_estrato_phi_rad_conversion():
    estrato = Estrato(espesor=10, cohesion=5, phi_grados=30, gamma=18)
    assert estrato.phi_rad == pytest.approx(math.radians(30))
```

## 9. Configuración de Entorno y Variables

- **`requirements.txt`**: Debe estar siempre actualizado con todas las dependencias y sus versiones fijas.
  ```
  customtkinter==X.Y.Z
  numpy==X.Y.Z
  matplotlib==X.Y.Z
  # ...
  ```
- **Variables de Entorno (si son necesarias para el agente):**
  - `OPENAI_API_KEY`: Si el agente Codex CLI la requiere para operar.

## 10. Prohibiciones Específicas (Qué NO hacer)

- ❌ **NO usar `print()` para logging en producción o `core`**. Usar el módulo `logging`.
- ❌ **NO introducir números mágicos directamente en el código**. Definirlos como constantes en `data/constants.py` o al inicio del archivo/clase.
- ❌ **NO escribir funciones/métodos excesivamente largos**. Dividir en unidades lógicas más pequeñas y testeables.
- ❌ **NO ignorar errores silenciosamente con `except: pass`**. Capturar excepciones específicas y manejarlas o loggearlas adecuadamente.
- ❌ **NO modificar listas o diccionarios mientras se iteran sobre ellos de forma insegura**.
- ❌ **NO depender de estado global mutable excesivamente**. Preferir pasar estado como parámetros.
- ❌ **NO mezclar lógica de GUI directamente con lógica de cálculo del `core`**. Mantener la separación de responsabilidades (`gui_analysis.py` como intermediario).

## 11. Notas Específicas del Dominio (Geotecnia)

- ✅ **Validación de `mα > 0`**: Es CRÍTICO para el método de Bishop. Si `mα <= 0` para alguna dovela, el FS no es válido. Esto usualmente indica un problema geométrico con el círculo de falla.
- ✅ **Convergencia de Bishop**: El FS debe converger dentro de `MAX_ITER_BISHOP` iteraciones y con una tolerancia `TOLERANCIA_CONVERGENCIA_BISHOP` (ej. 0.001 o 0.1%).
- ✅ **Factores de Seguridad Realistas**: Para taludes típicos, FS suelen estar entre 1.0 y 3.0. Valores muy altos (ej. > 10) o muy bajos (< 0.5) usualmente indican problemas geométricos o de parámetros.
- ✅ **Geometría del Círculo**: El círculo de falla debe cortar el talud de forma razonable. Módulos como `core/circle_constraints.py` ayudan a asegurar esto.
    - El centro del círculo no debe estar por debajo del pie del talud.
    - El radio debe ser suficiente para cortar el talud, pero no excesivamente grande.
- ✅ **Fuerzas en Dovelas**: Las fuerzas actuantes y resistentes deben tener signos consistentes con las convenciones físicas.

## 12. Errores Específicos para Codex de OpenAI (Prioridad Alta)

### 12.1 UnboundLocalError en Cálculo de Límites Geométricos
- **Error:** `No se pudo calcular los limites geométricos: cannot access local variable where it is not associated with a value`
- **Tipo:** `UnboundLocalError` (Python)
- **Descripción:** Una variable local se utiliza antes de que se le haya asignado un valor.
- **Ubicación Probable:** Dentro del módulo `core/circle_constraints.py`, específicamente en la lógica responsable de calcular los límites geométricos para el círculo de falla. Puede estar relacionado con la clase `CalculadorLimites` o funciones asociadas.
- **Contexto:** Este error aparece en la GUI cuando se intentan mostrar o calcular los límites del círculo de falla, impidiendo la correcta validación y visualización de los círculos.
- **Acción Requerida (Codex):**
    1.  Identificar la variable exacta que causa el `UnboundLocalError` en `core/circle_constraints.py`.
    2.  Analizar el flujo lógico para entender por qué la variable no se asigna en todos los casos esperados.
    3.  Corregir el código para asegurar que la variable siempre tenga un valor asignado antes de su uso.
    4.  Probar exhaustivamente la corrección con diversos escenarios geométricos en la GUI.
- **Prioridad:** ALTA. Este error bloquea una funcionalidad central de la validación inteligente de círculos.

## 13. Tareas Prioritarias Actuales (para el Agente IA)

1.  **Completar Integración de `core/circle_constraints.py` en `gui_app.py`:**
    - **Estado Actual:** Parcialmente implementado. Se ha añadido lógica en `_run_analysis_thread` para calcular límites y validar/corregir el círculo.
    - **Acción Requerida por Agente:** Implementar el método `update_circle_entries(self, xc: float, yc: float, radio: float)` en la clase `ParameterPanel` dentro de `gui_components.py`. Este método debe actualizar los valores de los campos de entrada `CTkEntry` para `centro_x`, `centro_y`, y `radio` en la GUI cuando el sistema corrige automáticamente un círculo inválido.
    - **Archivos Afectados:** `gui_components.py` (añadir método a `ParameterPanel`), `gui_app.py` (asegurar que la llamada `self.parameter_panel.update_circle_entries(...)` funcione).
2.  **Revisar y Estandarizar `longitud_base` para `generar_perfil_simple`:**
    - **Descripción:** Actualmente, `gui_app.py` en `_run_analysis_thread` usa `params.get('longitud_base_talud', 3 * params['altura'])` y en `show_slope_geometry` usa `longitud_base=30` (fijo).
    - **Acción Requerida por Agente:** Analizar si `ParameterPanel` puede/debe proveer `longitud_base_talud`. Si no, decidir un método consistente para calcularla (ej. basado en `altura` y `angulo_talud`) y aplicarlo en ambos lugares. Considerar si `generar_perfil_simple` debería tener una lógica más robusta para esto.
    - **Archivos Afectados:** `gui_app.py`, `data/models.py` (potencialmente `generar_perfil_simple`).
3.  **Implementar Botón "Buscar FS Crítico" (Nueva Funcionalidad):**
    - **Descripción:** Añadir un nuevo botón a la GUI (probablemente en `ParameterPanel` o cerca de los controles de análisis) que active una búsqueda automática del círculo de falla crítico.
    - **Funcionalidad Esperada:**
        - Al presionarlo, el sistema debe iterar a través de una serie de círculos de falla potenciales (utilizando `smart_circle_optimizer.py` o una lógica similar).
        - Debe identificar el círculo que produce el Factor de Seguridad (FS) mínimo.
        - La GUI debe actualizarse para mostrar los parámetros (Xc, Yc, Radio) de este círculo crítico y el FS resultante.
        - El proceso debe ser visualmente informativo si es posible (ej. mostrando círculos intermedios o una barra de progreso).
    - **Acción Requerida por Agente:**
        - Diseñar la ubicación y apariencia del botón en la GUI.
        - Implementar la lógica de callback para el botón en `gui_app.py` o `gui_analysis.py`.
        - Integrar con `core/smart_circle_optimizer.py` o desarrollar la lógica de optimización necesaria.
        - Asegurar que los resultados se muestren correctamente en la GUI y en el gráfico.
        - Añadir pruebas unitarias y de integración para esta funcionalidad.
    - **Archivos Afectados:** `gui_components.py` (añadir botón), `gui_app.py` (callback y lógica), `gui_analysis.py` (posible lógica de orquestación), `core/smart_circle_optimizer.py` (uso o mejora).
    - **Prioridad:** MEDIA-ALTA (después de resolver bugs críticos).

## 14. Mantenimiento de AGENTS.MD

- **Actualizar CUANDO:**
    - ✅ Se añaden/cambian dependencias críticas (`requirements.txt`).
    - ✅ Cambian convenciones de código fundamentales.
    - ✅ Se introducen nuevos comandos de build/test/calidad.
    - ✅ La arquitectura del proyecto evoluciona significativamente.
    - ✅ El Agente IA consistentemente no sigue alguna regla (indica que la regla no está clara o falta).
- **Revisión Periódica:** Revisar este archivo al menos mensualmente o al inicio de fases de desarrollo importantes.

---
Este `AGENTS.MD` está diseñado para guiar a un agente IA en la comprensión y contribución efectiva al proyecto `estabilidad-taludes_model`. La prioridad es resolver el bug crítico de integración de `core/circle_constraints.py` en `gui_app.py` y mejorar la robustez general de la aplicación.
