"""Validate required columns and configured numeric fields."""

import logging

import pandas as pd


logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):
    """Validate the DataFrame and return valid data.

    required_columns: a list of column names that must exist.
    numeric_columns: a list of column names whose values should be numeric.
    """
    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]
    if missing_columns:
        missing_list = ", ".join(missing_columns)
        logger.error("Required columns are missing: %s", missing_list)
        raise ValueError(f"Required columns are missing: {missing_list}")

    rows_before = len(df)
    validated = df.copy()

    for col in numeric_columns:
        invalid_rows = []
        for index, value in validated[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except ValueError:
                    invalid_rows.append(index)

        if invalid_rows:
            logger.warning(
                "Removed %d rows with invalid numeric values in %s",
                len(invalid_rows),
                col,
            )
            validated = validated.drop(index=invalid_rows)

        validated[col] = pd.to_numeric(validated[col])

    logger.debug("Validation: %d -> %d rows", rows_before, len(validated))
    return validated
