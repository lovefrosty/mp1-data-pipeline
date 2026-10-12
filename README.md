# MP1 Data Pipeline

This project is an end-to-end data pipeline that loads, validates, cleans, and saves data using configurable settings. The functions in `src/data_loaders.py` load CSV, JSON, and YAML files; the complete cleaning run uses the provided CSV, with YAML supplying the configuration. `pipeline.py` checks the input paths, loads the configuration, and runs the validation, cleaning, reporting, and output steps. `src/data_validator.py` confirms the input is a table, checks for required columns, converts configured numeric columns, and removes rows with invalid numeric values. `src/data_processor.py` removes duplicates, handles missing values, removes configured outliers, and creates a before-and-after report. `src/data_output.py` saves the cleaned data as a CSV without an index and creates the output directory when needed. `src/utils.py` provides logging and input-path checks, while `src/__init__.py` makes the module functions available to `pipeline.py`.

Run the sample pipeline from the repository root:

```bash
python3 pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Example output from the provided sample:

```text
17:49:23 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
17:49:23 INFO     src.utils — Input file validated: fixtures/sample_data.csv
17:49:23 INFO     src.utils — Input file validated: config/config.yaml
17:49:23 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
17:49:23 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
17:49:23 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
17:49:23 DEBUG    src.data_validator — Validation: 100 -> 98 rows
17:49:23 INFO     __main__ — Validation complete: 100 -> 98 rows
17:49:23 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
17:49:23 DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
17:49:23 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, removed=2
17:49:23 INFO     __main__ — Processing complete: 98 -> 92 rows
17:49:23 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
17:49:23 INFO     __main__ — Saved cleaned data to output/clean.csv
Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```

The cleaned CSV is written to `output/clean.csv`.
