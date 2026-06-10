from enum import Enum

class StrategyType(str, Enum):
    RSI_CROSS_TREND = "rsi_cross_trend"
    MULTI_SMAS_MOMENTUM = "multi_smas_momentum"
    RSI_DIP_ACCUMULATION = "rsi_dip_accumulation"

class StrategyNameType(str, Enum):
    RSI_CROSS_TREND_value = "RSI Cross Trend"
    MULTI_SMAS_MOMENTUM_value = "Multi SMAs Momentum"
    RSI_DIP_ACCUMULATION_value = "RSI Dip Accumulation"

class SignalType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class LogType(str, Enum):
    INFO = "INFO"
    ERROR = "ERROR"

class BotStatus(str, Enum):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"

class Timeframe(str, Enum):
    M5 = "M5"
    M15 = "M15"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
