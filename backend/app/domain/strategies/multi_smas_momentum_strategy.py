from app.domain.enums.enums import SignalType
from app.domain.strategies.utils import Utils
from app.domain.models.models import MarketData
import pandas as pd

class MultiSMAsMomentumStrategy:
    def __init__(self):
        self.utils = Utils()

    def execute(self, data: MarketData):
        # data from provider
        df_trend = data.trend
        df_entry = data.entry

        # minimum data to validate trend and entry
        if len(df_trend) < 200 or len(df_entry) < 30:
            return SignalType.HOLD

        # calculate SMAs (averages, last value)
        sma20 = df_trend["close"].rolling(20).mean()
        sma40 = df_trend["close"].rolling(40).mean()
        sma100 = df_trend["close"].rolling(100).mean()
        sma200 = df_trend["close"].rolling(200).mean()
        sma20_v = sma20.iloc[-1]
        sma40_v = sma40.iloc[-1]
        sma100_v = sma100.iloc[-1]
        sma200_v = sma200.iloc[-1]

        if pd.isna(sma200_v): # in case of invalid data
            return SignalType.HOLD

        # determine trend based on SMA order
        bullish_trend = (
            sma20_v > sma40_v and
            sma40_v > sma100_v
        )
        bearish_trend = (
            sma20_v < sma40_v and
            sma40_v < sma100_v
        )

        # calculate RSI entry
        rsi = self.utils.calculate_rsi(df_entry["close"], 14)
        rsi_ma = rsi.rolling(14).mean()
        bullish_cross = self.utils.crossover(rsi, rsi_ma)
        bearish_cross = self.utils.crossunder(rsi, rsi_ma)
        
        # calculate tick volume (price changes not market volume, considerate for other providers)
        volume_avg = df_entry["tick_volume"].rolling(20).mean()
        if pd.isna(volume_avg.iloc[-1]): # in case of invalid data
            return SignalType.HOLD
        volume_v = df_entry["tick_volume"].iloc[-1]
        volume_avg_v = volume_avg.iloc[-1] # last tick volume
        volume_ok = volume_v > (volume_avg_v * 1.2) # considerable movement, increase it to filter more deeply

        if bullish_trend and bullish_cross and volume_ok:
            return SignalType.BUY

        if bearish_trend and bearish_cross and volume_ok:
            return SignalType.SELL

        return SignalType.HOLD
