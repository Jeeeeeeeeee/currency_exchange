"""
doc string goes here
"""

__all__ = ['CurrencyService']

# Standard library imports.
import datetime as dt

# Related third party imports.

# Local application/library specific imports.
from currency_exchange.core.storage import DummyStorage
from currency_exchange.core.cache import DummyCacheBackend

from .backends import registry
from .exceptions import BackendException, BackendUnhandledException


class CurrencyService:
    convert_to_cache_expire = 100

    def __init__(self, storage=None, cache_backend=None):
        self.storage = storage or DummyStorage()
        self.cache_backend = cache_backend or DummyCacheBackend()

    def download_data(self, on_date=None):
        result = []
        errors = {}
        backends = registry.backends
        on_date = on_date or dt.date.today()

        for name, cls in backends.items():
            try:
                backend = cls()
                rates = backend.download_data(on_date)
                result.extend(rates)
            except BackendException as e:
                errors[name] = {'error': str(e), 'type': type(e).__name__}
            except Exception as e:
                e = BackendUnhandledException(str(e))
                errors[name] = {'error': str(e), 'type': type(e).__name__}

        self.storage.store_rates(result)

        return result

    def get_currency_rates(self, provider_names, currency_code, to_currencies=None, on_date=None):
        on_date = on_date or dt.date.today()
        result = self.storage.get_rates(provider_names, currency_code, to_currencies, on_date)

        return result

    @staticmethod
    def _build_cache_key(provider_names, amount, currency_code, to_currencies=None, on_date=None):
        result = 'provider={}amount={}from={}to={}on_date={}'.format(
            '|'.join(provider_names),
            str(amount),
            currency_code,
            '|'.join(to_currencies or []),
            str(on_date or '')
        )
        result = result.strip()
        return result

    def convert(self, provider_names, amount, currency_code, to_currencies=None, on_date=None):
        on_date = on_date or dt.date.today()

        cache_key = self._build_cache_key(provider_names, amount, currency_code, to_currencies, on_date)
        result = self.cache_backend.get(cache_key, [])
        if result:
            return result

        rates_data = self.get_currency_rates(provider_names, currency_code, to_currencies, on_date)

        for rate in rates_data:
            exchange_rate = rate.get_rate()
            converted_amount = amount * exchange_rate
            result.append({
                'provider': rate.get_provider(),
                'from': rate.get_from_currency(),
                'to': rate.get_to_currency(),
                'rate': exchange_rate,
                'amount': converted_amount
            })

        self.cache_backend.set(cache_key, result, timeout=self.convert_to_cache_expire)

        return result
