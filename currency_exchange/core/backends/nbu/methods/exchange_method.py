"""
doc string goes here
"""

__all__ = ['JsonExchangeMethod']

# Standard library imports.
import json
import copy
import decimal

# Related third party imports.

# Local application/library specific imports.
from currency_exchange.core.entities import CurrencyEntity, CurrencyExchangeRate
from .base import BaseMethod


class BaseExchangeMethod(BaseMethod):
    api_method_name = 'exchange'
    format = None

    def __init__(self, on_date, provider_name):
        self.on_date = on_date
        self.provider_name = provider_name
        self.to_currency = CurrencyEntity('Українська гривня', 'UAH')

    def build_request(self):
        result = {
            'date': self.on_date.strftime('%Y%m%d')
        }

        if self.format is not None:
            result[self.format] = ''

        return result

    def parse_response(self, response):
        raise NotImplementedError


class JsonExchangeMethod(BaseExchangeMethod):
    format = 'json'

    def parse_response(self, response):
        response = json.loads(response)
        result = []

        for val in response:
            from_currency = CurrencyEntity(val['txt'], val['cc'])
            rate = decimal.Decimal(val['rate'])
            record = CurrencyExchangeRate(self.provider_name, from_currency, self.to_currency, rate, self.on_date)
            result.append(record)

        return result
