from enum import Enum

class SignalType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    NONE = "NONE"

class Timeframe(str, Enum):
    M1 = "M1"
    M3 = "M3"
    M5 = "M5"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
