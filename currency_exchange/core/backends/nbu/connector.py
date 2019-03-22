"""
doc string goes here
"""

__all__ = ['Connector']

# Standard library imports.
import requests

# Related third party imports.

# Local application/library specific imports.
from currency_exchange.core.exceptions import BackendConnectionError, BackendReadTimeoutError, BackendReadError, BackendParseError
from .methods import BaseMethod


class Connector:
    access_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/'

    def execute(self, method):
        assert isinstance(method, BaseMethod)

        url_path = '{base_url}{method_name}?{params}'
        params = method.build_request()
        params_str = '&'.join(['{}={}'.format(k, v) for k, v in params.items()])

        url_path = url_path.format(
            base_url=self.access_url,
            method_name=method.api_method_name,
            params=params_str
        )

        try:
            response = requests.get(url_path)
        except requests.ConnectionError:
            raise BackendConnectionError
        except requests.ReadTimeout:
            raise BackendReadTimeoutError

        if response.status_code == 200:
            try:
                result = method.parse_response(response.text)
            except Exception as e:
                raise BackendParseError(str(e))
        else:
            raise BackendReadError('Response status code was: {}'.format(response.status_code))

        return result
