"""Provide models for the backtest endpoint"""

import datetime
from app.models.data_field import DataField
from app.models.filters import CalendarType, FilterType, WeightingMethod
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Dict, List, Literal, Optional, Union

class BacktestRequest(BaseModel):
    """Request model for backtesting."""

    model_config = ConfigDict(alias_generator=to_camel) # For better JSON serialization

    data_field: DataField
    calendar_rule: Union[
        Literal[CalendarType.CUSTOMER_DATES],
        Literal[CalendarType.QUARTERLY_DATES]
    ]
    filter_type: Union[
        Literal[FilterType.TOP_N_SECURITIES],
        Literal[FilterType.FILTER_BY_VALUE]
    ]
    weighting_method: Union[
        Literal[WeightingMethod.OPTIMIZED_WEIGHT],
        Literal[WeightingMethod.EQUAL_WEIGHT]
    ]
    list_of_dates: Optional[List[datetime.datetime]] = None
    initial_date: Optional[datetime.datetime] = None
    end_date: Optional[datetime.datetime] = datetime.datetime(2025, 1, 22)
    top_n: Optional[int] = None
    filter_value: Optional[float] = None
    weighting_minimum: Optional[float] = None
    weighting_maximum: Optional[float] = None

class BacktestResponse(BaseModel):
    """Response model for backtesting."""

    execution_time: float
    weights: Dict[datetime.datetime, Dict[str, float]]
