"""
Script de diagnóstico para entender los problemas con dovelas inválidas
"""

from gui_examples import CASOS_EJEMPLO
from validacion_geometrica import ValidadorGeometrico, validar_caso_ejemplo
from gui_analysis import analizar_desde_gui
from core.geometry import CirculoFalla, crear_dovelas, Estrato
import matplotlib.pyplot as plt

def diagnosticar_caso(nombre_caso, caso):
    """Diagnostica un caso específico"""
    print(f"\n{'='*60}")
    print(f"🔍 DIAGNÓSTICO: {nombre_caso}")
    print(f"{'='*60}")
    
    # 1. Información básica del caso
    print(f"\n📋 PARÁMETROS DEL CASO:")
    print(f"   Altura: {caso['altura']} m")
    print(f"   Ángulo talud: {caso['angulo_talud']}°")
    print(f"   Centro: ({caso['centro_x']}, {caso['centro_y']})")
    print(f"   Radio: {caso['radio']} m")
    print(f"   Perfil: {len(caso['perfil_terreno'])} puntos")
    
    # 2. Validación geométrica
    print(f"\n🔧 VALIDACIÓN GEOMÉTRICA:")
    resultado_validacion = validar_caso_ejemplo(caso)
    print(f"   Estado: {resultado_validacion.mensaje}")
    print(f"   Dovelas estimadas: {resultado_validacion.dovelas_validas_estimadas}")
    
    # 3. Análisis real
    print(f"\n⚙️ ANÁLISIS REAL:")
    parametros_gui = {
        'altura': caso['altura'],
        'angulo_talud': caso['angulo_talud'],
        'cohesion': caso['cohesion'],
        'phi_grados': caso['phi_grados'],
        'gamma': caso['gamma'],
        'con_agua': caso['con_agua'],
        'nivel_freatico': caso['nivel_freatico'],
        'centro_x': caso['centro_x'],
        'centro_y': caso['centro_y'],
        'radio': caso['radio'],
        'perfil_terreno': caso['perfil_terreno']
    }
    
    resultado_analisis = analizar_desde_gui(parametros_gui)
    
    if resultado_analisis['valido']:
        print(f"   ✅ Análisis exitoso")
        print(f"   Bishop FS: {resultado_analisis['bishop']['factor_seguridad']:.3f}")
        print(f"   Fellenius FS: {resultado_analisis['fellenius']['factor_seguridad']:.3f}")
    else:
        print(f"   ❌ Análisis falló: {resultado_analisis['error']}")
        if 'traceback' in resultado_analisis:
            print(f"   Traceback: {resultado_analisis['traceback'][:200]}...")
    
    # 4. Análisis detallado de dovelas
    print(f"\n🔍 ANÁLISIS DETALLADO DE DOVELAS:")
    try:
        circulo = CirculoFalla(
            xc=caso['centro_x'],
            yc=caso['centro_y'],
            radio=caso['radio']
        )
        
        estrato = Estrato(
            cohesion=caso['cohesion'],
            phi_grados=caso['phi_grados'],
            gamma=caso['gamma']
        )
        
        # Intentar crear dovelas directamente
        dovelas = crear_dovelas(
            circulo=circulo,
            perfil_terreno=caso['perfil_terreno'],
            estrato=estrato,
            num_dovelas=10
        )
        
        print(f"   ✅ Se crearon {len(dovelas)} dovelas")
        
        # Analizar dovelas problemáticas
        dovelas_problematicas = []
        for i, dovela in enumerate(dovelas):
            if hasattr(dovela, 'valida') and not dovela.valida:
                dovelas_problematicas.append((i, dovela))
        
        if dovelas_problematicas:
            print(f"   ⚠️ {len(dovelas_problematicas)} dovelas problemáticas:")
            for i, dovela in dovelas_problematicas[:3]:  # Solo mostrar las primeras 3
                print(f"      Dovela {i}: X={dovela.x_centro:.2f}")
        else:
            print(f"   ✅ Todas las dovelas son válidas")
            
    except Exception as e:
        print(f"   ❌ Error creando dovelas: {str(e)}")
    
    # 5. Visualización
    print(f"\n📊 GENERANDO VISUALIZACIÓN...")
    try:
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Dibujar perfil del terreno
        perfil_x = [p[0] for p in caso['perfil_terreno']]
        perfil_y = [p[1] for p in caso['perfil_terreno']]
        ax.plot(perfil_x, perfil_y, 'b-', linewidth=2, label='Perfil terreno')
        
        # Dibujar círculo de falla
        import numpy as np
        theta = np.linspace(0, 2*np.pi, 100)
        circulo_x = caso['centro_x'] + caso['radio'] * np.cos(theta)
        circulo_y = caso['centro_y'] + caso['radio'] * np.sin(theta)
        ax.plot(circulo_x, circulo_y, 'r--', linewidth=2, label='Círculo de falla')
        
        # Marcar centro
        ax.plot(caso['centro_x'], caso['centro_y'], 'ro', markersize=8, label='Centro')
        
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_title(f'Geometría: {nombre_caso}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.axis('equal')
        
        # Guardar imagen
        filename = f"diagnostico_{nombre_caso.replace(' ', '_').replace('-', '_')}.png"
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ Imagen guardada: {filename}")
        
    except Exception as e:
        print(f"   ❌ Error en visualización: {str(e)}")

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO COMPLETO DE DOVELAS")
    print("="*60)
    
    # Diagnosticar cada caso
    for nombre_caso, caso in CASOS_EJEMPLO.items():
        diagnosticar_caso(nombre_caso, caso)
    
    print(f"\n{'='*60}")
    print("🏁 DIAGNÓSTICO COMPLETADO")
    print("="*60)
    print("\nRevise los archivos de imagen generados para análisis visual")

if __name__ == "__main__":
    main()
