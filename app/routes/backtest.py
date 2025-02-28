"""Provide API endpoint for backtesting"""

from typing import Annotated
from app.models.backtest import BacktestRequest, BacktestResponse
from app.routes.dependencies import get_backtest_service
from app.services.backtest import BacktestService
from fastapi import APIRouter, Depends

router = APIRouter()

@router.post(path="/backtest", tags=["backtest"], response_model_exclude_none=True)
async def backtest(
    backtest_service: Annotated[BacktestService, Depends(get_backtest_service)],
    backtest_request: BacktestRequest
) -> BacktestResponse:
    r"""Run backtest based on user given rules and criteria
    
    **Parameters**
    - `backtest_service`: Backtesting service
    - `backtest_request`: Request calendar rules and weighting criteria
    
    **Returns**
    - `BacktestResponse`: Backtest results with execution time and weights

    """
    
    return backtest_service.run_backtest(request=backtest_request)