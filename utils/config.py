import json
from typing import Any, Dict
from pathlib import Path

_DEFAULT_CONFIG = {
    "logging": {"level": "INFO", "filename": "app.log"},
    "circle_constraints": {
        "factor_margen_lateral": 0.6,
        "factor_altura_minima": 1.2,
        "factor_altura_maxima": 3.0,
        "factor_radio_min": 0.15,
        "factor_radio_max": 2.5,
        "cobertura_minima": 0.3,
    },
}

_config_cache: Dict[str, Any] | None = None


def load_config(path: str = "config.json") -> Dict[str, Any]:
    global _config_cache
    if _config_cache is None:
        config_path = Path(path)
        if config_path.is_file():
            with open(config_path, "r", encoding="utf-8") as f:
                _config_cache = {**_DEFAULT_CONFIG, **json.load(f)}
        else:
            _config_cache = _DEFAULT_CONFIG
    return _config_cache


def validate_config(cfg: Dict[str, Any]) -> None:
    """Valida estructura básica del archivo de configuración."""
    if "logging" in cfg:
        if not isinstance(cfg["logging"], dict):
            raise ValueError("Sección 'logging' inválida")
    if "circle_constraints" in cfg:
        if not isinstance(cfg["circle_constraints"], dict):
            raise ValueError("Sección 'circle_constraints' inválida")


# Cargar y validar configuración por defecto en la importación
CONFIG = load_config()
validate_config(CONFIG)
