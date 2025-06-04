# PLAN DE DESARROLLO - APLICACIÓN ESTABILIDAD DE TALUDES

## OBJETIVO GENERAL
Desarrollar una aplicación Python completamente funcional que calcule el Factor de Seguridad de taludes usando los métodos de Fellenius y Bishop Modificado, con capacidad de análisis de múltiples estratos, nivel freático, y búsqueda automática de la superficie de falla crítica.

## ARQUITECTURA DE ARCHIVOS OBJETIVO
```
taludes_app/
├── plan.md                   # Este archivo - Plan detallado
├── log.md                    # Registro de progreso  
├── main.py                   # Interfaz principal
├── core/
│   ├── geometry.py          # Funciones geométricas
│   ├── fellenius.py        # Método Fellenius
│   ├── bishop.py           # Método Bishop iterativo
│   └── search.py           # Búsqueda superficie crítica
├── data/
│   ├── models.py           # Clases Dovela, CirculoFalla, Estrato
│   └── validation.py       # Validaciones obligatorias
├── visualization/
│   └── plotting.py         # Gráficos con matplotlib
├── tests/
│   ├── test_fellenius.py   # Tests funcionales
│   ├── test_bishop.py      # Tests iteración y convergencia
│   └── test_integration.py # Test caso completo
└── examples/
    ├── caso_simple.py      # Ejemplo básico funcionando
    └── caso_con_agua.py    # Ejemplo con nivel freático
```

## FUNCIONALIDADES ORDENADAS POR PRIORIDAD

### FASE 1: FUNDAMENTOS BÁSICOS (CRÍTICA)
**Prioridad: MÁXIMA - Sin esto no funciona nada**

#### 1.1 Estructura de Datos Base
- **Tarea**: Crear `data/models.py`
- **Funcionalidad**: Clases Dovela, CirculoFalla, Estrato con dataclasses
- **Criterios de éxito**: 
  - Dovela con todos los atributos requeridos (x_centro, ancho, altura, angulo_alpha, etc.)
  - CirculoFalla con centro, radio, dovelas y factores de seguridad
  - Validación de tipos y rangos válidos
- **Dependencias**: Ninguna
- **Tiempo estimado**: 1 iteración

#### 1.2 Funciones Geométricas Básicas
- **Tarea**: Crear `core/geometry.py`
- **Funcionalidad**: Funciones para cálculos geométricos fundamentales
- **Criterios de éxito**:
  - `calcular_y_circulo()`: Intersección círculo-vertical correcta
  - `interpolar_terreno()`: Interpolación lineal del perfil
  - `calcular_angulo_alpha()`: Ángulo tangente al círculo en radianes
  - `crear_dovelas()`: Discretización correcta del círculo
- **Dependencias**: models.py
- **Tiempo estimado**: 1-2 iteraciones

#### 1.3 Validaciones Críticas
- **Tarea**: Crear `data/validation.py`
- **Funcionalidad**: Validaciones geométricas y físicas obligatorias
- **Criterios de éxito**:
  - Validar geometría válida (altura > 0, |α| < 80°)
  - Validar parámetros geotécnicos (c' ≥ 0, 0° ≤ φ' ≤ 45°, γ > 0)
  - Validar convergencia en métodos iterativos
- **Dependencias**: models.py
- **Tiempo estimado**: 1 iteración

### FASE 2: MÉTODOS DE CÁLCULO (CRÍTICA)
**Prioridad: ALTA - Funcionalidad principal**

#### 2.1 Método Fellenius
- **Tarea**: Crear `core/fellenius.py`
- **Funcionalidad**: Implementación completa del método Fellenius
- **Criterios de éxito**:
  - Fórmula exacta: `Fs = Σ[c'i × ΔLi + (Wi × cos(αi) - ui × ΔLi) × tan(φ'i)] / Σ[Wi × sin(αi)]`
  - Manejo correcto de tracción (fricción = 0 si fuerza normal < 0)
  - Unidades consistentes (kN, m, kPa)
  - Test funcional con caso simple: 1.2 ≤ Fs ≤ 1.8
- **Dependencias**: geometry.py, models.py, validation.py
- **Tiempo estimado**: 2 iteraciones

#### 2.2 Método Bishop Modificado (ITERATIVO)
- **Tarea**: Crear `core/bishop.py`
- **Funcionalidad**: Implementación iterativa del método Bishop
- **Criterios de éxito**:
  - Proceso iterativo obligatorio con convergencia < 0.001
  - Validación mα > 0 para todas las dovelas
  - Máximo 100 iteraciones con manejo de no-convergencia
  - Fs_bishop ≥ Fs_fellenius (típicamente 5-15% mayor)
  - Convergencia en < 20 iteraciones para casos normales
- **Dependencias**: fellenius.py (para Fs inicial)
- **Tiempo estimado**: 2-3 iteraciones

### FASE 3: INTEGRACIÓN Y TESTS (ALTA)
**Prioridad: ALTA - Validación de funcionamiento**

#### 3.1 Tests Funcionales Básicos
- **Tarea**: Crear `tests/test_fellenius.py` y `tests/test_bishop.py`
- **Funcionalidad**: Tests para validar métodos individuales
- **Criterios de éxito**:
  - Test caso homogéneo sin agua
  - Test caso con nivel freático
  - Test convergencia Bishop
  - Test validación de mα > 0
- **Dependencias**: fellenius.py, bishop.py
- **Tiempo estimado**: 1-2 iteraciones

