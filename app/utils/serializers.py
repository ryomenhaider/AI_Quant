from datetime import datetime

import pandas as pd


def dataframe_to_dict(df: pd.DataFrame) -> list[dict]:
    result = []
    for _, row in df.iterrows():
        item = {}
        for col, value in row.items():
            if isinstance(value, (pd.Timestamp, datetime)):
                item[col] = value.isoformat()
            elif hasattr(value, "item"):
                item[col] = value.item()
            else:
                item[col] = value
        result.append(item)
    return result
