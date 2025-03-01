"""Backtest service"""

from abc import ABC, abstractmethod
import time
import pandas as pd
import numpy as np
from app.clients.data_loader import DataLoaderClient
from app.models.backtest import BacktestRequest, BacktestResponse
from app.utils.check_rule import (
    is_custom_dates,
    is_filter_by_value, 
    is_quarterly_dates,
    is_top_n_securities,
    is_weighting_method_equal_weight,
    is_weighting_method_optimized_weight,
)

class Rule(ABC):
    """Abstract base class for rules."""

    @abstractmethod
    def apply(self, dataset: pd.DataFrame, request: BacktestRequest) -> pd.DataFrame:
        """Apply the rule to the dataset."""
        pass

class CalendarRule(Rule):
    """Calendar rule class"""

    def apply(self, dataset: pd.DataFrame, request: BacktestRequest) -> pd.DataFrame:
        """Apply the calendar rule to the dataset."""

        filtered_data = dataset.copy()
        if is_custom_dates(request):
            filtered_data = filtered_data[filtered_data.index.isin(request.list_of_dates)]
        elif is_quarterly_dates(request):
            filtered_data = filtered_data[
                (filtered_data.index >= request.initial_date) & (filtered_data.index <= request.end_date)
            ]
        else:
            raise ValueError("Calendar rule is not supported.")
        return filtered_data

class FilterRule(Rule):
    """Filter rule class"""

    def apply(self, dataset: pd.DataFrame, request: BacktestRequest) -> pd.DataFrame:
        """Apply the filter rule to the dataset."""

        filtered_data = dataset.copy()
        if is_top_n_securities(request):
            filtered_data = filtered_data.nlargest(request.top_n, filtered_data.columns)
        elif is_filter_by_value(request):
            filtered_data = filtered_data[self.filtered_data > request.filter_value]
        else:
            raise ValueError("Filter rule is not supported.")
        return filtered_data

class WeightingRule(Rule):
    """Weighting rule class"""

    def apply(self, dataset: pd.DataFrame, request: BacktestRequest) -> None:
        """Apply the weighting rule to the dataset."""

        filtered_data = dataset.copy()
        if is_weighting_method_equal_weight(request):
            filtered_data *= 1 / len(filtered_data)
            filtered_data = filtered_data.sum(axis=1)
        elif is_weighting_method_optimized_weight(request):
            optimal_weights = np.full_like(filtered_data.values, request.weighting_minimum)
            remaining_weight = 1 - np.sum(optimal_weights, axis=1)
            for i in range(filtered_data.shape[1]):
                additional_weight = np.minimum(request.weighting_minimum - optimal_weights[:, i], remaining_weight)
                optimal_weights[:, i] += additional_weight
                remaining_weight -= additional_weight
            filtered_data = filtered_data * optimal_weights
            filtered_data = filtered_data.sum(axis=1)
        else:
            raise ValueError("Weighting rule is not supported.")
        return filtered_data

class BacktestService:
    """Backtest service"""

    rules: list[Rule]
    
    def __init__(self, data_loader_client: DataLoaderClient):
        self.rules = [
            CalendarRule(),
            FilterRule(),
            WeightingRule()
        ]
        self.data_loader_client = data_loader_client
    

    def run_backtest(self, request: BacktestRequest) -> BacktestResponse:
        r"""Run backtest based on user given rules and criteria
        
        **Parameters**
        - `backtest_request`: Request calendar rules and weighting criteria
        
        **Returns**
        - `BacktestResponse`: Backtest results with execution time and weights
        
        """
        
        self.data_loader_client.load_data(request.data_field)
        dataset = self.data_loader_client.dataset

        # time the execution
        start = time.time()
        for rule in self.rules:
            dataset = rule.apply(dataset=dataset, request=request)
        end = time.time()

        execution_time = end - start
        weights = dataset.to_dict() if not dataset.empty else {}
        return BacktestResponse(execution_time=execution_time, weights=weights)
