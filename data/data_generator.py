""" Generate dummy data for testing """

import pandas as pd
import numpy as np

# Generate data under data/ folder
path = "data/"

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