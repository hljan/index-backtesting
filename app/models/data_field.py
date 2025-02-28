"""Provide enum for data fields"""

from enum import Enum


class DataField(str, Enum):
    """Enum for backtest data field."""

    MARKET_CAPITALIZATION = "market_capitalization"
    PRICES = "prices"
    VOLUME = "volume"
    ADTV_3_MONTH = "adtv_3_month"