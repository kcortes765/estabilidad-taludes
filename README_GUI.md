# Interfaz Gráfica - Sistema de Análisis de Estabilidad de Taludes

## Descripción

Interfaz gráfica moderna y completa para el sistema de análisis de estabilidad de taludes, implementada con CustomTkinter y matplotlib. Proporciona una experiencia de usuario intuitiva para realizar análisis geotécnicos profesionales.

## Características Principales

### 🎯 Funcionalidades Core
- **Métodos de Análisis**: Bishop Modificado y Fellenius
- **Análisis en Tiempo Real**: Visualización inmediata de resultados
- **Análisis Paramétrico**: Estudios de sensibilidad automatizados
- **Nivel Freático**: Consideración de condiciones saturadas
- **Exportación Completa**: Gráficos y reportes en múltiples formatos

### 🎨 Interfaz de Usuario
- **Diseño Moderno**: Interfaz limpia y profesional con CustomTkinter
- **Visualización Avanzada**: Gráficos interactivos con matplotlib
- **Controles Intuitivos**: Sliders, entradas numéricas y controles visuales
- **Feedback en Tiempo Real**: Indicadores de estado y progreso
- **Responsive Design**: Adaptable a diferentes tamaños de pantalla

### 📊 Visualización
- **Geometría del Talud**: Perfil, círculo de falla y dovelas
- **Resultados de Análisis**: Factores de seguridad y fuerzas
- **Comparación de Métodos**: Bishop vs Fellenius
- **Convergencia**: Gráficos de iteraciones y convergencia
- **Análisis Paramétrico**: Gráficos de sensibilidad

## Instalación

### 1. Dependencias GUI
```bash
# Instalar dependencias específicas para la GUI
pip install -r requirements_gui.txt

# O instalar manualmente:
pip install customtkinter matplotlib pillow
```

### 2. Verificar Instalación
```bash
# Ejecutar script de verificación
python run_gui.py
```

## Uso

### Inicio Rápido
```bash
# Ejecutar la aplicación GUI
python run_gui.py
```

### Flujo de Trabajo Típico

1. **Configurar Parámetros**
   - Ajustar geometría del talud (altura, ángulo)
   - Definir propiedades del suelo (cohesión, fricción, peso específico)
   - Configurar parámetros de análisis (número de dovelas)
   - Opcional: Activar nivel freático

2. **Ejecutar Análisis**
   - Presionar "Analizar Talud" para cálculos Bishop y Fellenius
   - Observar resultados en tiempo real
   - Revisar visualizaciones en las pestañas

3. **Análisis Avanzado**
   - Usar "Análisis Paramétrico" para estudios de sensibilidad
   - Comparar diferentes configuraciones
   - Analizar convergencia del método Bishop

4. **Exportar Resultados**
   - Guardar gráficos en alta resolución
   - Generar reportes de texto
   - Exportar datos para análisis posterior

## Estructura de la GUI

### Archivos Principales
```
gui_app.py          # Aplicación principal y lógica de control
gui_components.py   # Componentes de interfaz (paneles, controles)
gui_plotting.py     # Integración con matplotlib y visualización
gui_dialogs.py      # Diálogos y utilidades auxiliares
run_gui.py         # Script de inicio con verificaciones
```

### Componentes de la Interfaz

#### Panel de Parámetros
- **Geometría**: Altura y ángulo del talud
- **Suelo**: Cohesión, ángulo de fricción, peso específico
- **Análisis**: Número de dovelas, tolerancia
- **Agua**: Activación y altura del nivel freático

#### Panel de Resultados
- **Bishop**: Factor de seguridad, iteraciones, convergencia
- **Fellenius**: Factor de seguridad, momentos
- **Estado**: Clasificación de estabilidad con códigos de color
- **Comparación**: Diferencias entre métodos

#### Panel de Herramientas
- **Análisis**: Ejecutar cálculos, análisis paramétrico
- **Exportación**: Guardar gráficos y reportes
- **Utilidades**: Limpiar resultados, ayuda

#### Panel de Visualización
- **Geometría**: Perfil del talud y círculo de falla
- **Análisis**: Dovelas, fuerzas y resultados
- **Comparación**: Bishop vs Fellenius
- **Convergencia**: Iteraciones y convergencia

## Características Técnicas

### Arquitectura
- **Modular**: Separación clara de responsabilidades
- **Threaded**: Análisis en hilos separados para UI responsiva
- **Event-Driven**: Actualizaciones en tiempo real
- **Extensible**: Fácil agregar nuevas funcionalidades

### Validaciones
- **Parámetros**: Rangos geotécnicos válidos
- **Geometría**: Verificación de configuraciones válidas
- **Convergencia**: Control de iteraciones Bishop
- **Resultados**: Validación de factores de seguridad

### Rendimiento
- **Cálculos Rápidos**: Optimización para análisis en tiempo real
- **Visualización Eficiente**: Actualización selectiva de gráficos
- **Memoria**: Gestión eficiente de recursos
- **Responsive**: Interfaz fluida y sin bloqueos

## Interpretación de Resultados

### Factor de Seguridad
- **Fs ≥ 2.0**: 🟢 MUY SEGURO - Talud muy estable
- **Fs ≥ 1.5**: 🟢 SEGURO - Condiciones aceptables
- **Fs ≥ 1.3**: 🟡 ACEPTABLE - Monitorear condiciones
- **Fs < 1.3**: 🔴 MARGINAL - Considerar estabilización

### Comparación de Métodos
- **Bishop**: Más preciso, considera fuerzas entre dovelas
- **Fellenius**: Más conservador, cálculo directo
- **Diferencia Típica**: 5-15% (Bishop menos conservador)

### Análisis Paramétrico
- **Sensibilidad**: Identificar parámetros críticos
- **Optimización**: Encontrar configuraciones óptimas
- **Riesgo**: Evaluar variabilidad de resultados

## Solución de Problemas

### Errores Comunes

1. **Error de Importación**
   ```bash
   # Verificar instalación de dependencias
   pip install customtkinter matplotlib pillow
   ```

2. **Convergencia Bishop**
   - Reducir número de dovelas
   - Ajustar tolerancia de convergencia
   - Verificar parámetros geotécnicos

3. **Visualización**
   - Verificar matplotlib backend
   - Actualizar drivers gráficos
   - Reducir resolución si es necesario

### Rendimiento
- **Análisis Lento**: Reducir número de dovelas
- **Memoria Alta**: Cerrar gráficos no utilizados
- **UI Lenta**: Verificar hilos de análisis

## Desarrollo y Extensión

### Agregar Nuevas Funcionalidades
1. Crear componentes en `gui_components.py`
2. Agregar lógica en `gui_app.py`
3. Implementar visualización en `gui_plotting.py`
4. Crear diálogos en `gui_dialogs.py`

### Personalización
- Modificar temas en configuración CustomTkinter
- Ajustar colores y estilos en archivos de componentes
- Agregar nuevos tipos de gráficos en módulo de plotting

## Soporte

### Documentación
- Código completamente documentado
- Ejemplos de uso incluidos
- Guías de desarrollo disponibles

### Contacto
Sistema desarrollado para análisis geotécnico profesional.
Basado en estándares de la ingeniería geotécnica.

---

**Versión**: 2.0  
**Fecha**: 2024  
**Framework**: CustomTkinter + matplotlib  
**Python**: 3.8+
