import queue
import logging
import threading
from app.domain.entities.signal import Signal

logger = logging.getLogger("signal")

class SignalBroadcaster:
    def __init__(self, max_queue_size: int = 100):
        self._lock = threading.Lock()
        self._subscribers: dict[int, tuple[str, "queue.Queue[Signal]"]] = {}
        self._max_queue_size = max_queue_size
        self._next_id = 0

    def subscribe(self, user_id: str) -> tuple[int, "queue.Queue[Signal]"]:
        subscriber_queue: "queue.Queue[Signal]" = queue.Queue(maxsize=self._max_queue_size)

        with self._lock:
            subscriber_id = self._next_id
            self._next_id += 1
            self._subscribers[subscriber_id] = (str(user_id), subscriber_queue)

        return subscriber_id, subscriber_queue

    def unsubscribe(self, subscriber_id: int) -> None:
        with self._lock:
            self._subscribers.pop(subscriber_id, None)

    def publish(self, signal: Signal) -> None:
        signal_user_id = str(signal.user_id)

        with self._lock:
            targets = [
                subscriber_queue
                for user_id, subscriber_queue in self._subscribers.values()
                if user_id == signal_user_id
            ]

        for subscriber_queue in targets:
            try:
                subscriber_queue.put_nowait(signal)
            except queue.Full:
                logger.warning(
                    "signal_stream_dropped",
                    extra={"user_id": signal.user_id, "symbol": signal.symbol},
                )

signal_broadcaster = SignalBroadcaster()
