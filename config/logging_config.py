import logging
import logging.config
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d"
            "  - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": PROJECT_ROOT / "logs" / "app.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "company_brochur": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "company_brochur.utils": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "company_brochur.llm": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
    "root": {"level": "WARNING", "handlers": ["console"]},
}


def setup_logging():
    """Setup logging configuration for the application."""
    # Create logs directory if it doesn't exist
    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Apply the logging configuration
    logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name."""
    return logging.getLogger(f"company_brochur.{name}")
