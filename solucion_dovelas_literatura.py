"""
SOLUCIÓN PARA DOVELAS EN CASOS DE LITERATURA TÉCNICA
Corrige el problema de "altura inválida" en dovelas para casos reales
"""

from data.models import CirculoFalla, Estrato, Dovela
from core.geometry import crear_dovelas, interpolar_terreno, calcular_y_circulo
from core.bishop import analizar_bishop
from core.fellenius import analizar_fellenius
import math

def crear_dovelas_literatura(circulo, perfil_terreno, estrato, num_dovelas=20):
    """
    Versión mejorada de crear_dovelas que maneja casos de literatura técnica.
    Evita crear dovelas donde el círculo se extiende más allá del terreno.
    """
    print(f"DEBUG: Iniciando crear_dovelas_literatura")
    print(f"DEBUG: Círculo centro=({circulo.xc}, {circulo.yc}), radio={circulo.radio}")
    print(f"DEBUG: Perfil: {perfil_terreno}")
    
    # Determinar intersecciones reales del círculo con el terreno
    x_min_perfil = min(p[0] for p in perfil_terreno) 
    x_max_perfil = max(p[0] for p in perfil_terreno)
    
    print(f"DEBUG: Rango perfil X: [{x_min_perfil}, {x_max_perfil}]")
    
    # Encontrar intersecciones válidas del círculo con el terreno
    intersecciones_validas = []
    
    # Buscar intersecciones con tolerancia
    for x in range(int(x_min_perfil), int(x_max_perfil) + 1):
        try:
            y_terreno = interpolar_terreno(x, perfil_terreno)
            y_circulo = calcular_y_circulo(x, circulo.xc, circulo.yc, circulo.radio, parte_superior=False)
            
            if y_circulo is not None:
                # Si el círculo está cerca del terreno, es una intersección válida
                if abs(y_circulo - y_terreno) < 1.0:  # 1m de tolerancia
                    intersecciones_validas.append(x)
                    print(f"DEBUG: Intersección válida en X={x}: terreno={y_terreno:.2f}, círculo={y_circulo:.2f}")
        except Exception as e:
            print(f"DEBUG: Error en X={x}: {e}")
            continue
    
    print(f"DEBUG: Intersecciones válidas encontradas: {intersecciones_validas}")
    
    if len(intersecciones_validas) < 2:
        # Si no hay suficientes intersecciones, usar el rango completo pero limitado
        x_inicio = max(circulo.xc - circulo.radio * 0.8, x_min_perfil)
        x_fin = min(circulo.xc + circulo.radio * 0.8, x_max_perfil)
        print(f"DEBUG: Usando rango limitado: [{x_inicio:.1f}, {x_fin:.1f}]")
    else:
        # Usar las intersecciones encontradas con un poco de margen
        x_inicio = max(min(intersecciones_validas) - 2, x_min_perfil)
        x_fin = min(max(intersecciones_validas) + 2, x_max_perfil)
        print(f"DEBUG: Usando rango de intersecciones: [{x_inicio:.1f}, {x_fin:.1f}]")
    
    # Crear dovelas solo en el rango válido
    ancho_total = x_fin - x_inicio
    ancho_dovela = ancho_total / num_dovelas
    
    print(f"DEBUG: Ancho total={ancho_total:.2f}, ancho dovela={ancho_dovela:.2f}")
    
    dovelas = []
    dovelas_rechazadas = 0
    
    for i in range(num_dovelas):
        x_centro = x_inicio + (i + 0.5) * ancho_dovela
        
        # Verificar que este punto está realmente en el perfil
        if x_centro < x_min_perfil or x_centro > x_max_perfil:
            dovelas_rechazadas += 1
            print(f"DEBUG: Dovela {i} rechazada - fuera de perfil: X={x_centro:.2f}")
            continue
            
        try:
            y_terreno = interpolar_terreno(x_centro, perfil_terreno)
            y_circulo = calcular_y_circulo(x_centro, circulo.xc, circulo.yc, circulo.radio, parte_superior=False)
            
            if y_circulo is None:
                dovelas_rechazadas += 1
                print(f"DEBUG: Dovela {i} rechazada - sin intersección círculo")
                continue
                
            altura = y_terreno - y_circulo
            
            # Solo crear dovela si tiene altura positiva y razonable
            if altura > 0.1 and altura < 50:  # Entre 10cm y 50m
                # Calcular ángulo alpha (tangente al círculo)
                dx = x_centro - circulo.xc
                dy = y_circulo - circulo.yc
                angulo_alpha = math.degrees(math.atan2(dx, dy))
                
                # Solo crear dovela si el ángulo es razonable para Bishop
                if -60 <= angulo_alpha <= 60:
                    dovela = Dovela(
                        x_centro=x_centro,
                        y_centro=(y_terreno + y_circulo) / 2,
                        ancho=ancho_dovela,
                        altura=altura,
                        angulo_alpha=angulo_alpha,
                        estrato=estrato
                    )
                    dovelas.append(dovela)
                    print(f"DEBUG: Dovela {i} creada - X={x_centro:.2f}, altura={altura:.2f}, α={angulo_alpha:.1f}°")
                else:
                    dovelas_rechazadas += 1
                    print(f"DEBUG: Dovela {i} rechazada - ángulo extremo: α={angulo_alpha:.1f}°")
            else:
                dovelas_rechazadas += 1
                print(f"DEBUG: Dovela {i} rechazada - altura inválida: {altura:.2f}m")
                    
        except Exception as e:
            # Si hay error en esta dovela, continuar con la siguiente
            dovelas_rechazadas += 1
            print(f"DEBUG: Dovela {i} rechazada - error: {e}")
            continue
    
    print(f"DEBUG: Dovelas creadas: {len(dovelas)}, rechazadas: {dovelas_rechazadas}")
    return dovelas

