from app.domain.enums.enums import SignalType
from app.domain.strategies.utils import Utils
from app.domain.models.models import MarketData

class RSICrossTrendStrategy:
    def __init__(self):
        self.utils = Utils()

    def execute(self, data: MarketData):
        # data from provider, only by trend
        df_trend = data.trend

        # minimum data points to calculate RSI and its moving average
        if len(df_trend) < 50:
            return SignalType.HOLD

        # calculate RSI
        rsi = self.utils.calculate_rsi(df_trend["close"], 14)
        rsi_ma = rsi.rolling(14).mean()
        bullish_cross = self.utils.crossover(rsi, rsi_ma)
        bearish_cross = self.utils.crossunder(rsi, rsi_ma)

        if bullish_cross:
            return SignalType.BUY

        if bearish_cross:
            return SignalType.SELL

        return SignalType.HOLD
