import time, queue, logging, threading
from app.application.services.notification_service import NotificationService

logger = logging.getLogger("signal")

class NotificationDispatcher:
    def __init__(
        self,
        notification_service: NotificationService,
        max_retries: int = 3,
        backoff_base: int = 2,
    ):
        self._service = notification_service
        self._queue = queue.Queue()
        self._max_retries = max_retries
        self._backoff_base = backoff_base

        threading.Thread(
            target=self._worker,
            daemon=True,
            name="notification-dispatcher",
        ).start()

    def enqueue(self, token: str, chat_id: str, message: str):
        self._queue.put((token, chat_id, message))

    def _worker(self):
        while True:
            token, chat_id, message = self._queue.get()

            try:
                self._deliver(token, chat_id, message)
            finally:
                self._queue.task_done()

    def _deliver(self, token: str, chat_id: str, message: str):
        for attempt in range(1, self._max_retries + 1):
            try:
                self._service.send(
                    token=token,
                    chat_id=chat_id,
                    message=message,
                )

                return

            except Exception as e:
                if attempt == self._max_retries:
                    logger.error(
                        "notification_failed",
                        extra={
                            "attempts": attempt,
                            "error": str(e),
                        }
                    )

                    return

                time.sleep(self._backoff_base ** attempt)
