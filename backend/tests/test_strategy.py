from app.infrastructure.data_provider.mt5_provider import MT5Provider
from app.infrastructure.config.config_loader import ConfigLoader
from app.domain.models.models import MarketData
from app.domain.services.strategy_engine import StrategyEngine

provider = MT5Provider()
engine = StrategyEngine()
configuration = ConfigLoader()
config = configuration.load()

for configuration in config.configurations:
    symbols = configuration.symbols

    for symbol in symbols:
        data = MarketData(
            trend = provider.get_data(symbol, configuration.timeframes.trend),
            entry = provider.get_data(symbol, configuration.timeframes.entry, 50)
        )
        for strategy in configuration.strategies:
            signal, logs = engine.run(strategy, data)
            break
        break
    break

print(signal, logs)
