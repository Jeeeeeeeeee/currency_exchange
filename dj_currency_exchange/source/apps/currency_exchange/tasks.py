"""
doc string goes here
"""

__all__ = ['provider_load_data_task']

# Standard library imports.
from datetime import datetime

# Related third party imports.
from django.conf import settings
from django.db import connections

# Local application/library specific imports.
from currency_exchange.core.backends import registry, NBUBackend
from currency_exchange.core.service import CurrencyService
from currency_exchange.core.storage import SQLiteStorage, PostgreSQLStorage

registry.register(NBUBackend.__name__, NBUBackend)


# SQLite Connection
# SQLITE_FILE_PATH = settings.DATABASES['default']['NAME']
# db_conn = connections['default']
# storage = SQLiteStorage(SQLITE_FILE_PATH)
# storage._connection = db_conn

db = settings.DATABASES['default']

storage = PostgreSQLStorage(
    dbname=db['NAME'],
    user=db['USER'],
    password=db['PASSWORD'],
    host=db['HOST'],
    port=db['PORT']
)

service = CurrencyService(storage)


def provider_load_data_task(provider_code, on_date=None):
    on_date = on_date or datetime.today()
    service.download_data(on_date)
