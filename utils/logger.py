from loguru import logger as loguru_logger
from pathlib import Path
from typing import Optional

class Logger:
    """
    Initialize and configure the application logger.

    Sets up logging to a file with rotation and retention policies,
    as well as logging to the console. The log level and log folder
    are configurable through the provided configuration dictionary.

    Args:
        config (dict): Dictionary containing configuration settings.

    Returns:
        logger (loguru.Logger): Configured loguru logger instance.
    """

    _instance = None

    def __new__(cls, config: Optional[dict] = None):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: Optional[dict] = None):
        if self._initialized:
            return  # Already initialized, skip

        if config is None:
            raise ValueError("Logger must be initialized with a config dictionary on first use.")

        log_folder = Path(config.get('log_folder', './resources/logs'))
        log_folder.mkdir(parents=True, exist_ok=True)

        log_file = log_folder / 'app.log'

        loguru_logger.remove()
        loguru_logger.add(
            log_file,
            rotation="10 MB",
            retention="10 days",
            level=config.get('log_level', 'INFO'),
            format="[{time:YYYY-MM-DD HH:mm:ss}] {level} - {message}",
        )

        loguru_logger.add(
            lambda msg: print(msg, end=''),
            level=config.get('log_level', 'INFO'),
            format="[{time:HH:mm:ss}] {level} - {message}"
        )

        self.logger = loguru_logger
        self._initialized = True

    def get_logger(self):
        """
        Returns the singleton logger instance.
        """
        return self.logger
