from ingestion import DataSource
from datetime import datetime
import pandas as pd
import requests
from app.config import MISO_API_KEY

ENDPOINT = "https://apim.misoenergy.org/lgi/v1/real-time/{}/demand/actual?geoResolution=region&pageNumber=1&timeResolution=hourly"

class MISODataSource(DataSource):

    def fetch(self, start: datetime, end: datetime) -> list[dict]:
        today = datetime.today()
        if start > today or end > today:
            print("Failed to fetch MISO load data. Start and end dates must occur before today's date.")
            return None
        if start > end:
            print("Failed to fetch MISO load data. Start date must occur before end date.")
            return None
        
        unique_days: pd.DatetimeIndex = pd.date_range(start=start, end=end, freq="D")
        date_strings: pd.Index[str] = unique_days.strftime("%Y-%m-%d")

        raw_data: list[dict] = []

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
                timestamp = datetime.fromisoformat(datapoint["timeInterval"]["start"])
                if not (start <= timestamp <= end):
                    continue

                raw_data.append({
                    "timestamp": timestamp,
                    "region": datapoint["region"],
                    "load_mw": float(datapoint["load"])
                })

        return raw_data
