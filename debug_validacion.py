#!/usr/bin/env python3
"""
Debug específico para el problema de validación de dovelas
"""

import sys
import os

# Agregar path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.validation import validar_conjunto_dovelas
from data.models import Estrato, CirculoFalla
from core.geometry import crear_perfil_simple, crear_dovelas

def debug_validacion_dovelas():
    """Debug del problema específico"""
    print("🔍 DEBUG: Validación de Dovelas")
    print("=" * 40)
    
    # Recrear exactamente el caso que falla
    circulo = CirculoFalla(xc=10.0, yc=8.0, radio=6.0)
    perfil = crear_perfil_simple(0.0, 10.0, 20.0, 0.0, 10)
    estrato = Estrato(cohesion=10.0, phi_grados=30.0, gamma=18.0, nombre="Arena")
    
    print(f"Círculo: xc={circulo.xc}, yc={circulo.yc}, r={circulo.radio}")
    print(f"Perfil: {len(perfil)} puntos")
    print(f"Estrato: c={estrato.cohesion}, φ={estrato.phi_grados}°")
    
    # Crear dovelas
    print("\n⚙️ Creando dovelas...")
    dovelas_validas = crear_dovelas(circulo, perfil, estrato, num_dovelas=8)
    print(f"Dovelas creadas: {len(dovelas_validas)}")
    
    # Mostrar detalles de dovelas
    print("\n📊 Detalles de dovelas:")
    for i, dovela in enumerate(dovelas_validas):
        print(f"  Dovela {i+1}: x_centro={dovela.x_centro:.2f}, ancho={dovela.ancho:.2f}, "
              f"altura={dovela.altura:.2f}, peso={dovela.peso:.1f}")
    
    # Probar validación paso a paso
    print(f"\n🧪 Probando validación...")
    resultado = validar_conjunto_dovelas(dovelas_validas)
    
    print(f"✅ Es válido: {resultado.es_valido}")
    print(f"📝 Mensaje: {resultado.mensaje}")
    print(f"🔧 Código error: {resultado.codigo_error}")
    
    # Si falla, investigar por qué
    if not resultado.es_valido:
        print(f"\n❌ FALLA - Investigando razón:")
        print(f"   Número de dovelas: {len(dovelas_validas)}")
        
        # Revisar dovelas individuales
        for i, dovela in enumerate(dovelas_validas):
            try:
                from data.validation import validar_dovela_critica
                res_individual = validar_dovela_critica(dovela)
                if not res_individual.es_valido:
                    print(f"   ❌ Dovela {i+1} inválida: {res_individual.mensaje}")
            except Exception as e:
                print(f"   ⚠️ Error al validar dovela {i+1}: {e}")

if __name__ == "__main__":
    debug_validacion_dovelas()
