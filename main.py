"""
Sistema de Análisis de Estabilidad de Taludes
==============================================

Interfaz principal para el análisis de estabilidad de taludes
utilizando los métodos de Fellenius y Bishop Modificado.

Autor: Sistema de Análisis Geotécnico
Versión: 1.0
"""

import sys
import os
import math
from typing import Optional, Dict, Any

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports del sistema
from core.fellenius import fellenius_talud_homogeneo
from core.bishop import bishop_talud_homogeneo, comparar_bishop_fellenius
from core.geometry import crear_perfil_simple, crear_nivel_freatico_horizontal
from visualization.plotting import *
from data.models import CirculoFalla
import matplotlib.pyplot as plt


class SistemaAnalisisEstabilidad:
    """
    Clase principal para el análisis de estabilidad de taludes.
    """
    
    def __init__(self):
        """Inicializar el sistema."""
        self.version = "1.0"
        self.configurar_visualizacion()
        print(f"🏗️  Sistema de Análisis de Estabilidad de Taludes v{self.version}")
        print("=" * 60)
    
    def configurar_visualizacion(self):
        """Configurar el sistema de visualización."""
        try:
            configurar_estilo_grafico()
            self.config_grafico = ConfiguracionGrafico(figsize=(14, 10))
            print("✅ Sistema de visualización configurado")
        except Exception as e:
            print(f"⚠️ Error configurando visualización: {e}")
            self.config_grafico = None
    
    def mostrar_menu_principal(self):
        """Mostrar el menú principal del sistema."""
        print("\n🎯 MENÚ PRINCIPAL")
        print("-" * 30)
        print("1. 📊 Análisis Rápido")
        print("2. 🔬 Análisis Detallado")
        print("3. 💧 Análisis con Agua")
        print("4. 📈 Análisis Paramétrico")
        print("5. 📋 Ejemplos Predefinidos")
        print("6. ℹ️  Información del Sistema")
        print("0. 🚪 Salir")
        print("-" * 30)
    
    def analisis_rapido(self):
        """Realizar un análisis rápido con parámetros típicos."""
        print("\n📊 ANÁLISIS RÁPIDO")
        print("=" * 40)
        
        try:
            # Solicitar parámetros básicos
            print("Ingrese los parámetros básicos del talud:")
            
            altura = float(input("Altura del talud (m): "))
            angulo_talud = float(input("Ángulo del talud (grados): "))
            cohesion = float(input("Cohesión del suelo (kPa): "))
            phi_grados = float(input("Ángulo de fricción (grados): "))
            gamma = float(input("Peso específico (kN/m³): "))
            
            print(f"\n🔄 Analizando talud de {altura}m con ángulo {angulo_talud}°...")
            
            # Análisis Bishop
            resultado = bishop_talud_homogeneo(
                altura=altura,
                angulo_talud=angulo_talud,
                cohesion=cohesion,
                phi_grados=phi_grados,
                gamma=gamma,
                num_dovelas=10
            )
            
            # Mostrar resultados
            self.mostrar_resultados_rapidos(resultado)
            
            # Generar visualización
            if self.config_grafico:
                self.generar_visualizacion_rapida(altura, angulo_talud, resultado)
            
            return True
            
        except ValueError:
            print("❌ Error: Ingrese valores numéricos válidos")
            return False
        except Exception as e:
            print(f"❌ Error en análisis: {e}")
            return False
    
    def mostrar_resultados_rapidos(self, resultado):
        """Mostrar resultados de análisis rápido."""
        fs = resultado.factor_seguridad
        
        print(f"\n📊 RESULTADOS DEL ANÁLISIS")
        print("-" * 35)
        print(f"Factor de Seguridad: {fs:.3f}")
        print(f"Iteraciones: {resultado.iteraciones}")
        print(f"Convergió: {'Sí' if resultado.convergio else 'No'}")
        print(f"Dovelas analizadas: {len(resultado.dovelas)}")
        
        # Interpretación
        if fs >= 2.0:
            estado = "🟢 MUY SEGURO"
            recomendacion = "Talud muy estable, proceder con confianza"
        elif fs >= 1.5:
            estado = "🟢 SEGURO"
            recomendacion = "Talud estable, condiciones aceptables"
        elif fs >= 1.3:
            estado = "🟡 ACEPTABLE"
            recomendacion = "Talud marginalmente estable, monitorear"
        elif fs >= 1.0:
            estado = "🟠 MARGINAL"
            recomendacion = "Talud en límite, considerar refuerzo"
        else:
            estado = "🔴 INESTABLE"
            recomendacion = "Talud inestable, rediseño necesario"
        
        print(f"\nEstado: {estado}")
        print(f"Recomendación: {recomendacion}")
    
    def generar_visualizacion_rapida(self, altura, angulo_talud, resultado):
        """Generar visualización para análisis rápido."""
        try:
            # Crear geometría
            longitud_base = altura / math.tan(math.radians(angulo_talud))
            perfil = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
            circulo = CirculoFalla(xc=longitud_base * 0.4, yc=altura * 1.1, radio=1.5 * altura)
            
            # Generar gráfico
            fig = graficar_resultado_bishop(perfil, circulo, resultado, self.config_grafico)
            print("✅ Gráfico generado exitosamente")
            
            # Cerrar para liberar memoria
            plt.close('all')
            
        except Exception as e:
            print(f"⚠️ Error generando gráfico: {e}")
    
    def analisis_detallado(self):
        """Realizar análisis detallado con comparación de métodos."""
        print("\n🔬 ANÁLISIS DETALLADO")
        print("=" * 40)
        
        try:
            # Solicitar parámetros detallados
            print("Ingrese los parámetros del talud:")
            
            altura = float(input("Altura del talud (m): "))
            angulo_talud = float(input("Ángulo del talud (grados): "))
            cohesion = float(input("Cohesión del suelo (kPa): "))
            phi_grados = float(input("Ángulo de fricción (grados): "))
            gamma = float(input("Peso específico (kN/m³): "))
            num_dovelas = int(input("Número de dovelas (8-20): "))
            
            print(f"\n🔄 Realizando análisis completo...")
            
            # Análisis Bishop
            print("Ejecutando método de Bishop...")
            resultado_bishop = bishop_talud_homogeneo(
                altura=altura,
                angulo_talud=angulo_talud,
                cohesion=cohesion,
                phi_grados=phi_grados,
                gamma=gamma,
                num_dovelas=num_dovelas
            )
            
            # Análisis Fellenius (si es posible)
            print("Ejecutando método de Fellenius...")
            try:
                resultado_fellenius = fellenius_talud_homogeneo(
                    altura=altura,
                    angulo_talud=angulo_talud,
                    cohesion=cohesion,
                    phi_grados=phi_grados,
                    gamma=gamma,
                    num_dovelas=num_dovelas
                )
                fellenius_ok = True
            except Exception as e:
                print(f"⚠️ Fellenius no disponible: {e}")
                resultado_fellenius = None
                fellenius_ok = False
            
            # Mostrar resultados detallados
            self.mostrar_resultados_detallados(resultado_bishop, resultado_fellenius)
            
            # Generar visualización completa
            if self.config_grafico:
                self.generar_visualizacion_detallada(altura, angulo_talud, 
                                                   resultado_bishop, resultado_fellenius)
            
            return True
            
        except ValueError:
            print("❌ Error: Ingrese valores numéricos válidos")
            return False
        except Exception as e:
            print(f"❌ Error en análisis detallado: {e}")
            return False
    
    def mostrar_resultados_detallados(self, resultado_bishop, resultado_fellenius=None):
        """Mostrar resultados detallados."""
        print(f"\n📊 RESULTADOS DETALLADOS")
        print("=" * 45)
        
        # Resultados Bishop
        print(f"🔹 MÉTODO DE BISHOP MODIFICADO")
        print(f"   Factor de Seguridad: {resultado_bishop.factor_seguridad:.3f}")
        print(f"   Iteraciones: {resultado_bishop.iteraciones}")
        print(f"   Convergió: {'Sí' if resultado_bishop.convergio else 'No'}")
        print(f"   Dovelas: {len(resultado_bishop.dovelas)}")
        
        # Resultados Fellenius si están disponibles
        if resultado_fellenius:
            print(f"\n🔹 MÉTODO DE FELLENIUS")
            print(f"   Factor de Seguridad: {resultado_fellenius.factor_seguridad:.3f}")
            print(f"   Momento Resistente: {resultado_fellenius.momento_resistente:.1f} kN·m")
            print(f"   Momento Actuante: {resultado_fellenius.momento_actuante:.1f} kN·m")
            
            # Comparación
            diferencia = ((resultado_bishop.factor_seguridad - resultado_fellenius.factor_seguridad) / 
                         resultado_fellenius.factor_seguridad) * 100
            
            print(f"\n🔹 COMPARACIÓN DE MÉTODOS")
            print(f"   Diferencia: {diferencia:+.1f}%")
            
            if abs(diferencia) < 5:
                print(f"   ✅ Métodos consistentes")
            elif diferencia > 0:
                print(f"   ℹ️  Bishop menos conservador")
            else:
                print(f"   ℹ️  Fellenius menos conservador")
        
        # Análisis de dovelas críticas
        self.analizar_dovelas_criticas(resultado_bishop)
    
    def analizar_dovelas_criticas(self, resultado):
        """Analizar dovelas más críticas."""
        if not resultado.dovelas:
            return
        
        print(f"\n🔹 ANÁLISIS DE DOVELAS")
        
        # Encontrar dovela con mayor peso
        dovela_pesada = max(resultado.dovelas, key=lambda d: d.peso)
        
        # Encontrar dovela con mayor ángulo
        dovela_inclinada = max(resultado.dovelas, key=lambda d: abs(d.angulo_alpha))
        
        print(f"   Dovela más pesada: {dovela_pesada.peso:.1f} kN (x={dovela_pesada.x_centro:.1f}m)")
        print(f"   Dovela más inclinada: {math.degrees(dovela_inclinada.angulo_alpha):.1f}° (x={dovela_inclinada.x_centro:.1f}m)")
        print(f"   Rango de pesos: {min(d.peso for d in resultado.dovelas):.1f} - {max(d.peso for d in resultado.dovelas):.1f} kN")
    
    def generar_visualizacion_detallada(self, altura, angulo_talud, resultado_bishop, resultado_fellenius=None):
        """Generar visualización detallada."""
        try:
            # Crear geometría
            longitud_base = altura / math.tan(math.radians(angulo_talud))
            perfil = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
            circulo = CirculoFalla(xc=longitud_base * 0.4, yc=altura * 1.1, radio=1.5 * altura)
            
            # Gráfico Bishop
            fig1 = graficar_resultado_bishop(perfil, circulo, resultado_bishop, self.config_grafico)
            print("✅ Gráfico Bishop generado")
            
            # Gráfico comparativo si Fellenius está disponible
            if resultado_fellenius:
                fig2 = graficar_comparacion_metodos(perfil, circulo, resultado_fellenius, 
                                                  resultado_bishop, self.config_grafico)
                print("✅ Gráfico comparativo generado")
            
            # Gráfico de convergencia
            if hasattr(resultado_bishop, 'historial_fs') and resultado_bishop.historial_fs:
                fig3 = graficar_convergencia_bishop(resultado_bishop.historial_fs, self.config_grafico)
                print("✅ Gráfico de convergencia generado")
            
            # Cerrar gráficos
            plt.close('all')
            
        except Exception as e:
            print(f"⚠️ Error en visualización detallada: {e}")
    
    def ejecutar_ejemplos(self):
        """Ejecutar ejemplos predefinidos."""
        print("\n📋 EJEMPLOS PREDEFINIDOS")
        print("=" * 35)
        print("1. 🏗️  Talud de carretera (caso simple)")
        print("2. 💧 Talud con nivel freático")
        print("3. 📊 Análisis paramétrico")
        print("0. ⬅️  Volver al menú principal")
        
        try:
            opcion = input("\nSeleccione un ejemplo: ")
            
            if opcion == "1":
                print("\n🔄 Ejecutando ejemplo de talud simple...")
                os.system("python examples/caso_simple.py")
            elif opcion == "2":
                print("\n🔄 Ejecutando ejemplo con agua...")
                os.system("python examples/caso_con_agua.py")
            elif opcion == "3":
                print("\n🔄 Ejecutando análisis paramétrico...")
                self.analisis_parametrico_interactivo()
            elif opcion == "0":
                return
            else:
                print("❌ Opción no válida")
                
        except Exception as e:
            print(f"❌ Error ejecutando ejemplo: {e}")
    
    def analisis_parametrico_interactivo(self):
        """Análisis paramétrico interactivo."""
        print("\n📈 ANÁLISIS PARAMÉTRICO")
        print("=" * 35)
        
        try:
            # Parámetros base
            altura = float(input("Altura base del talud (m): "))
            angulo_talud = float(input("Ángulo base del talud (grados): "))
            phi_grados = float(input("Ángulo de fricción base (grados): "))
            gamma = float(input("Peso específico base (kN/m³): "))
            
            # Parámetro a variar
            print("\nSeleccione parámetro a variar:")
            print("1. Cohesión")
            print("2. Ángulo de fricción")
            print("3. Altura del talud")
            
            param_opcion = input("Opción: ")
            
            if param_opcion == "1":
                self.variar_cohesion(altura, angulo_talud, phi_grados, gamma)
            elif param_opcion == "2":
                self.variar_friccion(altura, angulo_talud, gamma)
            elif param_opcion == "3":
                self.variar_altura(angulo_talud, phi_grados, gamma)
            else:
                print("❌ Opción no válida")
                
        except ValueError:
            print("❌ Error: Ingrese valores numéricos válidos")
        except Exception as e:
            print(f"❌ Error en análisis paramétrico: {e}")
    
    def variar_cohesion(self, altura, angulo_talud, phi_grados, gamma):
        """Variar cohesión y analizar efecto."""
        cohesiones = [10, 15, 20, 25, 30, 35, 40, 45, 50]
        
        print(f"\n📊 VARIACIÓN DE COHESIÓN")
        print(f"{'c (kPa)':<8} {'Fs':<8} {'Iteraciones':<12} {'Estado'}")
        print("-" * 40)
        
        for c in cohesiones:
            try:
                resultado = bishop_talud_homogeneo(
                    altura=altura,
                    angulo_talud=angulo_talud,
                    cohesion=c,
                    phi_grados=phi_grados,
                    gamma=gamma,
                    num_dovelas=8
                )
                
                fs = resultado.factor_seguridad
                iter_count = resultado.iteraciones
                
                if fs >= 1.5:
                    estado = "SEGURO"
                elif fs >= 1.3:
                    estado = "ACEPTABLE"
                elif fs >= 1.0:
                    estado = "MARGINAL"
                else:
                    estado = "INESTABLE"
                
                print(f"{c:<8} {fs:<8.3f} {iter_count:<12} {estado}")
                
            except Exception:
                print(f"{c:<8} {'ERROR':<8} {'-':<12} {'FALLO'}")
    
    def mostrar_informacion_sistema(self):
        """Mostrar información del sistema."""
        print(f"\nℹ️  INFORMACIÓN DEL SISTEMA")
        print("=" * 40)
        print(f"Versión: {self.version}")
        print(f"Métodos implementados:")
        print(f"  • Método de Fellenius (ordinario)")
        print(f"  • Método de Bishop Modificado")
        print(f"Capacidades:")
        print(f"  • Análisis de taludes homogéneos")
        print(f"  • Consideración de nivel freático")
        print(f"  • Visualización gráfica avanzada")
        print(f"  • Análisis paramétrico")
        print(f"  • Generación de reportes")
        print(f"Desarrollado con Python y matplotlib")
    
    def ejecutar(self):
        """Ejecutar el sistema principal."""
        while True:
            try:
                self.mostrar_menu_principal()
                opcion = input("\nSeleccione una opción: ")
                
                if opcion == "1":
                    self.analisis_rapido()
                elif opcion == "2":
                    self.analisis_detallado()
                elif opcion == "3":
                    print("💧 Análisis con agua - Ejecute: python examples/caso_con_agua.py")
                elif opcion == "4":
                    self.analisis_parametrico_interactivo()
                elif opcion == "5":
                    self.ejecutar_ejemplos()
                elif opcion == "6":
                    self.mostrar_informacion_sistema()
                elif opcion == "0":
                    print("\n👋 ¡Gracias por usar el Sistema de Análisis de Estabilidad!")
                    break
                else:
                    print("❌ Opción no válida. Intente nuevamente.")
                
                # Pausa para leer resultados
                if opcion in ["1", "2", "4", "6"]:
                    input("\nPresione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Sistema terminado por el usuario")
                break
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                input("Presione Enter para continuar...")


def main():
    """Función principal."""
    try:
        sistema = SistemaAnalisisEstabilidad()
        sistema.ejecutar()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        print("El sistema no pudo iniciarse correctamente")


if __name__ == "__main__":
    main()
