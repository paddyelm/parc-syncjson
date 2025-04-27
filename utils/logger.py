from loguru import logger
from pathlib import Path

def init_logger(config):
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
    log_folder = Path(config.get('log_folder', './logs'))
    log_folder.mkdir(parents=True, exist_ok=True)

    log_file = log_folder / 'app.log'

    logger.remove()
    logger.add(
        log_file,
        rotation="10 MB",
        retention="10 days",
        level=config.get('log_level', 'INFO'),
        format="[{time:YYYY-MM-DD HH:mm:ss}] {level} - {message}",
    )

    # Also output to console
    logger.add(
        lambda msg: print(msg, end=''),
        level=config.get('log_level', 'INFO'),
        format="[{time:HH:mm:ss}] {level} - {message}"
    )

    return logger