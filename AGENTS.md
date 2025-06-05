# Guía para el Agente IA: Estrategia de Pruebas Exhaustiva

## Objetivo Principal para el Agente IA: Generación y Ejecución de Pruebas

Tu tarea principal es desarrollar y ejecutar un conjunto de pruebas exhaustivas para el proyecto `estabilidad-taludes_model`. El objetivo es asegurar la robustez, precisión y fiabilidad de la aplicación en todas sus facetas, desde la interfaz de usuario hasta los cálculos más complejos del núcleo.

**Necesitamos probar TODO.** No asumas que algo funciona; verifica cada componente, cada función, cada interacción.

A continuación, se presenta una lista conceptual de categorías de pruebas y ejemplos de pruebas individuales. Debes usar estas ideas como base para generar pruebas concretas utilizando `pytest` y otras herramientas de testing adecuadas.

---

## Categorías de Pruebas Conceptuales (Aproximadamente 100 ideas)

### 1. Pruebas de Interfaz de Usuario (GUI)

*   **1.1. Inicialización y Visibilidad:**
    *   Verificar que todos los widgets principales (botones, campos de entrada, etiquetas, gráficos) son visibles al iniciar la aplicación.
    *   Asegurar que los valores por defecto en los campos de entrada son correctos.
    *   Comprobar que los elementos de menú están presentes y habilitados/deshabilitados según la lógica inicial.
*   **1.2. Interacción de Entrada:**
    *   Probar la entrada de valores numéricos válidos (enteros, flotantes) en todos los campos.
    *   Probar la entrada de valores no numéricos (texto, caracteres especiales) y verificar que se manejan correctamente (errores, rechazo de entrada).
    *   Probar la entrada de valores fuera de rango (ej. ángulos negativos, pesos unitarios cero) y verificar mensajes de error o correcciones automáticas.
    *   Verificar que los campos de entrada se actualizan correctamente al cambiar entre pestañas o módulos.
*   **1.3. Funcionalidad de Botones:**
    *   Probar cada botón (`Calcular FS`, `Buscar FS Crítico`, `Guardar`, `Cargar`, etc.) y verificar que realiza la acción esperada.
    *   Verificar el estado de los botones (habilitado/deshabilitado) en diferentes contextos (ej. `Calcular FS` deshabilitado si faltan datos).
    *   Probar clics repetidos en botones y verificar que no causan errores o comportamientos inesperados.
*   **1.4. Visualización de Resultados:**
    *   Verificar que los resultados de cálculo (FS, círculo de falla) se muestran correctamente en la GUI.
    *   Asegurar que los gráficos se actualizan dinámicamente con los nuevos datos.
    *   Probar la visualización de mensajes de error y advertencia al usuario.
*   **1.5. Manejo de Errores en GUI:**
    *   Simular errores en el backend y verificar que la GUI los captura y muestra adecuadamente al usuario.
    *   Probar escenarios donde la GUI recibe datos inesperados o incompletos del backend.
*   **1.6. Navegación y Pestañas:**
    *   Verificar que la navegación entre pestañas (`Datos de Entrada`, `Resultados`, etc.) funciona sin pérdida de datos o errores.
    *   Probar la persistencia de datos al cambiar de pestaña y volver.

### 2. Pruebas de Lógica de Cálculo (Core)

*   **2.1. Método de Bishop Simplificado:**
    *   Calcular FS para casos simples con geometría conocida y comparar con resultados manuales/analíticos.
    *   Probar con múltiples capas de suelo y verificar la correcta aplicación de propiedades.
    *   Probar con y sin nivel freático.
    *   Casos extremos: cohesión cero, ángulo de fricción cero, taludes muy empinados/planos.
    *   Verificar la convergencia del método.
*   **2.2. Método de Fellenius (Ordinario):**
    *   Similar a Bishop, probar casos simples y complejos, con y sin nivel freático.
    *   Comparar resultados con Bishop para entender las diferencias esperadas.
    *   Casos extremos.
