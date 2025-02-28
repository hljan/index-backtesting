"""Provide enum for filters in backtesting"""

from enum import Enum


class CalendarRule(str, Enum):
    """Calendar rule for backtesting"""

    CUSTOMER_DATES = "customer_dates"
    QUARTERLY_DATES = "quarterly_dates"

class FilterType(str, Enum):
    """Filter type for backtesting"""

    TOP_N_SECURITIES = "top_n_securities"
    FILTER_BY_VALUE = "filter_by_value"

class WeightingMethod(str, Enum):
    """Weighting method for backtesting"""

    EQUAL_WEIGHT = "equal_weight"
    OPTIMIZED_WEIGHT = "optimized_weight"
