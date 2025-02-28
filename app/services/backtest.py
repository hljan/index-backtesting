"""Backtest service"""

from app.models.backtest import BacktestRequest, BacktestResponse


class BacktestService:
    """Backtest service"""
    
    def __init__(self):
        pass
    

    def run_backtest(self, backtest_request: BacktestRequest) -> BacktestResponse:
        r"""Run backtest based on user given rules and criteria
        
        **Parameters**
        - `backtest_request`: Request calendar rules and weighting criteria
        
        **Returns**
        - `BacktestResponse`: Backtest results with execution time and weights
        
        """
        # TODO: Implement backtest service
        return BacktestResponse()