*   **2.3. Optimización de Círculos (Smart Circle Optimizer):**
    *   Verificar que el optimizador encuentra el círculo de falla crítico (FS mínimo) para escenarios conocidos.
    *   Probar la eficiencia del algoritmo (tiempo de ejecución) con un gran número de círculos.
    *   Asegurar que el optimizador maneja correctamente los límites geométricos y las correcciones.
    *   Probar con diferentes configuraciones de búsqueda (número de iteraciones, tamaño de paso).
*   **2.4. Cálculo de Dovelas (Slices):**
    *   Verificar la correcta subdivisión del círculo de falla en dovelas.
    *   Asegurar que las propiedades de cada dovela (ancho, altura, peso, fuerzas) se calculan correctamente.
    *   Probar con diferentes posiciones del nivel freático que intersecten las dovelas.
    *   Verificar la correcta interpolación de propiedades de suelo para dovelas que atraviesan múltiples capas.

### 3. Pruebas de Geometría y Restricciones de Círculos

*   **3.1. Cálculo de Límites Geométricos (`CalculadorLimites`):**
    *   Probar el cálculo de `centro_x_min`, `centro_x_max`, `centro_y_min`, `centro_y_max`, `radio_min`, `radio_max` para diversas geometrías de talud.
    *   Casos con taludes invertidos o geometrías complejas que puedan generar límites inusuales.
*   **3.2. Validación y Corrección de Círculos (`validar_y_corregir_circulo`):
    *   Probar círculos que están completamente dentro de los límites.
    *   Probar círculos que exceden `centro_x_min`, `centro_x_max`, `centro_y_min`, `centro_y_max`, `radio_min`, `radio_max` individualmente.
    *   Probar círculos que exceden múltiples límites simultáneamente.
    *   Verificar que la corrección automática (`corregir_automaticamente=True`) ajusta el círculo a los límites esperados.
    *   Verificar que sin corrección automática (`corregir_automaticamente=False`), se reportan las violaciones correctamente.
    *   Asegurar que el `ResultadoValidacion` contiene la información correcta (es_valido, violaciones, circulo_corregido).
*   **3.3. Intersecciones:**
    *   Probar la correcta detección de intersecciones entre círculos y líneas de talud/capas de suelo.

### 4. Pruebas de Propiedades de Materiales

*   **4.1. Definición de Suelos:**
    *   Verificar que las propiedades de cohesión, ángulo de fricción y peso unitario se asignan y recuperan correctamente.
    *   Probar con valores cero o negativos para propiedades (si son válidos o cómo se manejan).
*   **4.2. Múltiples Capas:**
    *   Asegurar que el sistema maneja correctamente la definición de múltiples capas de suelo con diferentes propiedades.
    *   Verificar que las propiedades correctas se aplican a las dovelas según la capa en la que se encuentran.

### 5. Pruebas de Integración y Flujo de Trabajo

*   **5.1. Flujo Completo:**
    *   Simular un flujo de trabajo completo: entrada de datos -> cálculo -> visualización -> guardar/cargar.
    *   Asegurar que los componentes interactúan correctamente sin errores.
*   **5.2. Persistencia de Datos:**
    *   Guardar un proyecto con datos complejos y cargarlo para verificar que todos los datos se restauran con precisión.
    *   Probar la compatibilidad de versiones de archivos (si se cambia el formato de guardado).
*   **5.3. Manejo de Errores Global:**
    *   Inyectar errores en diferentes puntos del sistema (ej. datos de entrada inválidos, fallos de cálculo) y verificar que el sistema los maneja de forma elegante y no se bloquea.

### 6. Pruebas de Rendimiento y Robustez

*   **6.1. Carga de Datos:**
    *   Probar el rendimiento con un gran número de puntos en la geometría del talud o muchas capas de suelo.
*   **6.2. Estrés de Cálculo:**
    *   Ejecutar el optimizador de círculos con un número extremadamente alto de iteraciones o una malla de búsqueda muy fina.
    *   Monitorear el uso de memoria y CPU durante cálculos intensivos.
