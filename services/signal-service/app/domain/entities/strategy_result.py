from dataclasses import dataclass
from app.domain.enums.enums import SignalType

@dataclass
class StrategyResult:
    signal: SignalType
    reason: str | None = None
