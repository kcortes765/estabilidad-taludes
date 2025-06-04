"""
Script para diagnosticar problemas específicos con el cálculo de fuerzas
"""

from gui_examples import CASOS_EJEMPLO
from core.geometry import CirculoFalla, crear_dovelas, Estrato
from core.fellenius import analizar_fellenius
from core.bishop import analizar_bishop

def diagnosticar_fuerzas_caso(nombre_caso, caso):
    """Diagnostica las fuerzas de un caso específico"""
    print(f"\n{'='*60}")
    print(f"⚡ DIAGNÓSTICO DE FUERZAS: {nombre_caso}")
    print(f"{'='*60}")
    
    try:
        # Crear objetos
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
        
        # Crear dovelas
        dovelas = crear_dovelas(
            circulo=circulo,
            perfil_terreno=caso['perfil_terreno'],
            estrato=estrato,
            num_dovelas=10
        )
        
        print(f"✅ Dovelas creadas: {len(dovelas)}")
        
        # Analizar cada dovela
        suma_fuerzas_actuantes = 0
        suma_fuerzas_resistentes = 0
        
        print(f"\n📊 ANÁLISIS DETALLADO POR DOVELA:")
        print(f"{'ID':<3} {'X':<6} {'Altura':<7} {'Peso':<8} {'Alpha':<6} {'F_act':<8} {'F_res':<8}")
        print("-" * 50)
        
        for i, dovela in enumerate(dovelas):
            # Calcular fuerzas manualmente
            from core.fellenius import calcular_fuerza_actuante_dovela, calcular_fuerza_resistente_dovela
            
            f_actuante = calcular_fuerza_actuante_dovela(dovela)
            f_resistente = calcular_fuerza_resistente_dovela(dovela)
            
            suma_fuerzas_actuantes += f_actuante
            suma_fuerzas_resistentes += f_resistente
            
            print(f"{i:<3} {dovela.x_centro:<6.1f} {dovela.altura:<7.2f} {dovela.peso:<8.1f} "
                  f"{dovela.angulo_alpha:<6.1f} {f_actuante:<8.2f} {f_resistente:<8.2f}")
        
        print("-" * 50)
        print(f"TOTALES: F_actuante={suma_fuerzas_actuantes:.2f}, F_resistente={suma_fuerzas_resistentes:.2f}")
        
        if suma_fuerzas_actuantes <= 0:
            print(f"❌ PROBLEMA: Suma de fuerzas actuantes ≤ 0")
            print(f"   Esto indica que las dovelas no tienen componente tangencial suficiente")
            print(f"   Posibles causas:")
            print(f"   - Círculo demasiado plano (ángulos alpha muy pequeños)")
            print(f"   - Dovelas con altura muy pequeña")
            print(f"   - Círculo mal posicionado")
        else:
            fs_manual = suma_fuerzas_resistentes / suma_fuerzas_actuantes
            print(f"✅ Factor de seguridad manual: {fs_manual:.3f}")
        
        # Intentar análisis Fellenius completo
        print(f"\n🧮 ANÁLISIS FELLENIUS COMPLETO:")
        try:
            resultado_fellenius = analizar_fellenius(
                circulo=circulo,
                perfil_terreno=caso['perfil_terreno'],
                estrato=estrato,
                num_dovelas=10
            )
            print(f"✅ Fellenius exitoso: FS = {resultado_fellenius['factor_seguridad']:.3f}")
        except Exception as e:
            print(f"❌ Fellenius falló: {str(e)}")
        
        # Intentar análisis Bishop completo
        print(f"\n🧮 ANÁLISIS BISHOP COMPLETO:")
        try:
            resultado_bishop = analizar_bishop(
                circulo=circulo,
                perfil_terreno=caso['perfil_terreno'],
                estrato=estrato,
                num_dovelas=10
            )
            print(f"✅ Bishop exitoso: FS = {resultado_bishop['factor_seguridad']:.3f}")
        except Exception as e:
            print(f"❌ Bishop falló: {str(e)}")
            
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

def main():
    """Función principal"""
    print("⚡ DIAGNÓSTICO DE FUERZAS - CASOS DE EJEMPLO")
    print("="*60)
    
    # Diagnosticar solo el primer caso para empezar
    primer_caso = list(CASOS_EJEMPLO.items())[0]
    nombre_caso, caso = primer_caso
    
    diagnosticar_fuerzas_caso(nombre_caso, caso)
    
    print(f"\n{'='*60}")
    print("🏁 DIAGNÓSTICO DE FUERZAS COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    main()
