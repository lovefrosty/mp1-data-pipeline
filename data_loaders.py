import json
import logging
from pathlib import Path

import pandas as pd


def load_csv(path):
    dataframe = pd.read_csv(path)
    logging.info("Loaded %s with %d rows", path, len(dataframe))
    return dataframe

def load_json(path):
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
    logging.info("Loaded JSON file: %s", path)
    return data

def load_yaml(path):
    import yaml

    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def load_data(filepath):
    path = Path(filepath)
    # read path.suffix.lower()
