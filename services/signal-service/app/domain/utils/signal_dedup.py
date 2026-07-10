def build_dedup_key(
    symbol: str,
    strategy: str,
    signal: str,
    timeframe: str,
):

    return (
        f"{symbol}:{strategy}:{signal}:{timeframe}"
    )
