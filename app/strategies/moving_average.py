import pandas as pd
import numpy as np


def generate_signals(
    df: pd.DataFrame, fast_window: int = 10, slow_window: int = 50
) -> pd.Series:
    close = df["close"]

    fast_ma = close.rolling(window=fast_window).mean()
    slow_ma = close.rolling(window=slow_window).mean()

    entries = (fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1))
    exits = (fast_ma < slow_ma) & (fast_ma.shift(1) >= slow_ma.shift(1))

    signals = pd.Series(np.zeros(len(df)), index=df.index, dtype=bool)
    signals[entries] = True
    signals[exits] = False

    return signals
