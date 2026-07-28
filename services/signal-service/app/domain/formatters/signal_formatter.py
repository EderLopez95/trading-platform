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
            f"<b>{symbol}</b>\n"
            f"<b>{strategy}</b>\n"
            f"<b>{signal}</b>\n"
            f"<b>{timeframe}</b>\n"
            f"<b>{price}</b>"
        )
