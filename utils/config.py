import yaml
from pathlib import Path

def load_config(config_path: str = "config.yaml") -> dict:
    """
    Load the configuration settings from a YAML file.

    Args:
        config_path (str): Path to the YAML configuration file. Defaults to 'config.yaml'.

    Returns:
        dict: Configuration settings as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    return config
