"""
Validación geométrica avanzada para parámetros de análisis de estabilidad de taludes.
Determina rangos válidos y valida configuraciones antes del análisis.
"""

import numpy as np
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass

@dataclass
class RangosValidos:
    """Rangos válidos para parámetros geométricos"""
    centro_x_min: float
    centro_x_max: float
    centro_y_min: float
    centro_y_max: float
    radio_min: float
    radio_max: float
    razon: str

@dataclass
class ResultadoValidacionGeometrica:
    """Resultado de validación geométrica"""
    es_valido: bool
    mensaje: str
    dovelas_validas_estimadas: int
    rangos_sugeridos: Optional[RangosValidos] = None

class ValidadorGeometrico:
    """Validador geométrico para parámetros de análisis de taludes"""
    
    def __init__(self, perfil_terreno: List[Tuple[float, float]], 
                 num_dovelas_minimas: int = 10):
        """
        Inicializa el validador geométrico
        
        Args:
            perfil_terreno: Lista de puntos (x, y) del perfil del terreno
            num_dovelas_minimas: Número mínimo de dovelas válidas requeridas
        """
        self.perfil_terreno = sorted(perfil_terreno, key=lambda p: p[0])
        self.num_dovelas_minimas = num_dovelas_minimas
        
        # Calcular límites del terreno
        self.x_min = min(p[0] for p in perfil_terreno)
        self.x_max = max(p[0] for p in perfil_terreno)
        self.y_min = min(p[1] for p in perfil_terreno)
        self.y_max = max(p[1] for p in perfil_terreno)
        
    def interpolar_y_terreno(self, x: float) -> float:
        """Interpola la altura del terreno en una coordenada x"""
        if x <= self.perfil_terreno[0][0]:
            return self.perfil_terreno[0][1]
        if x >= self.perfil_terreno[-1][0]:
            return self.perfil_terreno[-1][1]
            
        for i in range(len(self.perfil_terreno) - 1):
            x1, y1 = self.perfil_terreno[i]
            x2, y2 = self.perfil_terreno[i + 1]
            
            if x1 <= x <= x2:
                if x2 == x1:
                    return y1
                return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
        
        return self.perfil_terreno[-1][1]
    
    def calcular_intersecciones_circulo_terreno(self, centro_x: float, centro_y: float, 
                                              radio: float) -> List[Tuple[float, float]]:
        """
        Calcula las intersecciones entre el círculo y el terreno
        
        Returns:
            Lista de puntos de intersección (x, y)
        """
        intersecciones = []
        
        # Buscar intersecciones evaluando el círculo en puntos del terreno
        x_start = max(self.x_min, centro_x - radio)
        x_end = min(self.x_max, centro_x + radio)
        
        # Evaluar en puntos discretos
        num_puntos = 200
        x_vals = np.linspace(x_start, x_end, num_puntos)
        
        for x in x_vals:
            y_terreno = self.interpolar_y_terreno(x)
            
            # Calcular y del círculo en esta x
            discriminante = radio**2 - (x - centro_x)**2
            if discriminante >= 0:
                y_circulo_superior = centro_y + np.sqrt(discriminante)
                y_circulo_inferior = centro_y - np.sqrt(discriminante)
                
                # Verificar si el terreno intersecta el círculo
                if y_circulo_inferior <= y_terreno <= y_circulo_superior:
                    intersecciones.append((x, y_terreno))
        
        # Eliminar duplicados cercanos
        intersecciones_filtradas = []
        for punto in intersecciones:
            es_duplicado = False
            for punto_existente in intersecciones_filtradas:
                if abs(punto[0] - punto_existente[0]) < 0.1:
                    es_duplicado = True
                    break
            if not es_duplicado:
                intersecciones_filtradas.append(punto)
        
        return intersecciones_filtradas
    
    def estimar_dovelas_validas(self, centro_x: float, centro_y: float, 
                               radio: float, num_dovelas: int = 20) -> int:
        """
        Estima cuántas dovelas válidas se generarían con estos parámetros
        """
        intersecciones = self.calcular_intersecciones_circulo_terreno(centro_x, centro_y, radio)
        
        if len(intersecciones) < 2:
            return 0
        
        # Ordenar intersecciones por x
        intersecciones = sorted(intersecciones, key=lambda p: p[0])
        x_inicio = intersecciones[0][0]
        x_fin = intersecciones[-1][0]
        
        if x_fin - x_inicio < 1.0:  # Superficie muy pequeña
            return 0
        
        # Estimar dovelas válidas
        ancho_dovela = (x_fin - x_inicio) / num_dovelas
        dovelas_validas = 0
        
        for i in range(num_dovelas):
            x_centro_dovela = x_inicio + (i + 0.5) * ancho_dovela
            
            # Verificar que la dovela esté dentro del terreno y círculo
            y_terreno = self.interpolar_y_terreno(x_centro_dovela)
            
            # Calcular y del círculo
            discriminante = radio**2 - (x_centro_dovela - centro_x)**2
            if discriminante >= 0:
                y_circulo_inferior = centro_y - np.sqrt(discriminante)
                
                # La dovela es válida si hay altura suficiente
                if y_terreno > y_circulo_inferior and (y_terreno - y_circulo_inferior) > 0.5:
                    dovelas_validas += 1
        
        return dovelas_validas
    
    def calcular_rangos_validos(self) -> RangosValidos:
        """
        Calcula rangos válidos para los parámetros del círculo
        """
        # Rangos conservadores basados en la geometría del terreno
        margen = (self.x_max - self.x_min) * 0.2
        
        centro_x_min = self.x_min - margen
        centro_x_max = self.x_max + margen
        
        # Centro Y debe estar por encima del terreno para generar superficie de falla
        centro_y_min = self.y_max + 2.0
        centro_y_max = self.y_max + (self.x_max - self.x_min)
        
        # Radio debe ser suficiente para intersectar el terreno
        radio_min = 5.0
        radio_max = (self.x_max - self.x_min) * 1.5
        
        return RangosValidos(
            centro_x_min=centro_x_min,
            centro_x_max=centro_x_max,
            centro_y_min=centro_y_min,
            centro_y_max=centro_y_max,
            radio_min=radio_min,
            radio_max=radio_max,
            razon="Basado en geometría del terreno y requisitos mínimos de dovelas"
        )
    
    def validar_parametros(self, centro_x: float, centro_y: float, 
                          radio: float, num_dovelas: int = 20) -> ResultadoValidacionGeometrica:
        """
        Valida si los parámetros geométricos son válidos
        
        Returns:
            ResultadoValidacionGeometrica con el resultado de la validación
        """
        # Verificar rangos básicos
        rangos = self.calcular_rangos_validos()
        
        if not (rangos.centro_x_min <= centro_x <= rangos.centro_x_max):
            return ResultadoValidacionGeometrica(
                es_valido=False,
                mensaje=f"Centro X fuera de rango válido [{rangos.centro_x_min:.1f}, {rangos.centro_x_max:.1f}]",
                dovelas_validas_estimadas=0,
                rangos_sugeridos=rangos
            )
        
        if not (rangos.centro_y_min <= centro_y <= rangos.centro_y_max):
            return ResultadoValidacionGeometrica(
                es_valido=False,
                mensaje=f"Centro Y fuera de rango válido [{rangos.centro_y_min:.1f}, {rangos.centro_y_max:.1f}]",
                dovelas_validas_estimadas=0,
                rangos_sugeridos=rangos
            )
        
        if not (rangos.radio_min <= radio <= rangos.radio_max):
            return ResultadoValidacionGeometrica(
                es_valido=False,
                mensaje=f"Radio fuera de rango válido [{rangos.radio_min:.1f}, {rangos.radio_max:.1f}]",
                dovelas_validas_estimadas=0,
                rangos_sugeridos=rangos
            )
        
        # Verificar intersecciones con terreno
        intersecciones = self.calcular_intersecciones_circulo_terreno(centro_x, centro_y, radio)
        
        if len(intersecciones) < 2:
            return ResultadoValidacionGeometrica(
                es_valido=False,
                mensaje="El círculo no intersecta suficientemente con el terreno",
                dovelas_validas_estimadas=0,
                rangos_sugeridos=rangos
            )
        
        # Estimar dovelas válidas
        dovelas_validas = self.estimar_dovelas_validas(centro_x, centro_y, radio, num_dovelas)
        
        if dovelas_validas < self.num_dovelas_minimas:
            return ResultadoValidacionGeometrica(
                es_valido=False,
                mensaje=f"Insuficientes dovelas válidas: {dovelas_validas} < {self.num_dovelas_minimas}",
                dovelas_validas_estimadas=dovelas_validas,
                rangos_sugeridos=rangos
            )
        
        return ResultadoValidacionGeometrica(
            es_valido=True,
            mensaje=f"Parámetros válidos. Dovelas estimadas: {dovelas_validas}",
            dovelas_validas_estimadas=dovelas_validas
        )
    
    def generar_parametros_validos_ejemplo(self) -> Dict[str, float]:
        """
        Genera parámetros de ejemplo que garantizan un análisis válido
        """
        # Centro en el medio del terreno, elevado
        centro_x = (self.x_min + self.x_max) / 2
        centro_y = self.y_max + (self.x_max - self.x_min) * 0.3
        
        # Radio que cubra aproximadamente 60% del ancho del terreno
        radio = (self.x_max - self.x_min) * 0.6
        
        # Verificar y ajustar si es necesario
        resultado = self.validar_parametros(centro_x, centro_y, radio)
        
        if not resultado.es_valido:
            # Usar rangos seguros
            rangos = self.calcular_rangos_validos()
            centro_x = (rangos.centro_x_min + rangos.centro_x_max) / 2
            centro_y = (rangos.centro_y_min + rangos.centro_y_max) / 2
            radio = (rangos.radio_min + rangos.radio_max) / 2
        
        return {
            'centro_x': centro_x,
            'centro_y': centro_y,
            'radio': radio
        }

