class SignalFormatter:
    @staticmethod
    def telegram(
        symbol: str,
        strategy: str,
        signal: str,
        timeframe: str,
        price: float,
    ):

        return (
            f"Symbol: <b>{symbol}</b>\n"
            f"Strategy: <b>{strategy}</b>\n"
            f"Signal: <b>{signal}</b>\n"
            f"Timeframe: <b>{timeframe}</b>\n"
            f"Price: <b>{price}</b>"
        )
