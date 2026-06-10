import requests
from app.infrastructure.config.settings import settings
from app.domain.enums.enums import StrategyNameType, StrategyType

class TelegramNotifier:
    def __init__(self):
        self.token = settings.telegram_token
        self.chat_id = settings.telegram_chat_id

    def send(self, signal, symbol, temporality, strategy, price=0):
        match strategy:
            case StrategyType.RSI_CROSS_TREND:
                strategy_text = StrategyNameType.RSI_CROSS_TREND_value.value
            case StrategyType.MULTI_SMAS_MOMENTUM:
                strategy_text = StrategyNameType.MULTI_SMAS_MOMENTUM_value.value
            case StrategyType.RSI_DIP_ACCUMULATION:
                strategy_text = StrategyNameType.RSI_DIP_ACCUMULATION_value.value
            case _:
                strategy_text = strategy.value

        message = (
            f"Stock: <b>{symbol}</b>\n"
            f"Signal: <b>{signal.value}</b>\n"
            f"Temp: <b>{temporality.value}</b>\n"
            f"Strategy: <b>{strategy_text}</b>\n"
            f"Price: {price:.2f}"
        )

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        try:
            response = requests.post(url, json={
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            })
            # properly handle response status to propagate errors if any
            response.raise_for_status()
        except Exception as e:
            raise RuntimeError(f"Telegram Notifier error: {str(e)}")
