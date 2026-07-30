class SignalFormatter:
    @staticmethod
    def telegram(
        symbol: str,
        strategy: str,
        signal: str,
        trend_timeframe: str,
        context_timeframe: str,
        entry_timeframe: str,
        price: float,
    ):

        return (
            f"Symbol: <b>{symbol}</b>\n"
            f"Strategy: <b>{strategy}</b>\n"
            f"Signal: <b>{signal}</b>\n"
            f"Timeframes: <b>{trend_timeframe}{f' - {context_timeframe}' if context_timeframe else ''}- {entry_timeframe}</b>\n"
            f"Price: <b>{price}</b>"
        )
