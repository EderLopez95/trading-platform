from app.domain.strategies.multi_smas_momentum_strategy import MultiSMAsMomentumStrategy
from app.domain.strategies.rsi_cross_trend_strategy import RSICrossTrendStrategy

STRATEGIES = {
    "multi_smas_momentum": MultiSMAsMomentumStrategy(),
    "rsi_cross_trend": RSICrossTrendStrategy(),
}
