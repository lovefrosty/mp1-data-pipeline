"""Functions for saving pipeline output."""

import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def save_data(dataframe, output_path):
    """Create the output directory and save a DataFrame as an index-free CSV."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(path, index=False)
    logger.debug("Saved %d rows to %s", len(dataframe), path)
    return path
