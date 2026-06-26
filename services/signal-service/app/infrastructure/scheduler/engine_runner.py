from threading import Thread
from app.infrastructure.scheduler.signal_engine import SignalEngine

def start_engine():
    engine = SignalEngine()
    thread = Thread(
        target=engine.run,
        daemon=True,
        name="signal-engine",
    )
    thread.start()
