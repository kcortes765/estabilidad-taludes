"""
Modelos de datos para análisis de estabilidad de taludes.

Este módulo contiene las clases principales para representar:
- Dovelas individuales del círculo de falla
- Círculos de falla con sus propiedades
- Estratos de suelo con parámetros geotécnicos
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import math


@dataclass
class Estrato:
    """
    Representa un estrato de suelo con sus parámetros geotécnicos.
    
    Attributes:
        cohesion: Cohesión efectiva c' en kPa
        phi_grados: Ángulo de fricción interna φ' en grados
        gamma: Peso específico γ en kN/m³
        gamma_sat: Peso específico saturado γsat en kN/m³ (opcional)
        nombre: Nombre descriptivo del estrato (opcional)
    """
    cohesion: float  # c' en kPa
    phi_grados: float  # φ' en grados
    gamma: float  # γ en kN/m³
    gamma_sat: Optional[float] = None  # γsat en kN/m³
    nombre: str = "Estrato"
    
    def __post_init__(self):
        """Validaciones básicas de parámetros geotécnicos."""
        if self.cohesion < 0:
            raise ValueError(f"Cohesión debe ser ≥ 0, recibido: {self.cohesion}")
        if not (0 <= self.phi_grados <= 45):
            raise ValueError(f"Ángulo de fricción debe estar entre 0-45°, recibido: {self.phi_grados}")
        if self.gamma <= 0:
            raise ValueError(f"Peso específico debe ser > 0, recibido: {self.gamma}")
        if self.gamma_sat is not None and self.gamma_sat <= self.gamma:
            raise ValueError(f"Peso específico saturado debe ser > γ, recibido: γsat={self.gamma_sat}, γ={self.gamma}")
    
    @property
    def phi_radianes(self) -> float:
        """Ángulo de fricción en radianes."""
        return math.radians(self.phi_grados)
    
    @property
    def tan_phi(self) -> float:
        """Tangente del ángulo de fricción."""
        return math.tan(self.phi_radianes)


@dataclass
class Dovela:
    """
    Representa una dovela individual en el análisis de estabilidad.
    
    Una dovela es una rebanada vertical del talud delimitada por el círculo de falla.
    Contiene toda la información necesaria para los cálculos de Fellenius y Bishop.
    
    Attributes:
        x_centro: Coordenada X del centro de la dovela en m
        ancho: Ancho de la dovela (Δx) en m
        altura: Altura de la dovela en m
        angulo_alpha: Ángulo α de la tangente al círculo en radianes
        cohesion: Cohesión efectiva c' en kPa
        phi_grados: Ángulo de fricción interna φ' en grados
        gamma: Peso específico γ en kN/m³
        peso: Peso total de la dovela W en kN
        presion_poros: Presión de poros u en kPa
        longitud_arco: Longitud del arco ΔL en m
        fuerza_normal_efectiva: Fuerza normal efectiva en kN (calculada)
        tiene_traccion: Indica si la dovela está en tracción
    """
    x_centro: float
    ancho: float  # Δx
    altura: float
    angulo_alpha: float  # α en radianes
    cohesion: float  # c' en kPa
    phi_grados: float  # φ' en grados
    gamma: float  # γ en kN/m³
    peso: float  # W en kN
    presion_poros: float  # u en kPa
    longitud_arco: float  # ΔL en m
    fuerza_normal_efectiva: float = 0.0  # N' en kN
    tiene_traccion: bool = False
    
    def __post_init__(self):
        """Validaciones básicas de geometría y parámetros."""
        if self.ancho <= 0:
            raise ValueError(f"Ancho de dovela debe ser > 0, recibido: {self.ancho}")
        if self.altura <= 0:
            raise ValueError(f"Altura de dovela debe ser > 0, recibido: {self.altura}")
        if abs(self.angulo_alpha) > math.radians(80):
            raise ValueError(f"Ángulo α muy pronunciado: {math.degrees(self.angulo_alpha)}°")
        if self.cohesion < 0:
            raise ValueError(f"Cohesión debe ser ≥ 0, recibido: {self.cohesion}")
        if not (0 <= self.phi_grados <= 45):
            raise ValueError(f"Ángulo de fricción debe estar entre 0-45°, recibido: {self.phi_grados}")
        if self.gamma <= 0:
            raise ValueError(f"Peso específico debe ser > 0, recibido: {self.gamma}")
        if self.longitud_arco <= 0:
            raise ValueError(f"Longitud de arco debe ser > 0, recibido: {self.longitud_arco}")
    
    @property
    def phi_radianes(self) -> float:
        """Ángulo de fricción en radianes."""
        return math.radians(self.phi_grados)
    
    @property
    def tan_phi(self) -> float:
        """Tangente del ángulo de fricción."""
        return math.tan(self.phi_radianes)
    
    @property
    def sin_alpha(self) -> float:
        """Seno del ángulo α."""
        return math.sin(self.angulo_alpha)
    
    @property
    def cos_alpha(self) -> float:
        """Coseno del ángulo α."""
        return math.cos(self.angulo_alpha)
    
    @property
    def tan_alpha(self) -> float:
        """Tangente del ángulo α."""
        return math.tan(self.angulo_alpha)
    
    def calcular_fuerza_normal_efectiva(self) -> float:
        """
        Calcula la fuerza normal efectiva N' = W*cos(α) - u*ΔL.
        
        Returns:
            Fuerza normal efectiva en kN
        """
        self.fuerza_normal_efectiva = (self.peso * self.cos_alpha - 
                                     self.presion_poros * self.longitud_arco)
        
        # Verificar si hay tracción
        self.tiene_traccion = self.fuerza_normal_efectiva < 0
        
        return self.fuerza_normal_efectiva
    
    def calcular_resistencia_fellenius(self) -> float:
        """
        Calcula la resistencia al corte para el método de Fellenius.
        
        Fórmula: c'*ΔL + N'*tan(φ')
        Si hay tracción (N' < 0), la fricción se anula.
        
        Returns:
            Resistencia al corte en kN
        """
        resistencia_cohesion = self.cohesion * self.longitud_arco
        
        if self.tiene_traccion:
            # En tracción, solo actúa la cohesión
            resistencia_friccion = 0.0
        else:
            resistencia_friccion = self.fuerza_normal_efectiva * self.tan_phi
        
        return resistencia_cohesion + resistencia_friccion
    
    def calcular_fuerza_actuante_fellenius(self) -> float:
        """
        Calcula la fuerza actuante para el método de Fellenius.
        
        Fórmula: W*sin(α)
        
        Returns:
            Fuerza actuante en kN
        """
        return self.peso * self.sin_alpha


@dataclass
class CirculoFalla:
    """
    Representa un círculo de falla para análisis de estabilidad.
    
    Contiene la geometría del círculo, las dovelas que lo componen,
    y los factores de seguridad calculados con diferentes métodos.
    
    Attributes:
        xc: Coordenada X del centro del círculo en m
        yc: Coordenada Y del centro del círculo en m
        radio: Radio del círculo en m
        dovelas: Lista de dovelas que componen el círculo
        fs_fellenius: Factor de seguridad por método Fellenius
        fs_bishop: Factor de seguridad por método Bishop
        convergio_bishop: Indica si Bishop convergió
        iteraciones_bishop: Número de iteraciones usadas en Bishop
        es_valido: Indica si el círculo es geométricamente válido
    """
    xc: float  # Centro X
    yc: float  # Centro Y
    radio: float  # Radio
    dovelas: List[Dovela] = field(default_factory=list)
    fs_fellenius: Optional[float] = None
    fs_bishop: Optional[float] = None
    convergio_bishop: bool = False
    iteraciones_bishop: int = 0
    es_valido: bool = True
    
    def __post_init__(self):
        """Validaciones básicas del círculo."""
        if self.radio <= 0:
            raise ValueError(f"Radio debe ser > 0, recibido: {self.radio}")
    
    @property
    def num_dovelas(self) -> int:
        """Número de dovelas en el círculo."""
        return len(self.dovelas)
    
    @property
    def peso_total(self) -> float:
        """Peso total de todas las dovelas en kN."""
        return sum(dovela.peso for dovela in self.dovelas)
    
    @property
    def longitud_total_arco(self) -> float:
        """Longitud total del arco de falla en m."""
        return sum(dovela.longitud_arco for dovela in self.dovelas)
    
    def agregar_dovela(self, dovela: Dovela) -> None:
        """
        Agrega una dovela al círculo.
        
        Args:
            dovela: Dovela a agregar
        """
        self.dovelas.append(dovela)
    
    def validar_geometria(self) -> bool:
        """
        Valida que la geometría del círculo sea correcta.
        
        Returns:
            True si la geometría es válida
        """
        if self.num_dovelas == 0:
            self.es_valido = False
            return False
        
        # Verificar que todas las dovelas tengan geometría válida
        for i, dovela in enumerate(self.dovelas):
            if dovela.altura <= 0:
                self.es_valido = False
                return False
            if abs(dovela.angulo_alpha) > math.radians(80):
                self.es_valido = False
                return False
        
        self.es_valido = True
        return True
    
    def calcular_fuerzas_normales_efectivas(self) -> None:
        """Calcula las fuerzas normales efectivas de todas las dovelas."""
        for dovela in self.dovelas:
            dovela.calcular_fuerza_normal_efectiva()
    
    def tiene_dovelas_en_traccion(self) -> bool:
        """
        Verifica si alguna dovela está en tracción.
        
        Returns:
            True si hay dovelas en tracción
        """
        return any(dovela.tiene_traccion for dovela in self.dovelas)
    
    def obtener_dovelas_en_traccion(self) -> List[int]:
        """
        Obtiene los índices de las dovelas en tracción.
        
        Returns:
            Lista de índices de dovelas en tracción
        """
        return [i for i, dovela in enumerate(self.dovelas) if dovela.tiene_traccion]
    
    def resumen(self) -> str:
        """
        Genera un resumen del círculo de falla.
        
        Returns:
            String con información del círculo
        """
        info = [
            f"Círculo de Falla:",
            f"  Centro: ({self.xc:.2f}, {self.yc:.2f}) m",
            f"  Radio: {self.radio:.2f} m",
            f"  Dovelas: {self.num_dovelas}",
            f"  Peso total: {self.peso_total:.1f} kN",
            f"  Longitud arco: {self.longitud_total_arco:.2f} m"
        ]
        
        if self.fs_fellenius is not None:
            info.append(f"  Fs (Fellenius): {self.fs_fellenius:.3f}")
        
        if self.fs_bishop is not None:
            info.append(f"  Fs (Bishop): {self.fs_bishop:.3f}")
            info.append(f"  Convergió: {'Sí' if self.convergio_bishop else 'No'}")
            info.append(f"  Iteraciones: {self.iteraciones_bishop}")
        
        if self.tiene_dovelas_en_traccion():
            traccion_indices = self.obtener_dovelas_en_traccion()
            info.append(f"  Dovelas en tracción: {traccion_indices}")
        
        return "\n".join(info)


# Funciones auxiliares para crear instancias comunes

def crear_estrato_homogeneo(cohesion: float, phi_grados: float, gamma: float, 
                          nombre: str = "Homogéneo") -> Estrato:
    """
    Crea un estrato homogéneo con parámetros básicos.
    
    Args:
        cohesion: Cohesión efectiva en kPa
        phi_grados: Ángulo de fricción en grados
        gamma: Peso específico en kN/m³
        nombre: Nombre del estrato
        
    Returns:
        Instancia de Estrato
    """
    return Estrato(
        cohesion=cohesion,
        phi_grados=phi_grados,
        gamma=gamma,
        nombre=nombre
    )


def crear_circulo_simple(xc: float, yc: float, radio: float) -> CirculoFalla:
    """
    Crea un círculo de falla vacío con geometría básica.
    
    Args:
        xc: Coordenada X del centro
        yc: Coordenada Y del centro
        radio: Radio del círculo
        
    Returns:
        Instancia de CirculoFalla
    """
    return CirculoFalla(xc=xc, yc=yc, radio=radio)


def generar_perfil_simple(
    altura: float,
    angulo_grados: float,
    longitud_base: float | None = None,
    num_puntos: int = 50,
) -> List[Tuple[float, float]]:
    """Generar un perfil de talud sencillo.

    Esta función es un contenedor liviano sobre ``crear_perfil_terreno`` de
    ``core.geometry``. Si ``longitud_base`` no se especifica, la longitud se
    calcula automáticamente en función de la altura y el ángulo del talud.

    Args:
        altura: Altura del talud en metros.
        angulo_grados: Ángulo del talud en grados.
        longitud_base: Longitud horizontal de la base. Si ``None`` se estima de
            forma automática.
        num_puntos: Número de puntos que compondrán el perfil.

    Returns:
        Lista de tuplas ``(x, y)`` que representan el perfil del terreno.
    """
    from core.geometry import crear_perfil_terreno

    return crear_perfil_terreno(
        altura=altura,
        angulo_grados=angulo_grados,
        longitud_base=longitud_base,
        num_puntos=num_puntos,
    )


# Constantes útiles
GRAVEDAD = 9.81  # m/s²
DENSIDAD_AGUA = 9.81  # kN/m³ (γw)
TOLERANCIA_CONVERGENCIA = 0.001  # Para método Bishop
MAX_ITERACIONES_BISHOP = 100
