from ingestion import DataSource
from datetime import datetime
from pandas import DataFrame
import pandas as pd
import requests
import time
from app.config import MISO_API_KEY

ENDPOINT: str = "https://apim.misoenergy.org/lgi/v1/real-time/{}/demand/actual?geoResolution=region&pageNumber=1&timeResolution=hourly"

class MISODataSource(DataSource):

    def fetch(self, start: datetime, end: datetime) -> DataFrame:
        unique_days: pd.DatetimeIndex = pd.date_range(start=start, end=end, freq="D")
        date_strings: list[str] = unique_days.strftime("%Y-%m-%d")

        for date_string in date_strings:
            response: requests.Response = requests.get(
                url=ENDPOINT.format(date_string),
                headers={
                    "Ocp-Apim-Subscription-Key": MISO_API_KEY
                }
            )