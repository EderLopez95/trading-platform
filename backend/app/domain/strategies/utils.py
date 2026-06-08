import pandas as pd

class Utils:
    def __init__(self):
        self.MIN_DISTANCE = 1.5 # minimum distance between two series to consider a crossover valid

    def calculate_rsi(self, series, period=14):
        delta = series.diff() # price change between candles
        gain = delta.clip(lower=0) # only positive movements
        loss = -delta.clip(upper=0) # only negative movements
        avg_gain = gain.ewm(alpha=1/period, adjust=False).mean() # earnings average (wilder ema)
        avg_loss = loss.ewm(alpha=1/period, adjust=False).mean() # losses average (wilder ema)
        rs = avg_gain / avg_loss # correlation
        rsi = 100 - (100 / (1 + rs)) # scale 0-100
        return rsi

    def crossover(self, a, b):
        if len(a) < 2 or len(b) < 2: # in case of insufficient data, at least 2 values
            return False

        if pd.isna(a.iloc[-1]) or pd.isna(b.iloc[-1]): # in case of invalid data
            return False

        crossed = (
            a.iloc[-2] <= b.iloc[-2] and
            a.iloc[-1] > b.iloc[-1]
        )
        distance = abs(a.iloc[-1] - b.iloc[-1]) > self.MIN_DISTANCE # check for enough min distance
        return crossed and distance # only valid if both are true

    # same as crossover but backwards validation
    def crossunder(self, a, b):
        if len(a) < 2 or len(b) < 2:
            return False

        if pd.isna(a.iloc[-1]) or pd.isna(b.iloc[-1]):
            return False

        crossed = (
            a.iloc[-2] >= b.iloc[-2] and
            a.iloc[-1] < b.iloc[-1]
        )
        distance = abs(a.iloc[-1] - b.iloc[-1]) > self.MIN_DISTANCE
        return crossed and distance
