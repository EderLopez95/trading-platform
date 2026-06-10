import MetaTrader5 as mt5
import pandas as pd

mt5.initialize()

symbol = "AAPL.NAS"

rates = mt5.copy_rates_from_pos(
    symbol,
    mt5.TIMEFRAME_M5,
    0,
    50
)

df = pd.DataFrame(rates)

print(df.tail())
