"""
CrisisGuardian AI - Logging Configuration
Centralized logging setup for all application modules.
"""

import os
import logging
import logging.handlers
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create logs directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/crisisguardian.log")
ENABLE_DETAILED = os.getenv("ENABLE_DETAILED_LOGGING", "false").lower() == "true"

# Log format
DETAILED_FORMAT = '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s'
SIMPLE_FORMAT = '%(asctime)s [%(levelname)s] %(name)s - %(message)s'

LOG_FORMAT = DETAILED_FORMAT if ENABLE_DETAILED else SIMPLE_FORMAT
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def configure_logging():
    """
    Configures logging for the entire application with both file and console handlers.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    
    # Console handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (rotating)
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        root_logger.warning(f"Failed to setup file logging: {e}")
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance for a specific module.
    
    Args:
        name: Module name (typically __name__)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


# Configure logging on module import
configure_logging()
