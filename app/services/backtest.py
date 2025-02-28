"""Backtest service"""

from abc import ABC, abstractmethod
from datetime import time
from pandas import pd
from app.clients.data_loader import DataLoaderClient
from app.models.backtest import BacktestRequest, BacktestResponse

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
        match request:
            case request.create_with_custom_dates():
                filtered_data = filtered_data[filtered_data["date"].isin(request.list_of_dates)]
            case request.create_with_quarterly_dates():
                filtered_data = filtered_data[
                    (filtered_data["date"] >= request.initial_date) & (filtered_data["date"] <= request.end_date)
                ]
            case _:
                raise ValueError("Calendar rule is not supported.")
        return filtered_data

class FilterRule(Rule):
    """Filter rule class"""

    def apply(self, dataset: pd.DataFrame, request: BacktestRequest) -> pd.DataFrame:
        """Apply the filter rule to the dataset."""

        filtered_data = dataset.copy()
        match request:
            case request.create_with_top_n_securities():
                filtered_data = filtered_data.nlargest(request.top_n, "value")
            case request.create_with_filter_by_value():
                filtered_data = filtered_data[self.filtered_data["value"] > request.filter_value]
            case _:
                raise ValueError("Filter rule is not supported.")
        return filtered_data

class WeightingRule(Rule):
    """Weighting rule class"""

    def apply(self, dataset: pd.DataFrame, request: BacktestRequest) -> None:
        """Apply the weighting rule to the dataset."""

        filtered_data = dataset.copy()
        match request:
            case request.create_with_weighting_method_equal_weight():
                filtered_data *= 1 / len(filtered_data)
                filtered_data = filtered_data.sum(axis=1)
            case request.create_with_weighting_method_optimized_weight():
                # TODO: Implement optimized weighting logic
                filtered_data = filtered_data.fillna(1)
                filtered_data = filtered_data.sum(axis=1)
            case _:
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

        # time the execution
        start = time.time()
        for rule in self.rules:
            self.data_loader_client.dataset = rule.apply(dataset=self.data_loader_client.dataset, request=request)
        end = time.time()

        execution_time = end - start
        weights = self.data_loader_client.dataset.to_dict()
        return BacktestResponse(execution_time=execution_time, weights=weights)