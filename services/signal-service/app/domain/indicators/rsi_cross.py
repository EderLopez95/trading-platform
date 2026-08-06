import pandas as pd

class RSICross:
    def __init__(self, rsi_min_distance=1.5): # minimum distance between two series to consider a crossover valid
        self.rsi_min_distance = rsi_min_distance

    def calculate_rsi_ema(self, series, period=14):
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
        avg_loss = loss.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def calculate_rsi_sma(self, series, period=14):
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=period, min_periods=period).mean()
        avg_loss = loss.rolling(window=period, min_periods=period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi

    def crossover(self, a, b):

        if len(a) < 2 or len(b) < 2:

            return False

        if (
            pd.isna(a.iloc[-1])
            or pd.isna(b.iloc[-1])
            or pd.isna(a.iloc[-2])
            or pd.isna(b.iloc[-2])
        ):
            
            return False

        a_current = float(a.iloc[-1])
        b_current = float(b.iloc[-1])
        a_prev = float(a.iloc[-2])
        b_prev = float(b.iloc[-2])
        
        crossed = (
            a_prev <= b_prev
            and a_current > b_current
        )
        distance = abs(a_current - b_current) > self.rsi_min_distance

        return crossed and distance
    
    def crossunder(self, a, b):
        
        if len(a) < 2 or len(b) < 2:

            return False

        if (
            pd.isna(a.iloc[-1])
            or pd.isna(b.iloc[-1])
            or pd.isna(a.iloc[-2])
            or pd.isna(b.iloc[-2])
        ):
            
            return False

        a_current = float(a.iloc[-1])
        b_current = float(b.iloc[-1])
        a_prev = float(a.iloc[-2])
        b_prev = float(b.iloc[-2])

        crossed = (
            a_prev >= b_prev
            and a_current < b_current
        )
        distance = abs(a_current - b_current) > self.rsi_min_distance

        return crossed and distance
