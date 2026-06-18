import threading
from app.infrastructure.bot.bot_runner import BotRunner
from app.domain.enums.enums import BotStatus
from app.domain.exceptions.exceptions import BotAlreadyRunningError, BotNotRunningError

class BotService:
    def __init__(self):
        self.bot = BotRunner()
        self.thread = None

    def start(self):
        if self.thread and self.thread.is_alive():
            raise BotAlreadyRunningError("Bot is already running")

        self.thread = threading.Thread(
            target=self.bot.start,
            daemon=True
        )
        self.thread.start()
        return BotStatus.RUNNING.value

    def stop(self):
        if not self.thread or not self.thread.is_alive():
            raise BotNotRunningError("Bot is not running")

        self.bot.stop()
        return BotStatus.STOPPED.value

    def status(self):
        if self.thread and self.thread.is_alive():
            return BotStatus.RUNNING.value

        return BotStatus.STOPPED.value
