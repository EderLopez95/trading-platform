from dataclasses import dataclass

@dataclass
class SchedulerMetrics:
    signals: int = 0
    errors: int = 0
