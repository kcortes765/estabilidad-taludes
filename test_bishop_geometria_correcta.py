"""
Test con geometría correcta para Bishop.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import traceback
import math
from data.models import Estrato, CirculoFalla
from core.geometry import crear_perfil_simple
from core.bishop import analizar_bishop

def main():
    print("=== TEST BISHOP CON GEOMETRÍA CORRECTA ===")
    
    try:
        # Crear un talud típico
        altura = 12.0
        angulo_talud = 45.0  # 45 grados
        longitud_base = altura / math.tan(math.radians(angulo_talud))
        
        # Crear perfil con más extensión
        perfil = crear_perfil_simple(0.0, altura, longitud_base * 3, 0.0, 25)
        print(f"✅ Perfil creado: base {longitud_base * 3:.1f}m, altura {altura}m")
        
        # Crear círculo que pase por el pie del talud y salga por arriba
        # Centro más alejado y alto para generar una superficie de falla típica
        radio = altura * 1.8
        xc = longitud_base * 0.3  # Centro hacia atrás del talud
        yc = altura * 1.2  # Centro alto
        circulo = CirculoFalla(xc=xc, yc=yc, radio=radio)
        print(f"✅ Círculo creado: centro ({xc:.1f}, {yc:.1f}), radio {radio:.1f}m")
        
        # Verificar que el círculo intersecte apropiadamente
        x_pie_talud = longitud_base
        distancia_centro_pie = math.sqrt((xc - x_pie_talud)**2 + (yc - 0)**2)
        print(f"Distancia centro-pie talud: {distancia_centro_pie:.1f}m vs radio {radio:.1f}m")
        
        if distancia_centro_pie < radio:
            print("✅ El círculo pasa cerca del pie del talud")
        else:
            print("⚠️ El círculo podría no intersectar apropiadamente")
        
        # Crear estrato con parámetros típicos
        estrato = Estrato(cohesion=15.0, phi_grados=22.0, gamma=19.0, nombre="Arcilla")
        print("✅ Estrato creado (arcilla típica)")
        
        print("\nLlamando a analizar_bishop...")
        
        # Llamar función SIN validaciones para ver el resultado
        resultado = analizar_bishop(
            circulo=circulo,
            perfil_terreno=perfil,
            estrato=estrato,
            nivel_freatico=None,
            num_dovelas=10,
            factor_inicial=1.0,
            tolerancia=0.001,
            max_iteraciones=50,
            validar_entrada=False  # Sin validaciones para debug
        )
        
        print("✅ Análisis completado")
        print(f"Factor de seguridad: {resultado.factor_seguridad:.3f}")
        print(f"Convergió: {resultado.convergio}")
        print(f"Iteraciones: {resultado.iteraciones}")
        print(f"Dovelas: {len(resultado.dovelas)}")
        print(f"Advertencias: {len(resultado.advertencias)}")
        
        # Mostrar clasificación
        fs = resultado.factor_seguridad
        if fs < 1.0:
            clasificacion = "INESTABLE"
        elif fs < 1.3:
            clasificacion = "MARGINALMENTE ESTABLE"
        elif fs < 2.0:
            clasificacion = "ESTABLE"
        else:
            clasificacion = "MUY ESTABLE"
        
        print(f"Clasificación: {clasificacion}")
        
        if resultado.advertencias:
            print("\nAdvertencias:")
            for adv in resultado.advertencias:
                print(f"  - {adv}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
