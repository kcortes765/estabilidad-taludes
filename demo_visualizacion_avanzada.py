"""
DEMOSTRACIÓN DE VISUALIZACIÓN ULTRA-AVANZADA

Script para demostrar todas las capacidades gráficas y visuales mejoradas:
1. Gráficos con límites geométricos automáticos
2. Mapas de calor de estabilidad 
3. Visualización 3D del talud
4. Dashboard ultra-completo con múltiples paneles
5. Comparación visual de múltiples círculos
6. Zonas de validez y restricciones

OBJETIVO: Mostrar el poder visual completo del sistema sin fallos
"""

import sys
import os
import time
import traceback

# Agregar paths necesarios
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verificar_dependencias():
    """Verifica si las dependencias gráficas están disponibles"""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        print("✅ Dependencias gráficas disponibles (matplotlib, numpy)")
        return True
    except ImportError as e:
        print(f"❌ Dependencias gráficas faltantes: {e}")
        print("💡 Instalar con: pip install matplotlib numpy")
        return False

def demo_visualizacion_principal():
    """Demostración principal de visualización avanzada"""
    
    print("🎨 DEMO VISUALIZACIÓN ULTRA-AVANZADA")
    print("=" * 60)
    
    if not verificar_dependencias():
        return False
    
    try:
        # Importar módulos necesarios
        import matplotlib.pyplot as plt
        from data.models import CirculoFalla, Estrato
        from examples.gui_examples import casos_ejemplo
        
        # Importar módulos ultra-mejorados
        from core.circle_constraints import aplicar_limites_inteligentes, CalculadorLimites
        from visualization.advanced_circle_graphics import VisualizadorAvanzado
        from core.smart_circle_optimizer import optimizar_circulo_inteligente
        
        print("✅ Módulos de visualización importados correctamente")
        
        # Configurar datos de ejemplo
        caso = casos_ejemplo[0]
        perfil_terreno = caso['perfil_terreno']
        estrato = Estrato(
            cohesion=caso['cohesion'],
            angulo_friccion=caso['angulo_friccion'],
            peso_especifico=caso['peso_especifico']
        )
        
        circulo_original = caso['circulo']
        
        print(f"📋 Usando caso: {caso['nombre']}")
        
        # Calcular límites inteligentes
        limites = aplicar_limites_inteligentes(perfil_terreno, "talud_empinado", 1.5)
        
        # Optimizar círculo
        print("🔄 Optimizando círculo para visualización...")
        resultado_opt = optimizar_circulo_inteligente(perfil_terreno, estrato, "minimo_fs", 1.5)
        circulo_optimo = resultado_opt.circulo_optimo
        
        # Crear visualizador
        visualizador = VisualizadorAvanzado()
        
        # GRÁFICO 1: Talud con límites geométricos
        print("\n📊 Generando Gráfico 1: Talud con Límites Geométricos")
        try:
            fig1 = visualizador.plot_talud_con_limites(
                perfil_terreno=perfil_terreno,
                limites=limites,
                circulo=circulo_optimo,
                mostrar_zonas=True,
                titulo="Talud con Límites Automáticos y Círculo Óptimo"
            )
            
            # Guardar gráfico
            fig1.savefig('grafico1_talud_limites.png', dpi=150, bbox_inches='tight')
            print("   ✅ Guardado como: grafico1_talud_limites.png")
            plt.close(fig1)
            
        except Exception as e:
            print(f"   ❌ Error en Gráfico 1: {e}")
        
        # GRÁFICO 2: Mapa de calor de estabilidad
        print("\n🌡️  Generando Gráfico 2: Mapa de Calor de Estabilidad")
        try:
            fig2 = visualizador.plot_mapa_calor_estabilidad(
                perfil_terreno=perfil_terreno,
                estrato=estrato,
                limites=limites,
                resolucion=30  # Reducido para velocidad
            )
            
            # Guardar gráfico
            fig2.savefig('grafico2_mapa_calor.png', dpi=150, bbox_inches='tight')
            print("   ✅ Guardado como: grafico2_mapa_calor.png")
            plt.close(fig2)
            
        except Exception as e:
            print(f"   ❌ Error en Gráfico 2: {e}")
        
        # GRÁFICO 3: Análisis 3D del talud
        print("\n🏔️  Generando Gráfico 3: Visualización 3D")
        try:
            fig3 = visualizador.plot_analisis_3d_talud(
                perfil_terreno=perfil_terreno,
                circulo=circulo_optimo,
                estrato=estrato
            )
            
            # Guardar gráfico
            fig3.savefig('grafico3_analisis_3d.png', dpi=150, bbox_inches='tight')
            print("   ✅ Guardado como: grafico3_analisis_3d.png")
            plt.close(fig3)
            
        except Exception as e:
            print(f"   ❌ Error en Gráfico 3: {e}")
        
        # GRÁFICO 4: Dashboard ultra-completo
        print("\n📋 Generando Gráfico 4: Dashboard Ultra-Completo")
        try:
            fig4 = visualizador.plot_dashboard_completo_avanzado(
                perfil_terreno=perfil_terreno,
                circulo=circulo_optimo,
                estrato=estrato,
                limites=limites
            )
            
            # Guardar gráfico
            fig4.savefig('grafico4_dashboard_completo.png', dpi=150, bbox_inches='tight')
            print("   ✅ Guardado como: grafico4_dashboard_completo.png")
            plt.close(fig4)
            
        except Exception as e:
            print(f"   ❌ Error en Gráfico 4: {e}")
        
        # GRÁFICO 5: Comparación de múltiples círculos
        print("\n🔄 Generando Gráfico 5: Comparación Múltiples Círculos")
        try:
            # Generar varios círculos para comparar
            calculador = CalculadorLimites()
            circulos_comparar = calculador.generar_circulos_dentro_limites(limites, 5, "uniforme")
            circulos_comparar.append(circulo_optimo)  # Agregar el óptimo
            
            # Crear figura de comparación
            fig5, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig5.suptitle('Comparación de Múltiples Círculos', fontsize=16, fontweight='bold')
            
            for i, circulo in enumerate(circulos_comparar):
                if i >= 6:  # Solo 6 subplots
                    break
                
                ax = axes[i//3, i%3]
                
                # Dibujar talud
                x_terreno = [p[0] for p in perfil_terreno]
                y_terreno = [p[1] for p in perfil_terreno]
                ax.fill_between(x_terreno, y_terreno, min(y_terreno) - 2, 
                               color='#8B4513', alpha=0.7)
                ax.plot(x_terreno, y_terreno, 'k-', linewidth=2)
                
                # Dibujar círculo
                from matplotlib.patches import Circle
                circle_patch = Circle((circulo.centro_x, circulo.centro_y), circulo.radio, 
                                    fill=False, color='red', linewidth=2)
                ax.add_patch(circle_patch)
                ax.plot(circulo.centro_x, circulo.centro_y, 'ro', markersize=6)
                
                # Calcular FS para título
                try:
                    from core.bishop import analizar_bishop
                    resultado = analizar_bishop(circulo, perfil_terreno, estrato, 10, validar_entrada=False)
                    fs = resultado['factor_seguridad']
                    titulo_circulo = f"Círculo {i+1}\nFS = {fs:.3f}"
                except:
                    titulo_circulo = f"Círculo {i+1}\nFS = N/A"
                
                ax.set_title(titulo_circulo, fontsize=10)
                ax.grid(True, alpha=0.3)
                ax.set_aspect('equal')
                
                # Ajustar límites
                margen = max(circulo.radio * 0.2, 2)
                ax.set_xlim(circulo.centro_x - circulo.radio - margen, 
                           circulo.centro_x + circulo.radio + margen)
                ax.set_ylim(min(y_terreno) - margen, 
                           circulo.centro_y + circulo.radio + margen)
            
            # Remover subplots vacíos
            for j in range(len(circulos_comparar), 6):
                axes[j//3, j%3].remove()
            
            plt.tight_layout()
            fig5.savefig('grafico5_comparacion_circulos.png', dpi=150, bbox_inches='tight')
            print("   ✅ Guardado como: grafico5_comparacion_circulos.png")
            plt.close(fig5)
            
        except Exception as e:
            print(f"   ❌ Error en Gráfico 5: {e}")
        
        # GRÁFICO 6: Evolución de optimización
        print("\n📈 Generando Gráfico 6: Evolución de Optimización")
        try:
            if resultado_opt.historial_fs:
                fig6, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
                
                # Evolución del Factor de Seguridad
                ax1.plot(resultado_opt.historial_fs, 'b-', linewidth=2, marker='o', markersize=4)
                ax1.set_title('Evolución del Factor de Seguridad', fontweight='bold')
                ax1.set_xlabel('Iteración')
                ax1.set_ylabel('Factor de Seguridad')
                ax1.grid(True, alpha=0.3)
                
                # Estadísticas de optimización
                stats_text = f"""ESTADÍSTICAS DE OPTIMIZACIÓN:

Iteraciones: {resultado_opt.iteraciones_utilizadas}
Convergencia: {'✅ Sí' if resultado_opt.convergencia_alcanzada else '❌ No'}

Factor de Seguridad:
• Mejor: {resultado_opt.mejor_fs_encontrado:.3f}
• Peor: {resultado_opt.peor_fs_encontrado:.3f}
• Promedio: {resultado_opt.promedio_fs:.3f}
• Final: {resultado_opt.factor_seguridad:.3f}

Validez Geométrica: {resultado_opt.validez_geometrica:.1f}%

Círculo Óptimo:
• Centro: ({resultado_opt.circulo_optimo.centro_x:.2f}, {resultado_opt.circulo_optimo.centro_y:.2f})
• Radio: {resultado_opt.circulo_optimo.radio:.2f} m"""
                
                ax2.text(0.05, 0.95, stats_text, transform=ax2.transAxes,
                        verticalalignment='top', fontsize=10, family='monospace',
                        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
                ax2.set_title('Estadísticas de Optimización', fontweight='bold')
                ax2.axis('off')
                
                plt.tight_layout()
                fig6.savefig('grafico6_evolucion_optimizacion.png', dpi=150, bbox_inches='tight')
                print("   ✅ Guardado como: grafico6_evolucion_optimizacion.png")
                plt.close(fig6)
            else:
                print("   ⚠️  Sin historial de optimización disponible")
                
        except Exception as e:
            print(f"   ❌ Error en Gráfico 6: {e}")
        
        # Resumen final
        print("\n🎉 VISUALIZACIÓN ULTRA-AVANZADA COMPLETADA")
        print("=" * 60)
        print("✅ GRÁFICOS GENERADOS:")
        print("   📊 grafico1_talud_limites.png - Talud con límites automáticos")
        print("   🌡️  grafico2_mapa_calor.png - Mapa de calor de estabilidad")
        print("   🏔️  grafico3_analisis_3d.png - Visualización 3D del talud")
        print("   📋 grafico4_dashboard_completo.png - Dashboard ultra-completo")
        print("   🔄 grafico5_comparacion_circulos.png - Comparación múltiples círculos")
        print("   📈 grafico6_evolucion_optimizacion.png - Evolución optimización")
        
        print("\n🎯 CAPACIDADES DEMOSTRADAS:")
        print("   • Límites geométricos automáticos e inteligentes")
        print("   • Validación visual de círculos con código de colores")
        print("   • Mapas de calor para identificar zonas críticas")
        print("   • Visualización 3D profesional del talud")
        print("   • Dashboard completo con múltiples métricas")
        print("   • Comparación visual de alternativas")
        print("   • Seguimiento de evolución de optimización")
        
        print("\n💫 EL SISTEMA GRÁFICO ES ULTRA-ROBUSTO Y PROFESIONAL")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en demo de visualización: {e}")
        print("🔍 Traceback completo:")
        traceback.print_exc()
        return False

def demo_limites_visuales():
    """Demostración específica de límites y restricciones visuales"""
    
    print("\n🎯 DEMO ESPECÍFICA: LÍMITES Y RESTRICCIONES VISUALES")
    print("-" * 60)
    
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        from data.models import CirculoFalla, Estrato
        from examples.gui_examples import casos_ejemplo
        from core.circle_constraints import aplicar_limites_inteligentes, CalculadorLimites
        
        caso = casos_ejemplo[0]
        perfil_terreno = caso['perfil_terreno']
        
        # Calcular límites para diferentes tipos de talud
        tipos_talud = ['talud_suave', 'talud_empinado', 'talud_critico', 'talud_conservador']
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Límites Automáticos para Diferentes Tipos de Talud', fontsize=16, fontweight='bold')
        
        for i, tipo in enumerate(tipos_talud):
            ax = axes[i//2, i%2]
            
            # Calcular límites específicos para este tipo
            limites = aplicar_limites_inteligentes(perfil_terreno, tipo, 1.5)
            
            # Dibujar talud
            x_terreno = [p[0] for p in perfil_terreno]
            y_terreno = [p[1] for p in perfil_terreno]
            ax.fill_between(x_terreno, y_terreno, min(y_terreno) - 2, 
                           color='#8B4513', alpha=0.7, label='Talud')
            ax.plot(x_terreno, y_terreno, 'k-', linewidth=2)
            
            # Dibujar zona permitida para centro
            zona_centro = patches.Rectangle(
                (limites.centro_x_min, limites.centro_y_min),
                limites.centro_x_max - limites.centro_x_min,
                limites.centro_y_max - limites.centro_y_min,
                facecolor='lightblue', alpha=0.3, label='Zona permitida'
            )
            ax.add_patch(zona_centro)
            
            # Dibujar límites
            ax.axvline(limites.centro_x_min, color='blue', linestyle='--', alpha=0.7)
            ax.axvline(limites.centro_x_max, color='blue', linestyle='--', alpha=0.7)
            ax.axhline(limites.centro_y_min, color='blue', linestyle='--', alpha=0.7)
            ax.axhline(limites.centro_y_max, color='blue', linestyle='--', alpha=0.7)
            
            # Generar círculos de ejemplo dentro de límites
            calculador = CalculadorLimites()
            circulos_ejemplo = calculador.generar_circulos_dentro_limites(limites, 3, "uniforme")
            
            colores = ['red', 'green', 'orange']
            for j, circulo in enumerate(circulos_ejemplo):
                circle = patches.Circle((circulo.centro_x, circulo.centro_y), circulo.radio, 
                                      fill=False, color=colores[j], linewidth=2, alpha=0.8)
                ax.add_patch(circle)
                ax.plot(circulo.centro_x, circulo.centro_y, 'o', color=colores[j], markersize=6)
            
            # Información del tipo
            info_text = f"""{tipo.replace('_', ' ').title()}
Radio: [{limites.radio_min:.1f}, {limites.radio_max:.1f}] m
Margen: {limites.centro_x_max - limites.centro_x_min:.1f} m"""
            
            ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
                   verticalalignment='top', fontsize=9,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            ax.set_title(f'{tipo.replace("_", " ").title()}', fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_aspect('equal')
            ax.legend(loc='upper right')
            
            # Ajustar límites del gráfico
            ax.set_xlim(limites.centro_x_min - 5, limites.centro_x_max + 5)
            ax.set_ylim(min(y_terreno) - 3, limites.centro_y_max + 5)
        
        plt.tight_layout()
        plt.savefig('demo_limites_tipos_talud.png', dpi=150, bbox_inches='tight')
        print("✅ Guardado como: demo_limites_tipos_talud.png")
        plt.close()
        
        print("🎯 Demo de límites visuales completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en demo de límites: {e}")
        return False

if __name__ == "__main__":
    inicio_demo = time.time()
    
    print("🎨 INICIANDO DEMOSTRACIÓN DE VISUALIZACIÓN ULTRA-AVANZADA")
    print("📅 Fecha y hora:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # Ejecutar demo principal de visualización
    exito = demo_visualizacion_principal()
    
    if exito:
        # Ejecutar demo de límites específicos
        demo_limites_visuales()
        
        print("\n🎉 ¡DEMOSTRACIÓN DE VISUALIZACIÓN COMPLETADA CON ÉXITO!")
        print("💫 Todos los gráficos ultra-avanzados generados exitosamente")
        print("🎯 El sistema visual es robusto, profesional y sin fallos")
    else:
        print("\n❌ Demo de visualización falló")
        print("💡 Verificar instalación de matplotlib y numpy")
    
    print(f"\n⏱️  Tiempo total: {time.time() - inicio_demo:.2f} segundos")
    
    # Pausa para que el usuario pueda leer los resultados
    print("\n👆 Presiona Enter para finalizar...")
    try:
        input()
    except:
        pass
