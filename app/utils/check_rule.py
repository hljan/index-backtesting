"""Utils to check the rules of the backtest request"""

from app.models.backtest import BacktestRequest
from app.models.filters import CalendarType, FilterType, WeightingMethod


def is_custom_dates(request: BacktestRequest) -> bool:
    return request.calendar_rule == CalendarType.CUSTOMER_DATES and request.list_of_dates is not None

def is_quarterly_dates(request: BacktestRequest) -> bool:
    return request.calendar_rule == CalendarType.QUARTERLY_DATES and request.initial_date is not None

def is_top_n_securities(request: BacktestRequest) -> bool:
    return request.filter_type == FilterType.TOP_N_SECURITIES and request.top_n is not None

def is_filter_by_value(request: BacktestRequest) -> bool:
    return request.filter_type == FilterType.FILTER_BY_VALUE and request.filter_value is not None

def is_weighting_method_equal_weight(request: BacktestRequest) -> bool:
    return request.weighting_method == WeightingMethod.EQUAL_WEIGHT

def is_weighting_method_optimized_weight(request: BacktestRequest) -> bool:
    return request.weighting_method == WeightingMethod.OPTIMIZED_WEIGHT and request.weighting_minimum is not None and request.weighting_maximum is not None
