# Guía para el Agente IA: Estrategia de Pruebas y Mejoras

## Objetivo Principal para el Agente IA: Robustez y Funcionalidad Completa

Tu tarea principal es asegurar la robustez, precisión y funcionalidad completa de la aplicación `estabilidad-taludes_model`. Esto implica:
1.  **Identificar y corregir errores críticos** que impiden el uso de la aplicación.
2.  **Implementar una estrategia de pruebas exhaustiva** con evaluaciones significativas.
3.  **Proponer y, si es viable, implementar mejoras técnicas** para la robustez del código base.

**Necesitamos probar y corregir TODO.** No asumas que algo funciona; verifica cada componente, cada función, cada interacción, y cada flujo de trabajo.

---

## 1. Errores Críticos Identificados y Prioridades de Corrección

Se han identificado los siguientes errores críticos que deben ser abordados. La prioridad es resolver aquellos que bloquean la funcionalidad principal o la usabilidad.

### 1.1. Restricción Excesiva del Área de Búsqueda de Círculos de Falla
*   **Descripción del Problema:** El algoritmo de búsqueda de círculos de falla (Smart Circle Optimizer) o sus restricciones geométricas (`core/circle_constraints.py`) son demasiado restrictivas, impidiendo que el usuario explore un rango adecuado de posibles círculos de falla. Esto puede llevar a no encontrar el círculo crítico real o a resultados incorrectos.
*   **Impacto:** Limita la precisión y utilidad del análisis de estabilidad.
*   **Acción Requerida:** Investigar las funciones de cálculo de límites y validación de círculos. Modificar las lógicas para permitir una búsqueda más amplia y realista, asegurando que los círculos generados sean geológicamente plausibles pero no excesivamente limitados.

### 1.2. Botón "ANALIZAR TALUD" No Funciona
*   **Descripción del Problema:** El botón "ANALIZAR TALUD" en la interfaz de usuario no inicia el proceso de análisis o no produce los resultados esperados.
*   **Impacto:** Bloquea la funcionalidad principal de la aplicación.
*   **Acción Requerida:** Depurar la función asociada a este botón en `gui_app.py` y las funciones de backend que debería llamar (e.g., `run_analysis`, `_run_analysis_thread`, y las funciones de cálculo de Bishop/Fellenius). Asegurar que el flujo de datos desde la GUI hasta el cálculo y la visualización de resultados sea correcto.

### 1.3. Botón "LIMPIAR" No Funciona
*   **Descripción del Problema:** El botón "LIMPIAR" en la interfaz de usuario no restablece los campos de entrada, los resultados o los gráficos a su estado inicial.
*   **Impacto:** Dificulta la realización de múltiples análisis o el inicio de un nuevo proyecto sin reiniciar la aplicación.
*   **Acción Requerida:** Implementar o corregir la lógica asociada al botón "LIMPIAR" en `gui_app.py` para que resetee adecuadamente el estado de la aplicación.

### 1.4. Eliminación del Botón "EXPORTAR"
*   **Descripción del Problema:** El usuario ha solicitado la eliminación de la funcionalidad y el botón "EXPORTAR".
*   **Impacto:** Simplificación de la interfaz y eliminación de una funcionalidad no deseada.
*   **Acción Requerida:** Eliminar el botón "Exportar" de la GUI en `gui_app.py` y cualquier código asociado a su funcionalidad.

### 1.5. Bugs Previamente Identificados (Contexto)
*   **Bug 1: `AttributeError: 'Dovela' object has no attribute 'y_base'`**
    *   **Descripción:** La clase `Dovela` no tenía los atributos `y_base` ni `y_superficie`, causando errores al intentar graficarlos.
    *   **Estado:** Resuelto (se añadieron los atributos a `Dovela` y se actualizó `crear_dovelas`).
    *   **Acción Requerida:** Asegurar que estos atributos se visualizan correctamente en los gráficos y que no causan nuevos problemas.
*   **Bug 2: `UnboundLocalError` en `validar_y_corregir_circulo`**
    *   **Descripción:** Variables no inicializadas en `validar_y_corregir_circulo` causaban un `UnboundLocalError`.
    *   **Estado:** Pendiente de confirmación de resolución y pruebas.
    *   **Acción Requerida:** Crear tests de reproducción y aplicar una solución robusta.
*   **Bug 3: Error de Inicio de la GUI (`AttributeError: 'SlopeStabilityApp' object has no attribute 'mainloop'`)**
    *   **Descripción:** La aplicación no se iniciaba debido a una llamada incorrecta a `mainloop`.
    *   **Estado:** Resuelto (se corrigió la llamada a `app.root.mainloop()` en `start_gui.py`).
    *   **Acción Requerida:** Verificación final del inicio correcto de la GUI.

---

## 2. Estrategia de Pruebas Exhaustiva

Debes desarrollar y ejecutar un conjunto de pruebas exhaustivas para toda la aplicación.

### 2.1. Requisitos de Evaluación
*   **Cantidad:** Se requieren al menos **50 evaluaciones (tests)** para toda la aplicación.
*   **Relevancia:** Los tests no deben ser simples. Deben ser lo suficientemente relevantes para identificar y corregir problemas en todas las funcionalidades clave. Esto incluye:
    *   Casos límite y extremos para cálculos (ej. taludes muy planos/empinados, propiedades de suelo cero o negativas si son válidas).
    *   Interacciones complejas entre módulos (GUI -> Core -> Plotting).
    *   Escenarios de error y cómo la aplicación los maneja (ej. entrada de datos inválidos).
    *   Pruebas de regresión para bugs corregidos.