def validar_caso_ejemplo(caso: Dict) -> ResultadoValidacionGeometrica:
    """
    Valida un caso de ejemplo completo
    
    Args:
        caso: Diccionario con los parámetros del caso
        
    Returns:
        ResultadoValidacionGeometrica
    """
    perfil = caso['perfil_terreno']
    validador = ValidadorGeometrico(perfil)
    
    return validador.validar_parametros(
        caso['centro_x'],
        caso['centro_y'], 
        caso['radio']
    )

if __name__ == "__main__":
    # Ejemplo de uso
    perfil_ejemplo = [(0, 10), (10, 15), (20, 12), (30, 8), (40, 5)]
    validador = ValidadorGeometrico(perfil_ejemplo)
    
    # Generar parámetros válidos
    params_validos = validador.generar_parametros_validos_ejemplo()
    print("Parámetros válidos generados:")
    print(f"Centro X: {params_validos['centro_x']:.2f}")
    print(f"Centro Y: {params_validos['centro_y']:.2f}")
    print(f"Radio: {params_validos['radio']:.2f}")
    
    # Validar
    resultado = validador.validar_parametros(
        params_validos['centro_x'],
        params_validos['centro_y'],
        params_validos['radio']
    )
    
    print(f"\nValidación: {resultado.mensaje}")
    print(f"Dovelas válidas estimadas: {resultado.dovelas_validas_estimadas}")
