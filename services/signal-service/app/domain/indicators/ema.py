def calculate_ema_series(
    values: list[float],
    period: int,
) -> list:
    
    if len(values) < period:
        return []
        
    sma = sum(values[:period]) / period
    multiplier = 2 / (period + 1)
    ema_values = [sma]
    ema = sma
    
    for value in values[period:]:
        ema = ((value - ema) * multiplier) + ema
        ema_values.append(ema)
        
    return ema_values
