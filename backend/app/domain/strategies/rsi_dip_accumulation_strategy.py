from app.domain.enums.enums import SignalType
from app.domain.strategies.utils import Utils
from app.domain.models.models import MarketData

class RSIDipAccumulationStrategy:
    def __init__(self):
        self.utils = Utils(rsi_min_distance=7)

    def execute(self, data: MarketData):
        # data from provider
        df_trend = data.trend
        df_entry = data.entry

        # minimum data points to calculate RSI and its moving average
        if len(df_trend) < 50 or len(df_entry) < 30:
            return SignalType.HOLD

        # calculate trend RSI
        trend_rsi = self.utils.calculate_rsi(df_trend["close"], 14)
        trend_rsi_ma = trend_rsi.rolling(14).mean()
        trend_rsi_v = trend_rsi.iloc[-1] # trend last value
        trend_rsi_ma_v = trend_rsi_ma.iloc[-1] # trend average last value
        trend_rsi_prev = trend_rsi.iloc[-2]
        trend_rsi_ma_prev = trend_rsi_ma.iloc[-2]

        # current and previous distance
        trend_distance = trend_rsi_ma_v - trend_rsi_v
        trend_distance_prev = trend_rsi_ma_prev - trend_rsi_prev

        # trend RSI bearish with minimum force
        trend_bearish = (
            trend_distance >= 5 or
            trend_distance_prev >= 5
        )

        # bearish momentum increasing
        bearish_strengthening = (
            trend_distance >= trend_distance_prev
        )

        # calculate entry RSI
        entry_rsi = self.utils.calculate_rsi(df_entry["close"], 14)
        entry_rsi_ma = entry_rsi.rolling(14).mean()
        entry_rsi_v = entry_rsi.iloc[-1]
        entry_rsi_ma_v = entry_rsi_ma.iloc[-1]

        # distance between average and RSI
        entry_distance = entry_rsi_ma_v - entry_rsi_v

        # entry still weak
        entry_bearish = entry_distance >= 3

        # SMA20 price discount
        sma20 = df_entry["close"].rolling(20).mean()
        sma20_v = sma20.iloc[-1]
        close_v = df_entry["close"].iloc[-1]

        # % distance below SMA20
        price_distance = (sma20_v - close_v) / sma20_v
        discounted_price = (
            close_v < sma20_v and
            price_distance > 0.015
        )

        # SMA20 slightly falling
        sma20_slope = sma20_v - sma20.iloc[-3]
        sma20_falling = sma20_slope < 0

        if (
            trend_bearish and
            bearish_strengthening and
            entry_bearish and
            discounted_price and
            sma20_falling
        ):
            return SignalType.BUY
        
        return SignalType.HOLD
