"""Provide dependency injection for services"""

from typing import Annotated
from app.clients.data_loader import DataLoaderClient, ParquetLoaderClient
from app.services.backtest import BacktestService
from fastapi import Depends

def get_data_loader_client() -> DataLoaderClient:
    """Get the data loader client depending on the data source."""

    return ParquetLoaderClient()

def get_backtest_service(
        data_loader_client: Annotated[DataLoaderClient, Depends(get_data_loader_client)],
) -> BacktestService:
    """Get the backtest service."""

    return BacktestService(data_loader_client=data_loader_client)