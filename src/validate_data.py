import great_expectations as gx
import pandas as pd
from great_expectations import expectations as ge

from src.prepare_data import RAW_FILE, clean_data

COLUMNS = [
    "id", "vendor_id", "pickup_datetime", "dropoff_datetime", "passenger_count",
    "pickup_longitude", "pickup_latitude", "dropoff_longitude", "dropoff_latitude",
    "store_and_fwd_flag", "trip_duration",
]


def make_validation():
    context = gx.get_context(mode="ephemeral")
    context.config.progress_bars = {"globally": False}
    source = context.data_sources.add_pandas(name="taxi")
    asset = source.add_dataframe_asset(name="trips")
    batch = asset.add_batch_definition_whole_dataframe("all_rows")
    suite = gx.ExpectationSuite(name="taxi_contract")
    suite.add_expectation(ge.ExpectTableColumnsToMatchSet(column_set=COLUMNS))
    suite.add_expectation(ge.ExpectTableRowCountToBeBetween(min_value=1))

    for column in COLUMNS:
        suite.add_expectation(ge.ExpectColumnValuesToNotBeNull(column=column))

    for column, values in [
        ("vendor_id", [1, 2]), ("store_and_fwd_flag", ["N", "Y"]),
    ]:
        suite.add_expectation(
            ge.ExpectColumnValuesToBeInSet(column=column, value_set=values)
        )

    for column, low, high in [
        ("passenger_count", 1, 6),
        ("pickup_longitude", -75, -72),
        ("pickup_latitude", 39, 42),
        ("dropoff_longitude", -75, -72),
        ("dropoff_latitude", 39, 42),
        ("trip_duration", 1, 86400),
    ]:
        suite.add_expectation(
            ge.ExpectColumnValuesToBeBetween(column=column, min_value=low, max_value=high)
        )

    suite = context.suites.add(suite)
    return context.validation_definitions.add(
        gx.ValidationDefinition(name="check_taxi", data=batch, suite=suite)
    )


def check_table(validation, data, label):
    result = validation.run(
        batch_parameters={"dataframe": data},
        result_format={"result_format": "BASIC", "partial_unexpected_count": 0},
    )
    passed = result.statistics["successful_expectations"]
    total = result.statistics["evaluated_expectations"]
    print(f"{label}: {len(data)} rows, {passed}/{total} checks passed", flush=True)
    for item in result.results:
        if not item.success:
            rule = item.expectation_config
            column = rule.kwargs.get("column", "table")
            count = item.result.get("unexpected_count", "n/a")
            print(f"  {column}: {rule.type}, invalid values: {count}", flush=True)
    return result.success


def main():
    raw = pd.read_csv(RAW_FILE)
    validation = make_validation()
    check_table(validation, raw, "Raw data")
    cleaned = clean_data(raw)
    print(f"Rows removed: {len(raw) - len(cleaned)}", flush=True)
    if not check_table(validation, cleaned, "Clean data"):
        raise SystemExit("Cleaned data failed the contract.")


if __name__ == "__main__":
    main()
