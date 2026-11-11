from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "nyc-taxi-trip-duration.zip"
OUTPUT_FILE = ROOT / "data" / "processed" / "nyc_taxi_clean.csv"


def clean_data(data):
    data = data.copy()
    for column in data.columns:
        if data[column].isna().any():
            mode = data[column].mode()
            if not mode.empty:
                data[column] = data[column].fillna(mode.iloc[0])

    valid_mask = (
        data["vendor_id"].isin([1, 2])
        & data["passenger_count"].between(1, 6)
        & data["pickup_longitude"].between(-75, -72)
        & data["pickup_latitude"].between(39, 42)
        & data["dropoff_longitude"].between(-75, -72)
        & data["dropoff_latitude"].between(39, 42)
        & data["store_and_fwd_flag"].isin(["N", "Y"])
        & data["trip_duration"].between(1, 86400)
    )
    return data.loc[valid_mask].copy()


def main():
    raw_data = pd.read_csv(RAW_FILE)
    cleaned = clean_data(raw_data)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_FILE, index=False)
    print(f"Rows: {len(raw_data)} -> {len(cleaned)}")
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
