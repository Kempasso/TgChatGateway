import requests
from src.core.settings import telegram_bot_key


class TelegramApiProvider:

    def __init__(self):
        self.telegram_bot_key = telegram_bot_key
        self.telegram_api_url = f'https://api.telegram.org/bot{self.telegram_bot_key}/'

    async def send_message(self, chat_id, text):
        action = 'sendMessage'
        url = f'{self.telegram_api_url}{action}'
        data = {'chat_id': chat_id, 'text': text}
        requests.post(url, data=data)
