"""Provide models for the backtest endpoint"""

import datetime
from app.models.filters import CalendarRule, FilterType, WeightingMethod
from pydantic import BaseModel
from typing import Dict, List, Optional

class BacktestRequest(BaseModel):
    # Calendar rule
    calendar_rule: CalendarRule
    list_of_dates: Optional[List[datetime.datetime]] = None # for customer dates
    initial_date: Optional[datetime.datetime] = None # for quarterly dates
    end_date: Optional[datetime.datetime] = datetime.datetime(2025, 1, 22) # for quarterly dates, set 2025-01-22 as default
    # Portfolio filter
    filter_type: FilterType
    filter_field: str # for both filter types
    top_n: Optional[int] = None # for top N securities
    filter_value: Optional[float] = None # for filter by value
    # Weighting method
    weighting_method: WeightingMethod
    weighting_field: Optional[str] = None # for optimized weight
    weighting_minimum: Optional[float] = None # for optimized weight
    weighting_maximum: Optional[float] = None # for optimized weight

class BacktestResponse(BaseModel):
    execution_time: float
    weights: Dict[datetime.datetime, Dict[str, float]]