*   **6.3. Estabilidad a Largo Plazo:**
    *   Ejecutar la aplicación durante un período prolongado con operaciones repetidas para detectar fugas de memoria o inestabilidades.

---

## Instrucciones para el Agente IA

1.  **Prioridad:** Tu máxima prioridad es implementar estas pruebas. No te enfoques en nuevas características hasta que el conjunto de pruebas sea robusto.
2.  **Herramientas:** Utiliza `pytest` para la creación y ejecución de pruebas unitarias y de integración. Considera `pytest-cov` para la cobertura de código.
3.  **Detalle:** Cada idea conceptual debe traducirse en uno o más casos de prueba concretos, con entradas y salidas esperadas bien definidas.
4.  **Cobertura:** Intenta lograr la mayor cobertura de código posible, especialmente en los módulos `core/`.
5.  **Reporte:** Genera informes de prueba claros y concisos. Si una prueba falla, proporciona suficiente información para depurar el problema.
6.  **Automatización:** Las pruebas deben ser completamente automatizadas y ejecutables sin intervención manual.
7.  **Colaboración:** Si encuentras ambigüedades en las ideas de prueba o necesitas aclaraciones sobre el comportamiento esperado, pregunta.
8.  **Actualización de Código:** Si descubres bugs a través de estas pruebas, documenta el bug y, si es posible, crea una solución. Sin embargo, el enfoque principal es la creación de pruebas.

¡Comienza a construir un conjunto de pruebas que nos dé total confianza en la aplicación!

---

## Plan de Resolución de Bugs Identificados (Actualización)

Se han identificado dos bugs críticos que impiden el correcto funcionamiento y la visualización de resultados. La estrategia para su resolución se centrará en la creación de tests que reproduzcan el error, la implementación de soluciones robustas y la evaluación iterativa de los resultados.

### Bug 1: `AttributeError: 'Dovela' object has no attribute 'y_base'`

*   **Descripción del Problema:** La clase `Dovela` (en `data/models.py`) no posee los atributos `y_base` ni `y_superficie`. Sin embargo, el módulo de graficación (`gui_plotting.py`) intenta acceder a estos atributos al dibujar las dovelas, lo que provoca un `AttributeError` y el cierre inesperado de la aplicación.
*   **Origen:** La función `crear_dovelas` (en `core/geometry.py`) es la encargada de instanciar los objetos `Dovela` y no les asigna estos atributos. Los objetos `Dovela` se generan a partir del resultado del análisis de Bishop (`analizar_bishop` en `core/bishop.py`), que a su vez es llamado por `bishop_talud_homogeneo`.
*   **Impacto:** Impide la visualización de los resultados del análisis de estabilidad, haciendo que la aplicación sea inoperable para su propósito principal.

**Tareas para la Resolución del Bug 1:**
1.  **Creación de Tests de Reproducción (Pytest):**
    *   Crear un test unitario que simule la creación de un objeto `Dovela` a través de `crear_dovelas` y luego intente acceder a `y_base` o `y_superficie`, esperando un `AttributeError` inicialmente.
    *   Crear un test de integración que ejecute un análisis completo de Bishop y verifique que las dovelas resultantes no causan un `AttributeError` al ser procesadas para graficación (esto requerirá una simulación o mock del comportamiento de `gui_plotting.py`).
    *   **Evaluación:** El test debe fallar antes de la corrección y pasar después.
2.  **Análisis y Diseño de Solución Robusta:**
    *   Determinar la fuente correcta de `y_base` y `y_superficie`. ¿Deben ser parte del `dataclass Dovela`? ¿O deben ser calculados en `gui_plotting.py` o en una función auxiliar antes de la graficación?
    *   Si deben ser parte de `Dovela`, modificar `data/models.py` para incluir estos atributos y `crear_dovelas` para calcular y asignar sus valores.
    *   Si deben ser calculados en otro lugar, modificar `gui_plotting.py` o una función intermedia para calcularlos dinámicamente antes de dibujar, sin depender de que estén en el objeto `Dovela`.
    *   **Consideración:** La solución debe ser coherente con el modelo de datos y la separación de responsabilidades.
