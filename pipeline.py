"""Command-line entry point for the MP1 data pipeline."""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse the paths and options used to run the pipeline."""
    parser = argparse.ArgumentParser(description="Run the data processing pipeline.")
    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument(
        "--output", "-o", required=True, help="Path to the cleaned CSV output"
    )
    parser.add_argument(
        "--config", required=True, help="Path to the YAML configuration file"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    return parser.parse_args()


def main():
    """Load, validate, process, and save the configured dataset."""
    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(
        "Arguments parsed: input=%s, config=%s, output=%s",
        args.input,
        args.config,
        args.output,
    )

    if not validate_input(args.input) or not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError as error:
        logger.error("Could not load input or configuration: %s", error)
        sys.exit(1)

    validation_config = config["validation"]
    required_columns = validation_config["required_columns"]
    numeric_columns = validation_config["numeric_columns"]
    rows_before_validation = len(data)
    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError as error:
        logger.error("Data validation failed: %s", error)
        sys.exit(1)
    logger.info(
        "Validation complete: %d -> %d rows",
        rows_before_validation,
        len(data),
    )
    data_before = data.copy()

    try:
        data = process_data(data, config)
    except ValueError as error:
        logger.error("Data processing failed: %s", error)
        sys.exit(1)

    cleaning_report = create_cleaning_report(data_before, data)
    logger.info("Processing complete: %d -> %d rows", len(data_before), len(data))
    saved_path = save_data(data, args.output)
    logger.info("Saved cleaned data to %s", saved_path)

    print("Cleaning report:")
    print(cleaning_report)


if __name__ == "__main__":
    main()
