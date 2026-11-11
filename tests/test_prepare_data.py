import pandas as pd
import pytest

from src.prepare_data import clean_data


@pytest.fixture
def trip():
    return {
        "vendor_id": 1,
        "passenger_count": 2,
        "pickup_longitude": -74,
        "pickup_latitude": 40,
        "dropoff_longitude": -74,
        "dropoff_latitude": 40,
        "store_and_fwd_flag": "N",
        "trip_duration": 1200,
    }


def test_keeps_valid_trips_including_long_ones(trip):
    trips = pd.DataFrame([
        {**trip, "trip_duration": seconds} for seconds in [1, 3601, 86400]
    ])
    pd.testing.assert_frame_equal(clean_data(trips), trips)


def test_fills_missing_values_without_changing_input(trip):
    trips = pd.DataFrame([trip, trip, {**trip, "passenger_count": None,
                                       "store_and_fwd_flag": None}])
    original = trips.copy()
    result = clean_data(trips)
    assert result["passenger_count"].tolist() == [2, 2, 2]
    assert result["store_and_fwd_flag"].tolist() == ["N", "N", "N"]
    pd.testing.assert_frame_equal(trips, original)


@pytest.mark.parametrize(("column", "invalid"), [
    ("vendor_id", 3),
    ("passenger_count", 0),
    ("passenger_count", 7),
    ("pickup_longitude", -80),
    ("pickup_latitude", 50),
    ("dropoff_longitude", -80),
    ("dropoff_latitude", 50),
    ("store_and_fwd_flag", "X"),
    ("trip_duration", 0),
    ("trip_duration", 86401),
])
def test_drops_invalid_trip(trip, column, invalid):
    trips = pd.DataFrame([trip, {**trip, column: invalid}])
    pd.testing.assert_frame_equal(clean_data(trips), trips.iloc[:1])