3.  **Implementación de la Solución:** Aplicar los cambios de código según el diseño elegido.
4.  **Ejecución y Evaluación Iterativa:**
    *   Ejecutar los tests creados para el Bug 1. Si fallan, depurar y ajustar la solución.
    *   Ejecutar la aplicación completa y verificar visualmente que los gráficos de dovelas se muestran correctamente sin errores.
    *   **Iteración:** Si se encuentran nuevos problemas, documentarlos y repetir el ciclo de test-solución-evaluación.

### Bug 2: `UnboundLocalError` en `validar_y_corregir_circulo`

*   **Descripción del Problema:** En la función `validar_y_corregir_circulo` (en `core/circle_constraints.py`), las variables `xc_corregido`, `yc_corregido` y `radio_corregido` se declaran y asignan condicionalmente dentro de bloques `if corregir_automaticamente:`. Si estas condiciones no se cumplen (ej. `corregir_automaticamente` es `False`, o el círculo no viola ningún límite), las variables nunca son asignadas. Sin embargo, el código intenta utilizarlas más adelante para construir el objeto `circulo_corregido`, lo que resulta en un `UnboundLocalError`.
*   **Origen:** Falta de inicialización de las variables o un flujo de control que no garantiza su asignación antes de su uso.
*   **Impacto:** El programa falla cuando se intenta validar un círculo bajo ciertas condiciones, impidiendo la correcta operación del módulo de restricciones geométricas.

**Tareas para la Resolución del Bug 2:**
1.  **Creación de Tests de Reproducción (Pytest):**
    *   Crear un test unitario para `validar_y_corregir_circulo` que pase un `CirculoFalla` que no viole ningún límite y con `corregir_automaticamente=False`. Este test debe reproducir el `UnboundLocalError`.
    *   Crear tests adicionales que pasen círculos que violen límites pero con `corregir_automaticamente=False`, para asegurar que las violaciones se reportan correctamente sin errores.
    *   **Evaluación:** Los tests deben fallar antes de la corrección y pasar después.
2.  **Análisis y Diseño de Solución Robusta:**
    *   Inicializar `xc_corregido`, `yc_corregido`, y `radio_corregido` con valores por defecto (ej. los valores originales del círculo) al inicio de la función. Esto garantiza que siempre tengan un valor asignado.
    *   Alternativamente, refactorizar la lógica para que `circulo_corregido` solo se construya si `corregir_automaticamente` es `True` y se han realizado correcciones, o si se inicializa con el `circulo` original y solo se modifican los atributos necesarios.
    *   **Consideración:** La solución debe ser limpia y evitar la repetición de código.
3.  **Implementación de la Solución:** Aplicar los cambios de código según el diseño elegido.
4.  **Ejecución y Evaluación Iterativa:**
    *   Ejecutar los tests creados para el Bug 2. Si fallan, depurar y ajustar la solución.
    *   Integrar estos tests en el conjunto de pruebas general y asegurar que no introducen regresiones.
    *   **Iteración:** Si se encuentran nuevos problemas, documentarlos y repetir el ciclo de test-solución-evaluación.

---

**Instrucciones Generales para la Resolución de Bugs:**
*   **Priorización:** Abordar el Bug 1 (`AttributeError`) primero, ya que es un bloqueador para la visualización.
*   **Desarrollo Dirigido por Pruebas (TDD):** Para cada bug, escribir los tests de reproducción *antes* de implementar la solución. Esto asegura que la solución realmente corrige el problema y que no se introducen regresiones.
*   **Modularidad:** Mantener las soluciones lo más localizadas posible, afectando solo el código necesario.
*   **Documentación:** Asegurarse de que el código corregido esté bien comentado y que los cambios sean claros.
*   **Control de Versiones:** Realizar commits atómicos con mensajes claros para cada paso (ej. "feat: Add test for Dovela y_base bug", "fix: Resolve Dovela y_base AttributeError").
