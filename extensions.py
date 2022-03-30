import requests
import json
from config import keys

class ConvertionExeption(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionExeption(f"Не возможно конвертировать {quote} в {quote}!")

        try:
            ticker_quote = keys[quote]
        except KeyError:
            raise ConvertionExeption(f"Не удалось обработать {quote}")

        try:
            ticker_base = keys[base]
        except KeyError:
            raise ConvertionExeption(f"Не удалось обработать {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f"Не удалось обработать {amount}")

        r = requests.get(
            f'http://api.exchangeratesapi.io/v1/latest?access_key=664ceeeaba5dc1706c92cea4ed2598cc&symbols={ticker_base},{ticker_quote}')
        base_eur = json.loads(r.content)["rates"][keys[base]]
        quote_eur = json.loads(r.content)["rates"][keys[quote]]
        result = round(amount * base_eur / quote_eur, 3)
        return result
