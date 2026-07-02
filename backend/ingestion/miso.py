from ingestion import DataSource
from datetime import datetime
import pandas as pd
import requests
from app.config import MISO_API_KEY

ENDPOINT: str = "https://apim.misoenergy.org/lgi/v1/real-time/{}/demand/actual?geoResolution=region&pageNumber=1&timeResolution=hourly"

class MISODataSource(DataSource):

    def fetch(self, start: datetime, end: datetime) -> list[dict]:
        unique_days: pd.DatetimeIndex = pd.date_range(start=start, end=end, freq="D")
        date_strings: pd.Index[str] = unique_days.strftime("%Y-%m-%d")

        load_by_timestamp: dict[str: float] = {}

        for date_string in date_strings:
            response: requests.Response = requests.get(
                url=ENDPOINT.format(date_string),
                headers={
                    "Ocp-Apim-Subscription-Key": MISO_API_KEY
                }
            )

            if response.status_code != 200 or (response.status_code == 200 and not response.json()):
                print(f"Failed to fetch MISO load data for {date_string}")
                return

            response_data = response.json()["data"]
            
            for datapoint in response_data:
                timestamp: datetime = datetime.fromisoformat(datapoint["timeInterval"]["start"])
                if not (start <= timestamp <= end):
                    continue
                load_mw: float = float(datapoint["load"])

                if timestamp in load_by_timestamp:
                    load_by_timestamp[timestamp] = load_by_timestamp[timestamp] + load_mw
                else:
                    load_by_timestamp[timestamp] = load_mw

        raw_data: list[dict] = []
        
        for timestamp, load_mw in load_by_timestamp.items():
            raw_data.append({
                "timestamp": timestamp,
                "load_mw": load_mw
            })

        return raw_data
                
                