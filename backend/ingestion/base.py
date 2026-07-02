from abc import ABC, abstractmethod
from datetime import datetime
from pandas import DataFrame

class DataSource(ABC):

    @abstractmethod
    def fetch(self, start: datetime, end: datetime) -> DataFrame:
        pass