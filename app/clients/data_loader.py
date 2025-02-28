"""Provide interface and implementation for data loader"""

from abc import ABC, abstractmethod
import os
import pandas as pd

from app.models.data_field import DataField
from app.utils.generate_data import generate_dummy_data


class DataLoaderClient(ABC):
    """Abstract base class for data loader client."""

    dataset: pd.DataFrame
    
    @abstractmethod
    def load_data(self, data_field: DataField) -> None:
        """Load data from data source."""
        pass

class ParquetLoaderClient(DataLoaderClient):
    """Parquet loader client."""
    
    def load_data(self, data_field: DataField) -> None:
        """Load data from parquet files."""

        file_path = f"data/{data_field}.parquet"
        if not os.path.exists(file_path):
            # Parquet file does not exist. Trying to generate and load from data generation script.
            generate_dummy_data()

        try:
            self.dataset = pd.read_parquet(file_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data field {data_field} does not exist and cannot be generated.")
