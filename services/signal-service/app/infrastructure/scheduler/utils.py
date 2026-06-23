from datetime import datetime
from .timeframe import TIMEFRAME_MINUTES

def should_execute(configuration, now: datetime):
    minutes = TIMEFRAME_MINUTES[configuration.entry_timeframe]

    return (
        now.minute % minutes == 0
    )
