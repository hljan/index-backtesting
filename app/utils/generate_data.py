""" Generate dummy data for testing """

import os
import pandas as pd
import numpy as np

# Generate data under data/ folder
def generate_dummy_data(path="data/"):
    if not os.path.exists(path):
        os.makedirs(path)

    data_field_identifiers = [
        "market_capitalization",
        "prices",
        "volume",
        "adtv_3_month"
    ]

    securities = list(map(str, range(1000)))  # Unique security identifiers
    dates = pd.date_range("2020-01-01", "2025-01-22")

    for data_field_identifier in data_field_identifiers:
        data = np.random.uniform(low=1, high=100, size=(len(dates), len(securities)))
        data = pd.DataFrame(
            data,
            index=dates,
            columns=securities
        )
        data.to_parquet(f"{path}/{data_field_identifier}.parquet")

if __name__ == "__main__":
    generate_dummy_data()