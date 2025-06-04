"""
Optimiza círculos de los casos de ejemplo para obtener factores de seguridad realistas
"""

import re
from typing import Tuple, List

from gui_examples import CASOS_EJEMPLO, calcular_perfil_terreno
from core.geometry import CirculoFalla, Estrato, crear_dovelas
from core.bishop import analizar_bishop


def rango_objetivo(descripcion: str) -> Tuple[float, float]:
    """Devuelve rango objetivo de FS basado en texto descriptivo"""
    desc = descripcion.lower()
    if '1.2' in desc and '1.4' in desc:
        return 1.2, 1.4
    if '1.0' in desc and '1.2' in desc:
        return 1.0, 1.2
    if '2.0' in desc:
        return 2.0, 4.0  # muy estable
    if '1.5' in desc:
        return 1.5, 2.5
    # por defecto
    return 1.5, 3.0


def optimizar_circulo(caso: dict) -> Tuple[float, float, float, float]:
    """Busca círculo con FS en rango objetivo, devuelve mejor (cx, cy, r, fs) o None"""
    # Rango objetivo
    fs_min, fs_max = rango_objetivo(caso['esperado'])

    # fijar centro_x como 17-18 basado en geometría
    centro_x = 18.0

    best = None
    best_diff = float('inf')
    # Rango de búsqueda
    altura = caso['altura']

    for cy in [round(y, 1) for y in frange(4.0, altura*1.3, 0.5)]:
        for radio in [round(r, 1) for r in frange(12.0, altura*3.0, 1.0)]:
            try:
                circulo = CirculoFalla(centro_x, cy, radio)
                estrato = Estrato(caso['cohesion'], caso['phi_grados'], caso['gamma'])
                dovelas = crear_dovelas(circulo, caso['perfil_terreno'], estrato, 10)
                res = analizar_bishop(circulo, caso['perfil_terreno'], estrato, 10)
                fs = res['factor_seguridad']
                if fs_min <= fs <= fs_max:
                    return centro_x, cy, radio, fs
                diff = abs((fs_min+fs_max)/2 - fs)
                if diff < best_diff and 0.5 < fs < 10:
                    best_diff = diff
                    best = (centro_x, cy, radio, fs)
            except Exception:
                continue
    return best  # Puede ser None


def frange(start: float, stop: float, step: float):
    x = start
    while x <= stop:
        yield x
        x += step


def main():
    nuevos_casos = {}
    for nombre, caso in CASOS_EJEMPLO.items():
        print(f"\n🔍 Optimizando {nombre}")
        config = optimizar_circulo(caso)
        if config:
            cx, cy, radio, fs = config
            print(f"  ✅ Config encontrada: FS={fs:.3f}, cx={cx}, cy={cy}, r={radio}")
            nuevo = caso.copy()
            nuevo['centro_x'] = cx
            nuevo['centro_y'] = cy
            nuevo['radio'] = radio
            nuevos_casos[nombre] = nuevo
        else:
            print("  ❌ No se encontró configuración adecuada, se mantiene original")
            nuevos_casos[nombre] = caso

    # Generar código para reemplazar gui_examples
    generar_nuevo_gui(nuevos_casos)


def generar_nuevo_gui(casos: dict):
    """Escribe un nuevo archivo gui_examples_opt.py para inspección"""
    import json
    content = """# Casos de ejemplo optimizados automáticamente para FS realistas

import math

def calcular_perfil_terreno(altura, angulo_talud, longitud_total=40):
    angulo_rad = math.radians(angulo_talud)
    proyeccion_horizontal = altura / math.tan(angulo_rad)
    return [
        (0, altura),
        (longitud_total * 0.3, altura),
        (longitud_total * 0.3 + proyeccion_horizontal, 0),
        (longitud_total, 0)
    ]

CASOS_EJEMPLO = """ + json.dumps(casos, indent=4) + """
"""
    with open('gui_examples_opt.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("\n📄 Archivo gui_examples_opt.py generado")

if __name__ == "__main__":
    main()
