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
            f"<b>Symbol:</b> {symbol}\n"
            f"<b>Strategy:</b> {strategy}\n"
            f"<b>Signal:</b> {signal}\n"
            f"<b>Timeframe:</b> {timeframe}\n"
            f"<b>Price:</b> {price}"
        )
