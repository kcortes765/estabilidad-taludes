import logging
from typing import Dict, Any


def setup_logging(config: Dict[str, Any]) -> None:
    level_str = config.get("level", "INFO")
    level = getattr(logging, level_str.upper(), logging.INFO)
    filename = config.get("filename")

    logging.basicConfig(
        level=level,
        filename=filename,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
