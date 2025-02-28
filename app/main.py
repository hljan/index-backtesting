"""Bootstrap the application"""

from fastapi import FastAPI
from app.routes import backtest

app = FastAPI()

app.include_router(backtest.router, prefix="/v1")