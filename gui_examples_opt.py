# Casos de ejemplo optimizados automáticamente para FS realistas

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

CASOS_EJEMPLO = {
    "Talud Estable - Carretera": {
        "descripcion": "Talud t\u00edpico de carretera con factor de seguridad alto",
        "altura": 8.0,
        "angulo_talud": 35.0,
        "cohesion": 35.0,
        "phi_grados": 30.0,
        "gamma": 19.0,
        "con_agua": false,
        "nivel_freatico": 0.0,
        "centro_x": 17.0,
        "centro_y": 8.0,
        "radio": 20.0,
        "esperado": "Fs > 1.5 (ESTABLE)",
        "perfil_terreno": [
            [
                0,
                8.0
            ],
            [
                12.0,
                8.0
            ],
            [
                23.425184053936917,
                0
            ],
            [
                40,
                0
            ]
        ]
    },
    "Talud Marginal - Arcilla Blanda": {
        "descripcion": "Talud en arcilla blanda con factor de seguridad l\u00edmite",
        "altura": 10.0,
        "angulo_talud": 45.0,
        "cohesion": 12.0,
        "phi_grados": 20.0,
        "gamma": 18.0,
        "con_agua": false,
        "nivel_freatico": 0.0,
        "centro_x": 17.0,
        "centro_y": 10.0,
        "radio": 18.0,
        "esperado": "1.2 < Fs < 1.4 (MARGINAL)",
        "perfil_terreno": [
            [
                0,
                10.0
            ],
            [
                12.0,
                10.0
            ],
            [
                22.0,
                0
            ],
            [
                40,
                0
            ]
        ]
    },
    "Talud con Agua - Cr\u00edtico": {
        "descripcion": "Talud con nivel fre\u00e1tico alto, condici\u00f3n cr\u00edtica",
        "altura": 8.0,
        "angulo_talud": 40.0,
        "cohesion": 20.0,
        "phi_grados": 25.0,
        "gamma": 18.0,
        "con_agua": true,
        "nivel_freatico": 6.0,
        "centro_x": 18.0,
        "centro_y": 7.0,
        "radio": 16.0,
        "esperado": "Fs \u2248 1.0-1.2 (CR\u00cdTICO)",
        "perfil_terreno": [
            [
                0,
                8.0
            ],
            [
                12.0,
                8.0
            ],
            [
                21.53402874075368,
                0
            ],
            [
                40,
                0
            ]
        ]
    },
    "Talud Moderado - Arena Densa": {
        "descripcion": "Talud en arena densa con par\u00e1metros moderados",
        "altura": 6.0,
        "angulo_talud": 30.0,
        "cohesion": 5.0,
        "phi_grados": 35.0,
        "gamma": 20.0,
        "con_agua": false,
        "nivel_freatico": 0.0,
        "centro_x": 16.0,
        "centro_y": 6.0,
        "radio": 16.0,
        "esperado": "Fs > 2.0 (MUY ESTABLE)",
        "perfil_terreno": [
            [
                0,
                6.0
            ],
            [
                12.0,
                6.0
            ],
            [
                22.392304845413264,
                0
            ],
            [
                40,
                0
            ]
        ]
    }
}
