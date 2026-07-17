from ingestion import DataSource
from datetime import datetime
from collections import deque
import time
import pandas as pd
import requests
from app.config import MISO_API_KEY

ENDPOINT = "https://apim.misoenergy.org/lgi/v1/real-time/{}/demand/actual?geoResolution=region&pageNumber=1&timeResolution=hourly"

MAX_REQUESTS_PER_WINDOW = 95 # MISO's API allows 100 requests per minute, so keeping max requests a little under
RATE_WINDOW_SECONDS = 60.0

def _respect_rate_limit(request_times: deque) -> None:
    now: float = time.monotonic()
    while request_times and now - request_times[0] >= RATE_WINDOW_SECONDS:
        request_times.popleft()

    if len(request_times) >= MAX_REQUESTS_PER_WINDOW:
        wait: float = RATE_WINDOW_SECONDS - (now - request_times[0])
        if wait > 0:
            print(f"Rate limit reached, sleeping {wait:.1f}s...")
            time.sleep(wait)

    request_times.append(time.monotonic())

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
        request_times: deque = deque()

        for date_string in date_strings:
            _respect_rate_limit(request_times)

            response: requests.Response = requests.get(
                url=ENDPOINT.format(date_string),
                headers={
                    "Ocp-Apim-Subscription-Key": MISO_API_KEY
                }
            )

            if response.status_code != 200 or (response.status_code == 200 and not response.json()):
                print(f"Failed to fetch MISO load data for {date_string}")
                print(response.text)
                continue

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
