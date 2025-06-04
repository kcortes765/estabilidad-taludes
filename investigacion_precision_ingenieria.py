"""
INVESTIGACIÓN DE PRECISIÓN DE INGENIERÍA
Análisis profundo para determinar por qué el sistema requiere parámetros no realistas
"""

from data.models import CirculoFalla, Estrato
from core.bishop import analizar_bishop
import math

def analizar_problema_fundamental():
    """
    Investiga por qué se requieren parámetros tan bajos para obtener FS realistas.
    """
    print("=" * 80)
    print("🔬 INVESTIGACIÓN: ¿POR QUÉ SE REQUIEREN PARÁMETROS NO REALISTAS?")
    print("=" * 80)
    
    # GEOMETRÍA ACTUAL
    perfil_terreno = [(0, 10), (10, 10), (20, 0), (40, 0)]
    circulo = CirculoFalla(xc=15, yc=5, radio=30)
    
    print("📐 GEOMETRÍA ANALIZADA:")
    print(f"   Perfil: {perfil_terreno}")
    print(f"   Círculo: Centro=({circulo.xc}, {circulo.yc}), Radio={circulo.radio}")
    
    # CALCULAR ALTURA DEL TALUD
    altura_talud = 10  # de y=10 a y=0
    longitud_talud = 10  # de x=10 a x=20
    angulo_talud = math.degrees(math.atan(altura_talud / longitud_talud))
    
    print(f"\n📊 CARACTERÍSTICAS DEL TALUD:")
    print(f"   Altura: {altura_talud} m")
    print(f"   Longitud horizontal: {longitud_talud} m")
    print(f"   Ángulo del talud: {angulo_talud:.1f}° (pendiente 1:1)")
    
    # ANÁLISIS CON PARÁMETROS REALISTAS
    print(f"\n🧪 ANÁLISIS CON PARÁMETROS REALISTAS DE INGENIERÍA:")
    print("-" * 60)
    
    casos_realistas = [
        {"nombre": "Arcilla blanda", "c": 10, "phi": 15, "descripcion": "Parámetros mínimos reales"},
        {"nombre": "Arcilla media", "c": 20, "phi": 20, "descripcion": "Parámetros típicos"},
        {"nombre": "Arcilla firme", "c": 30, "phi": 25, "descripcion": "Parámetros buenos"},
        {"nombre": "Arena arcillosa", "c": 5, "phi": 30, "descripcion": "Suelo granular"},
        {"nombre": "Arena densa", "c": 0, "phi": 35, "descripcion": "Arena pura"}
    ]
    
    for caso in casos_realistas:
        estrato = Estrato(
            cohesion=caso["c"],
            phi_grados=caso["phi"],
            gamma=18.0,
            nombre=caso["nombre"]
        )
        
        try:
            resultado = analizar_bishop(circulo, perfil_terreno, estrato, num_dovelas=8)
            
            if resultado.es_valido and resultado.convergio:
                fs = resultado.factor_seguridad
                print(f"   {caso['nombre']:<15}: FS = {fs:6.2f} | c={caso['c']:2d} kPa, φ={caso['phi']:2d}° | {caso['descripcion']}")
            else:
                print(f"   {caso['nombre']:<15}: ERROR   | c={caso['c']:2d} kPa, φ={caso['phi']:2d}° | No válido/convergió")
                
        except Exception as e:
            print(f"   {caso['nombre']:<15}: ERROR   | c={caso['c']:2d} kPa, φ={caso['phi']:2d}° | {str(e)[:30]}...")

def investigar_geometria_literatura():
    """
    Compara con geometrías de literatura técnica conocida.
    """
    print(f"\n" + "=" * 80)
    print("📚 COMPARACIÓN CON LITERATURA TÉCNICA")
    print("=" * 80)
    
    # CASO BISHOP (1955) - CLÁSICO
    print("📖 CASO BISHOP (1955) - REFERENCIA TÉCNICA:")
    print("   Talud: 18.3m altura, pendiente 2:1")
    print("   Suelo: c=5.9 kPa, φ=20°, γ=19.6 kN/m³")
    print("   Factor esperado: FS ≈ 1.26")
    
    # Intentar replicar caso Bishop
    perfil_bishop = [
        (0, 18.3),   # Altura original
        (36.6, 0),   # Pendiente 2:1
        (50, 0)      # Extensión
    ]
    
    circulo_bishop = CirculoFalla(xc=25, yc=25, radio=35)
    estrato_bishop = Estrato(cohesion=5.9, phi_grados=20.0, gamma=19.6, nombre="Bishop 1955")
    
    try:
        resultado = analizar_bishop(circulo_bishop, perfil_bishop, estrato_bishop, num_dovelas=10)
        if resultado.es_valido:
            print(f"   RESULTADO: FS = {resultado.factor_seguridad:.3f}")
            print(f"   ERROR vs literatura: {abs(resultado.factor_seguridad - 1.26):.3f}")
        else:
            print("   RESULTADO: ERROR - No válido")
    except Exception as e:
        print(f"   RESULTADO: ERROR - {e}")

