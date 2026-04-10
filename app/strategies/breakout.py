import pandas as pd
import numpy as np


def generate_signals(df: pd.DataFrame, window: int = 20) -> pd.Series:
    high = df["high"]
    low = df["low"]

    rolling_high = high.rolling(window=window).max().shift(1)
    rolling_low = low.rolling(window=window).min().shift(1)

    entries = high > rolling_high
    exits = low < rolling_low

    signals = pd.Series(np.zeros(len(df)), index=df.index, dtype=bool)
    signals[entries] = True
    signals[exits] = False

    return signals
