import requests

class TelegramAdapter():
    def send(
        self,
        token: str,
        chat_id: str,
        message: str,
    ):
        try:
            response = requests.post(
                (f"https://api.telegram.org/bot{token}/sendMessage"),
                json={
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                },
                timeout=10,
            )
            response.raise_for_status()

            return True
        
        except Exception as e:
            raise RuntimeError(f"Telegram Notifier error: {str(e)}")
