"""Provide models for the backtest endpoint"""

import datetime
from app.models.data_field import DataField
from app.models.filters import CalendarRule, FilterType, WeightingMethod
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Dict, List, Literal, Optional, Union

class BacktestRequest(BaseModel):
    """Request model for backtesting."""

    model_config = ConfigDict(alias_generator=to_camel) # For better JSON serialization

    data_field: DataField
    calendar_rule: Union[
        Literal[CalendarRule.CUSTOMER_DATES],
        Literal[CalendarRule.QUARTERLY_DATES]
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

    @classmethod
    def create_with_custom_dates(cls, data_field: DataField, list_of_dates: List[datetime.datetime], **kwargs):
        return cls(
            data_field=data_field,
            calendar_rule=CalendarRule.CUSTOMER_DATES,
            list_of_dates=list_of_dates,
            **kwargs
        )

    @classmethod
    def create_with_quarterly_dates(cls, data_field: DataField, initial_date: datetime.datetime, end_date: Optional[datetime.datetime] = datetime.datetime(2025, 1, 22), **kwargs):
        return cls(
            data_field=data_field,
            calendar_rule=CalendarRule.QUARTERLY_DATES,
            initial_date=initial_date,
            end_date=end_date,
            **kwargs
        )

    @classmethod
    def create_with_top_n_securities(cls, data_field: DataField, top_n: int, **kwargs):
        return cls(
            data_field=data_field,
            filter_type=FilterType.TOP_N_SECURITIES,
            top_n=top_n,
            **kwargs
        )

    @classmethod
    def create_with_filter_by_value(cls, data_field: DataField, filter_value: float, **kwargs):
        return cls(
            data_field=data_field,
            filter_type=FilterType.FILTER_BY_VALUE,
            filter_value=filter_value,
            **kwargs
        )

    @classmethod
    def create_with_optimized_weight(cls, data_field: DataField, weighting_minimum: float, weighting_maximum: float, **kwargs):
        return cls(
            data_field=data_field,
            weighting_method=WeightingMethod.OPTIMIZED_WEIGHT,
            weighting_minimum=weighting_minimum,
            weighting_maximum=weighting_maximum,
            **kwargs
        )

    @classmethod
    def create_with_equal_weight(cls, data_field: DataField, **kwargs):
        return cls(
            data_field=data_field,
            weighting_method=WeightingMethod.EQUAL_WEIGHT,
            **kwargs
        )

class BacktestResponse(BaseModel):
    """Response model for backtesting."""

    model_config = ConfigDict(alias_generator=to_camel) # For better JSON serialization

    execution_time: float
    weights: Dict[datetime.datetime, Dict[str, float]]
