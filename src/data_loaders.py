import json
import logging
from pathlib import Path

import pandas as pd
import yaml


logger = logging.getLogger(__name__)


def load_csv(path):
    """Load a CSV file into a DataFrame."""
    dataframe = pd.read_csv(path)
    logger.info("Loaded CSV file: %s (%d rows)", path, len(dataframe))
    return dataframe


def load_json(path):
    """Load a JSON file into a Python object."""
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    logger.info("Loaded JSON file: %s", path)
    return data


def load_yaml(path):
    """Load a YAML file into a Python object."""
    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    logger.info("Loaded YAML file: %s", path)
    return data


def load_data(filepath):
    """Load a file using the loader selected by its extension."""
    path = Path(filepath)
    extension = path.suffix.lower()

    if extension == ".csv":
        return load_csv(path)
    if extension == ".json":
        return load_json(path)
    if extension == ".yaml":
        return load_yaml(path)

    logger.error("Unsupported file format: %s", extension)
    raise ValueError(f"Unsupported file format: {extension}")
