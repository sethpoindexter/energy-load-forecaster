import pandas as pd
import numpy as np

def normalize(raw_data: list[dict], source: str) -> pd.DataFrame:
    df = pd.DataFrame(raw_data)

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["load_mw"] = df["load_mw"].astype(int)
    df["source"] = source
    
    df = df.drop_duplicates(subset=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    return df