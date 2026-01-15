"""
Centralized logging configuration.
"""

import logging
from logging.handlers import RotatingFileHandler
from configs.config_paths import LOG_FILE  

def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure root logger with console and rotating file handlers.
    """
    root = logging.getLogger()
    if root.handlers:
        return  

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    root.setLevel(level)
    root.addHandler(console)

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  

    # File handler
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)
