"""
doc string goes here
"""

__all__ = ['SQLiteStorage']

# Standard library imports.
import sqlite3
import itertools
import decimal
import datetime

# Related third party imports.

# Local application/library specific imports.
from currency_exchange.core.storage.base import BaseStorage
from currency_exchange.core.entities import CurrencyExchangeRate, CurrencyEntity
from .migration import MIGRATION_SCRIPT


class SQLiteStorage(BaseStorage):
    _connection = None

    def __init__(self, connection_string, connection_defaults=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.connection_string = connection_string
        self.connection_defaults = connection_defaults or {}

    @property
    def connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self.connection_string,
                                               **self.connection_defaults)
        return self._connection

    def store_currencies(self, currencies):
        assert all([isinstance(obj, CurrencyEntity) for obj in currencies])

        conn = self.connection
        cursor = conn.cursor()

        currency_codes = [c.get_code() for c in currencies]
        in_db_codes = [c.get_code() for c in self.get_currencies(None, currency_codes)]

        diff = set(currency_codes).difference(set(in_db_codes))
        new_currencies = filter(lambda c: c.get_code() in diff, currencies)
        new_currencies = map(lambda c: (c.get_code(), c.get_name()), new_currencies)

        insert_sql = 'insert into currency (code, name) values (?, ?)'
        cursor.executemany(insert_sql, new_currencies)
        conn.commit()

    def _store_new_providers(self, providers):
        conn = self.connection
        cursor = conn.cursor()

        read_sql = 'select code from provider where code in ({})'.\
            format(', '.join('?' * len(providers)))
        cursor.execute(read_sql, providers)
        in_db_providers = cursor.fetchall()
        in_db_providers = [p[0] for p in in_db_providers]

        diff = set(providers).difference(set(in_db_providers))
        new_providers = filter(lambda p: p in diff, set(providers))
        new_providers = map(lambda p: (p, p), new_providers)

        if new_providers:
            insert_sql = 'insert into provider (code, name) values (?, ?)'
            cursor.executemany(insert_sql, new_providers)
            conn.commit()

    def store_rates(self, exchange_rates):
        assert all([isinstance(obj, CurrencyExchangeRate) for obj in exchange_rates])
        conn = self.connection
        cursor = conn.cursor()

        providers = [r.get_provider() for r in exchange_rates]
        self._store_new_providers(providers)

        insert_sql = 'insert into currency_exchange_rate (from_currency_id, to_currency_id, on_date, provider_id, rate) values (?, ?, ?, ?, ?)'
        data = map(lambda r: (r.get_from_currency().get_code(), r.get_to_currency().get_code(),
                              r.get_on_date(), r.get_provider(), float(r.get_rate())), exchange_rates)

        cursor.executemany(insert_sql, data)
        conn.commit()

    def get_currencies(self, provider_names, currency_codes):
        result = []
        conn = self.connection
        cursor = conn.cursor()

        read_sql = 'select code, name from currency where code in ({})'.format(', '.join('?' * len(currency_codes)))

        cursor.execute(read_sql, currency_codes)
        data = cursor.fetchall()

        for val in data:
            currency = CurrencyEntity(val[0], val[1])
            result.append(currency)

        retrieved_codes = [c.get_code() for c in result]
        diff = set(currency_codes).difference(set(retrieved_codes))

        for val in diff:
            result.append(CurrencyEntity(val, val))

        return result

    def get_rates(self, provider_names, currency_code, to_currencies=None, on_date=None):
        conn = self.connection
        cursor = conn.cursor()

        currecies = self.get_currencies(None, [currency_code] + (to_currencies or None))
        currecies = {c.get_code(): c for c in currecies}

        def map_query_data(record):
            mapped = record[0] + (record[1], )
            return mapped

        filter_sql = 'provider_id=? and from_currency_id=?'

        query_data = itertools.product(provider_names, [currency_code])
        if to_currencies:
            query_data = itertools.product(query_data, to_currencies)
            query_data = map(map_query_data, query_data)
            filter_sql += ' and to_currency_id=?'

        if on_date:
            query_data = itertools.product(query_data, [on_date])
            query_data = map(map_query_data, query_data)
            filter_sql += ' and on_date=?'

        query_data = list(query_data)

        filter_sql = '({}) or '.format(filter_sql) * len(query_data)
        filter_sql = filter_sql[:-4]
        query_sql = 'select provider_id, from_currency_id, to_currency_id, rate, on_date ' \
                    'from currency_exchange_rate where {}'.format(filter_sql)

        q_data = []
        for qd in query_data:
            q_data.extend(list(qd))

        cursor.execute(query_sql, q_data)
        data = cursor.fetchall()

        result = list()
        for rec in data:
            tmp = CurrencyExchangeRate(
                rec[0],
                currecies.get(rec[1]),
                currecies.get(rec[2]),
                decimal.Decimal(rec[3]),
                datetime.datetime.strptime(rec[4], '%Y-%m-%d')
            )
            result.append(tmp)

        return result

    def migrate(self):
        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.executescript(MIGRATION_SCRIPT)
            return True, None
        except Exception as e:
            return False, str(e)

    def drop_tables(self):
        conn = self.connection
        cursor = conn.cursor()

        for table in self.DB_TABLES:
            cursor.execute('drop table {};'.format(table))
