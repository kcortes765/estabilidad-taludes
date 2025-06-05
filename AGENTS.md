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
