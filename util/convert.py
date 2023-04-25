import decimal

import requests


def convert(base_url, currency1, currency2, amount_of_currency1):
    url = f'{base_url}/conversion/{currency1}/{currency2}/{amount_of_currency1}'
    result = decimal.Decimal(requests.get(url).text)
    return result