def probar_casos_literatura_mejorados():
    """
    Prueba los casos de literatura con la creación de dovelas mejorada.
    """
    print(" PROBANDO CASOS DE LITERATURA CON DOVELAS MEJORADAS")
    print("=" * 80)
    
    casos = [
        {
            "nombre": "Bishop 1955",
            "perfil": [(0, 18.3), (36.6, 0), (60, 0)],
            "circulo": CirculoFalla(xc=25.9, yc=27.4, radio=28.1),
            "estrato": Estrato(cohesion=20, phi_grados=15, gamma=18)
        },
        {
            "nombre": "Spencer 1967", 
            "perfil": [(0, 15), (30, 0), (50, 0)],
            "circulo": CirculoFalla(xc=18, yc=22, radio=25),
            "estrato": Estrato(cohesion=10, phi_grados=25, gamma=18)
        }
    ]
    
    for caso in casos:
        print(f"\n CASO: {caso['nombre']}")
        print(f"   Perfil: {caso['perfil']}")
        print(f"   Círculo: Centro=({caso['circulo'].xc}, {caso['circulo'].yc}), Radio={caso['circulo'].radio}")
        
        # Método original
        try:
            dovelas_original = crear_dovelas(caso['circulo'], caso['perfil'], caso['estrato'], num_dovelas=20)
            print(f"   Dovelas método original: {len(dovelas_original)} creadas")
        except Exception as e:
            print(f"   Dovelas método original: ERROR - {str(e)}")
            
        # Método mejorado
        try:
            dovelas_mejorado = crear_dovelas_literatura(caso['circulo'], caso['perfil'], caso['estrato'], num_dovelas=20)
            print(f"   Dovelas método mejorado: {len(dovelas_mejorado)} creadas")
            
            if len(dovelas_mejorado) > 0:
                # Mostrar algunas propiedades de las dovelas
                alturas = [d.altura for d in dovelas_mejorado]
                angulos = [d.angulo_alpha for d in dovelas_mejorado]
                print(f"      - Alturas: min={min(alturas):.2f}m, max={max(alturas):.2f}m")
                print(f"      - Ángulos α: min={min(angulos):.1f}°, max={max(angulos):.1f}°")
                
                # Intentar análisis Bishop
                try:
                    from core.bishop import calcular_factor_seguridad_bishop
                    resultado = calcular_factor_seguridad_bishop(dovelas_mejorado)
                    if resultado.convergio:
                        print(f"      - Factor de seguridad Bishop: {resultado.factor_seguridad:.3f}")
                    else:
                        print(f"      - Bishop no convergió")
                except Exception as e:
                    print(f"      - Error en Bishop: {str(e)}")
                    
        except Exception as e:
            print(f"   Dovelas método mejorado: ERROR - {str(e)}")

if __name__ == "__main__":
    probar_casos_literatura_mejorados()
