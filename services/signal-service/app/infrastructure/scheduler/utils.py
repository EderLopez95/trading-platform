from datetime import datetime
from app.infrastructure.scheduler.timeframe import TIMEFRAME_MINUTES

def should_execute(configuration, now: datetime):
    minutes = TIMEFRAME_MINUTES[configuration.entry_timeframe]
    total_minutes = (now.hour * 60 + now.minute)

    return total_minutes % minutes == 0

def get_candle_key(configuration, now: datetime):
    timeframe_minutes = TIMEFRAME_MINUTES[configuration.entry_timeframe]
    total_minutes = (now.hour * 60 + now.minute)
    bucket = total_minutes // timeframe_minutes

    return (
        f"{configuration.id}:"
        f"{now.year}:"
        f"{now.month}:"
        f"{now.day}:"
        f"{bucket}"
    )
