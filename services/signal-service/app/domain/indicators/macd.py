import pandas as pd

class MACD:
    def __init__(self, fast_period=12, slow_period=26, signal_period=9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    def calculate(self, series):
        ema_fast = series.ewm(span=self.fast_period, adjust=False, min_periods=self.fast_period).mean()
        ema_slow = series.ewm(span=self.slow_period, adjust=False, min_periods=self.slow_period).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=self.signal_period, adjust=False, min_periods=self.signal_period).mean()
        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    def rising(self, series):

        if len(series) < 2:

            return False

        if pd.isna(series.iloc[-1]) or pd.isna(series.iloc[-2]):

            return False

        return float(series.iloc[-1]) > float(series.iloc[-2])

    def falling(self, series):

        if len(series) < 2:

            return False

        if pd.isna(series.iloc[-1]) or pd.isna(series.iloc[-2]):

            return False

        return float(series.iloc[-1]) < float(series.iloc[-2])
