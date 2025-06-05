import logging
from logging_utils import get_logger

logger = get_logger(__name__)


def load_text_file(path: str) -> str:
    """Load text file contents, logging an error if the file is missing."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error("Archivo no encontrado: %s", path)
        raise