*   **Cobertura:** Priorizar la cobertura de los módulos `core/` y `gui_app.py`, así como `data/models.py`.
*   **Herramientas:** Utiliza `pytest` para la creación y ejecución de pruebas unitarias y de integración. Considera `pytest-cov` para la cobertura de código.

### 2.2. Áreas Clave a Probar
*   **Funcionalidades de la GUI:**
    *   **Inicio y Cierre:** La aplicación se inicia y cierra sin errores.
    *   **Entrada de Parámetros:** Validación de todos los campos de entrada (numéricos, rangos, tipos).
    *   **Botones:** "ANALIZAR TALUD", "ENCONTRAR FS CRÍTICO", "Análisis Paramétrico", "Limpiar", "Ayuda", "Acerca de". Verificar que cada botón realiza su acción esperada y maneja errores.
    *   **Navegación:** Funcionalidad de las pestañas "Geometría", "Análisis", "Comparación", "Convergencia".
    *   **Visualización:** Los gráficos se actualizan correctamente y muestran la información esperada (geometría, círculos de falla, dovelas, resultados).
*   **Lógica de Cálculo (Core):**
    *   **Métodos Bishop y Fellenius:** Precisión de los cálculos con diferentes configuraciones de suelo, nivel freático, y geometría. Comparación con resultados conocidos o analíticos.
    *   **Cálculo de Dovelas:** Correcta subdivisión, cálculo de propiedades (`y_base`, `y_superficie`, altura, peso, etc.).
    *   **Optimización de Círculos:** Eficacia del optimizador para encontrar el FS crítico, manejo de límites y correcciones.
    *   **Restricciones Geométricas:** La función `validar_y_corregir_circulo` y las funciones de límites deben ser probadas exhaustivamente para asegurar que el área de búsqueda de círculos no es excesivamente restrictiva y que los errores `UnboundLocalError` no se reproducen.
*   **Integración:**
    *   Flujo completo desde la entrada de datos en la GUI hasta la visualización de resultados, incluyendo el guardado y carga de proyectos (si aplica).
    *   Manejo de errores entre capas (ej. un error en el cálculo del core se reporta adecuadamente en la GUI).

---

## 3. Recomendaciones para Mejoras Técnicas (Robustez)

Además de la corrección de errores y las pruebas, se recomienda considerar las siguientes mejoras para aumentar la robustez técnica de la aplicación:

*   **Manejo de Errores y Logging Mejorado:**
    *   Implementar un sistema de logging más detallado que capture errores, advertencias y depuración en un archivo o consola, facilitando la depuración futura.
    *   Centralizar el manejo de excepciones para presentar mensajes de error más amigables al usuario sin que la aplicación se cierre inesperadamente.
*   **Configuración Externa:**
    *   Externalizar parámetros configurables (ej. número de iteraciones para optimizadores, tolerancias, límites de búsqueda de círculos) a un archivo de configuración (YAML/JSON) para facilitar ajustes sin modificar el código. Esto es crucial para la flexibilidad del área de búsqueda de círculos.
*   **Validación de Entrada Robusta:**
    *   Implementar una capa de validación de datos más allá de la GUI, asegurando que los datos pasados a las funciones de cálculo sean siempre válidos y dentro de rangos esperados.
*   **Modularización y Separación de Responsabilidades:**
    *   Revisar la estructura del código para asegurar una clara separación entre la lógica de la GUI, la lógica de negocio (cálculos) y la manipulación de datos. Esto facilitará el mantenimiento y la adición de nuevas funcionalidades.
*   **Pruebas de Rendimiento:**
    *   Considerar la adición de pruebas de rendimiento para identificar cuellos de botella en los cálculos, especialmente con geometrías complejas o un gran número de círculos.
*   **Uso de Tipos (Type Hinting):**
    *   Continuar y expandir el uso de type hinting en todo el código Python para mejorar la legibilidad, facilitar la depuración y permitir el uso de herramientas de análisis estático.

---

## Instrucciones para el Agente IA

1.  **Prioridad:** Aborda los errores críticos en el orden de impacto, comenzando por los que bloquean la funcionalidad.
2.  **TDD:** Para cada error, escribe los tests de reproducción *antes* de implementar la solución.
3.  **Detalle:** Cada test debe ser concreto, con entradas y salidas esperadas bien definidas.
4.  **Reporte:** Genera informes de prueba claros. Si una prueba falla, proporciona información suficiente para depurar.
5.  **Automatización:** Las pruebas deben ser completamente automatizadas.
6.  **Colaboración:** Si encuentras ambigüedades o necesitas aclaraciones, pregunta.
7.  **Actualización de Código:** Documenta los bugs y, si es posible, crea una solución, pero el enfoque principal es la creación de pruebas y la resolución de los problemas actuales.
8.  **Implementación de Mejoras:** Una vez que la aplicación sea funcional y estable, comienza a implementar las mejoras técnicas recomendadas.

¡Comienza a construir una aplicación robusta y confiable!