import json
import requests
from config import keys


class ConvertExeption(Exception):  # класс исключений
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:  # проверка введенных значений на равенство
            raise ConvertExeption(f'Введены одинаковые валюты {base}')  # поднимаем исключение ConvertExeption
        quote_ticker, base_ticker = keys[quote], keys[base]
        try:
            quote_ticker = keys[quote]  # сверка со словарём валют
        except KeyError:
            raise ConvertExeption(f'Невозможно обработать введенную валюту {quote}')
        try:
            quote_ticker = keys[quote]  # сверка со словарём валют
        except KeyError:
            raise ConvertExeption(f'Невозможно обработать введенную валюту {base}')
        try:
            amount = float(amount)  # проверка, что введено корректное значение
        except ValueError:
            raise ConvertExeption(f'Невозможно обработать введенную величину {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * float(amount)
        return total_base