#### 3.2 Visualización Básica
- **Tarea**: Crear `visualization/plotting.py`
- **Funcionalidad**: Gráficos básicos del talud y círculo de falla
- **Criterios de éxito**:
  - Gráfico del perfil del terreno
  - Círculo de falla con dovelas
  - Nivel freático si existe
  - Información del Factor de Seguridad
- **Dependencias**: models.py
- **Tiempo estimado**: 1-2 iteraciones

### FASE 4: CASOS DE EJEMPLO (MEDIA)
**Prioridad: MEDIA - Demostración de uso**

#### 4.1 Ejemplo Básico
- **Tarea**: Crear `examples/caso_simple.py`
- **Funcionalidad**: Caso de prueba simple funcionando
- **Criterios de éxito**:
  - Talud homogéneo sin agua
  - Cálculo Fellenius y Bishop
  - Visualización del resultado
  - Fs entre 1.2-1.8
- **Dependencias**: Todos los módulos básicos
- **Tiempo estimado**: 1 iteración

#### 4.2 Ejemplo con Agua
- **Tarea**: Crear `examples/caso_con_agua.py`
- **Funcionalidad**: Caso con nivel freático
- **Criterios de éxito**:
  - Mismo talud que caso simple pero con agua
  - Fs_con_agua < Fs_sin_agua
  - Visualización del nivel freático
- **Dependencias**: caso_simple.py funcionando
- **Tiempo estimado**: 1 iteración

### FASE 5: BÚSQUEDA AUTOMÁTICA (BAJA)
**Prioridad: BAJA - Funcionalidad avanzada**

#### 5.1 Búsqueda Superficie Crítica
- **Tarea**: Crear `core/search.py`
- **Funcionalidad**: Búsqueda automática del círculo con Fs mínimo
- **Criterios de éxito**:
  - Algoritmo de búsqueda en grilla
  - Identificación del círculo crítico
  - Validación de múltiples círculos
- **Dependencias**: Todos los métodos de cálculo
- **Tiempo estimado**: 2-3 iteraciones

#### 5.2 Interfaz Principal
- **Tarea**: Crear `main.py`
- **Funcionalidad**: Interfaz de línea de comandos
- **Criterios de éxito**:
  - Carga de datos desde archivo
  - Selección de método de cálculo
  - Exportación de resultados
- **Dependencias**: Todos los módulos
- **Tiempo estimado**: 1-2 iteraciones

### FASE 6: DOCUMENTACIÓN Y TESTS AVANZADOS (BAJA)
**Prioridad: BAJA - Pulimiento final**

#### 6.1 Test de Integración
- **Tarea**: Crear `tests/test_integration.py`
- **Funcionalidad**: Test completo de caso real
- **Criterios de éxito**:
  - Test de extremo a extremo
  - Validación de múltiples estratos
  - Test de rendimiento básico
- **Dependencias**: Toda la aplicación
- **Tiempo estimado**: 1 iteración

#### 6.2 Archivo de Registro
- **Tarea**: Crear y mantener `log.md`
- **Funcionalidad**: Registro de progreso y decisiones
- **Criterios de éxito**:
  - Log de cada tarea completada
  - Problemas encontrados y soluciones
  - Commits asociados
- **Dependencias**: Se actualiza en cada iteración
- **Tiempo estimado**: Continuo

## ORDEN DE IMPLEMENTACIÓN RECOMENDADO

1. **models.py** → Base de datos
2. **geometry.py** → Funciones geométricas
3. **validation.py** → Validaciones críticas
4. **fellenius.py** → Primer método de cálculo
5. **test_fellenius.py** → Validación Fellenius
6. **bishop.py** → Método iterativo
7. **test_bishop.py** → Validación Bishop
8. **plotting.py** → Visualización básica
9. **caso_simple.py** → Ejemplo funcionando
10. **caso_con_agua.py** → Ejemplo con agua
11. **search.py** → Búsqueda automática (opcional)
12. **main.py** → Interfaz principal (opcional)

## CRITERIOS DE ÉXITO GLOBALES

### Técnicos
- ✅ Método Bishop es iterativo con convergencia verificada
- ✅ Se valida que mα > 0 para todas las dovelas
- ✅ Se manejan casos de tracción (fricción = 0)
- ✅ Unidades consistentes (kN, m, kPa, radianes)
- ✅ Diferencia Bishop-Fellenius: 5-15% típicamente

### Funcionales
- ✅ Caso simple funciona: 1.2 ≤ Fs ≤ 1.8
- ✅ Caso con agua: Fs_con_agua < Fs_sin_agua
- ✅ Convergencia Bishop en < 20 iteraciones
- ✅ Visualización clara del talud y círculo
- ✅ Tests funcionales pasan correctamente

### Arquitecturales
- ✅ Código modular y bien organizado
- ✅ Separación clara de responsabilidades
- ✅ Tests para cada módulo principal
- ✅ Ejemplos funcionando listos para usar

## NOTAS IMPORTANTES

- **NUNCA** implementar Bishop como fórmula directa - DEBE ser iterativo
- **SIEMPRE** validar convergencia y manejar no-convergencia
- **OBLIGATORIO** verificar mα > 0 antes de usar Bishop
- **CRÍTICO** manejar tracción correctamente en dovelas
- Crear test funcional después de cada funcionalidad principal
- Actualizar log.md con cada commit
- Una tarea a la vez, sin saltar pasos

## PRÓXIMA ACCIÓN
Comenzar con la implementación de `data/models.py` - las clases base del sistema.
