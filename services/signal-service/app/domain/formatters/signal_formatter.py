class SignalFormatter:
    @staticmethod
    def format_price(price: float) -> str:
        formatted = f"{price:.4f}"
        cleaned = formatted.rstrip('0')
        decimal_part = cleaned.split('.')[1] if '.' in cleaned else ''
        
        if len(decimal_part) < 2:
            return f"{price:.2f}"
            
        return cleaned

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
        formatted_price = SignalFormatter.format_price(price)

        return (
            f"Symbol: <b>{symbol}</b>\n"
            f"Strategy: <b>{strategy}</b>\n"
            f"Signal: <b>{signal}</b>\n"
            f"Timeframes: <b>{f'{context_timeframe} - ' if context_timeframe else ''}{trend_timeframe} - {entry_timeframe}</b>\n"
            f"Price: <b>{formatted_price}</b>"
        )
