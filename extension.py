import json
import requests
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Не удалось перевести одинаковые валюты - {base}')
        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту - {quote}')
        try:
            base_tiker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту - {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество - {amount}')
        if amount <= 0:
            raise APIException(f'Невозможно конвертировать количество меньше или равно 0')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_tiker}')
        exchange_rate = json.loads(r.content)[base_tiker]
        total_base = float(amount) * float(exchange_rate)

        return round(total_base, 3)