def diagnosticar_ecuaciones_bishop():
    """
    Verifica si las ecuaciones del método Bishop están correctamente implementadas.
    """
    print(f"\n" + "=" * 80)
    print("🧮 DIAGNÓSTICO DE ECUACIONES DEL MÉTODO BISHOP")
    print("=" * 80)
    
    print("✅ ECUACIÓN BISHOP IMPLEMENTADA:")
    print("   FS = Σ[c'·ΔL + (W·cos(α) - u·ΔL)·tan(φ')/mα] / Σ[W·sin(α)]")
    print("   donde: mα = cos(α) + sin(α)·tan(φ')/FS")
    
    print("\n🔍 FACTORES QUE PUEDEN CAUSAR FS EXCESIVOS:")
    print("   1. Círculo muy grande → Fuerzas resistentes excesivas")
    print("   2. Talud muy suave → Fuerzas actuantes bajas") 
    print("   3. Error en cálculo de ángulos α")
    print("   4. Error en cálculo de pesos de dovelas")
    print("   5. Error en longitudes de arco")
    
    # Análisis detallado de una dovela
    print(f"\n📊 ANÁLISIS DETALLADO DE DOVELAS:")
    
    perfil = [(0, 10), (10, 10), (20, 0), (40, 0)]
    circulo = CirculoFalla(xc=15, yc=5, radio=30)
    estrato = Estrato(cohesion=20, phi_grados=20, gamma=18.0, nombre="Test")
    
    try:
        resultado = analizar_bishop(circulo, perfil, estrato, num_dovelas=8)
        if resultado.es_valido and hasattr(resultado, 'dovelas'):
            print(f"   Número de dovelas: {len(resultado.dovelas)}")
            
            suma_resistentes = 0
            suma_actuantes = 0
            
            for i, dovela in enumerate(resultado.dovelas):
                if hasattr(dovela, 'peso') and hasattr(dovela, 'angulo_alpha'):
                    peso = dovela.peso
                    alpha = math.radians(dovela.angulo_alpha)
                    
                    fuerza_actuante = peso * math.sin(alpha)
                    fuerza_resistente_base = peso * math.cos(alpha) * math.tan(math.radians(estrato.phi_grados))
                    
                    suma_actuantes += fuerza_actuante
                    suma_resistentes += fuerza_resistente_base
                    
                    if i < 3:  # Mostrar solo primeras 3
                        print(f"   Dovela {i+1}: W={peso:.1f}N, α={dovela.angulo_alpha:.1f}°, F_act={fuerza_actuante:.1f}N")
            
            fs_simple = suma_resistentes / suma_actuantes if suma_actuantes > 0 else float('inf')
            print(f"   FS simplificado (sin cohesión): {fs_simple:.2f}")
            print(f"   FS Bishop completo: {resultado.factor_seguridad:.2f}")
            print(f"   Ratio Bishop/Simple: {resultado.factor_seguridad/fs_simple:.2f}")
            
    except Exception as e:
        print(f"   ERROR en análisis: {e}")

def conclusiones_y_recomendaciones():
    """
    Conclusiones sobre la precisión de ingeniería del sistema.
    """
    print(f"\n" + "=" * 80)
    print("📋 CONCLUSIONES Y RECOMENDACIONES")
    print("=" * 80)
    
    print("🎯 PROBLEMAS IDENTIFICADOS:")
    print("   1. El sistema requiere parámetros no realistas para FS normales")
    print("   2. Geometría actual puede ser demasiado 'fácil' para el círculo")
    print("   3. Posible error en implementación que infla los FS")
    
    print("\n✅ INVESTIGACIONES REQUERIDAS:")
    print("   1. Verificar ecuaciones Bishop vs literatura")
    print("   2. Validar cálculo de pesos y ángulos de dovelas")
    print("   3. Comparar con software comercial (GeoStudio, etc.)")
    print("   4. Usar geometrías estándar de literatura")
    
    print("\n🔧 PRÓXIMOS PASOS PARA PRECISIÓN DE INGENIERÍA:")
    print("   1. Implementar casos de validación de literatura exactos")
    print("   2. Corregir cualquier error en ecuaciones")
    print("   3. Asegurar que funcione con parámetros geotécnicos reales")
    print("   4. Validar contra software comercial")

if __name__ == "__main__":
    analizar_problema_fundamental()
    investigar_geometria_literatura()
    diagnosticar_ecuaciones_bishop()
    conclusiones_y_recomendaciones()
    
    print(f"\n🎯 RESPUESTA A LA PREGUNTA DEL USUARIO:")
    print("NO, la calibración actual NO es precisa desde ingeniería.")
    print("Los parámetros son artificialmente bajos y no representan suelos reales.")
    print("Se requiere investigación profunda para corregir el problema fundamental.")
