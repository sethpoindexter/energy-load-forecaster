from abc import ABC, abstractmethod
from datetime import datetime

class DataSource(ABC):

    @abstractmethod
    def fetch(self, start: datetime, end: datetime) -> list[dict]:
        pass