import decimal
import datetime
import logging
import os

from currency_exchange.core.backends import registry, NBUBackend
from currency_exchange.core.service import CurrencyService
from currency_exchange.core.storage import SQLiteStorage, PostgreSQLStorage
from currency_exchange.core.cache import MemcachedBackend, RedisBackend

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger('currency_exchange.tester')

logger.info('Register backends')
registry.register(NBUBackend.__name__, NBUBackend)


# CACHE CONFIGURATION
logger.info('Configure cache connection')
# cache_backend = MemcachedBackend(host='127.0.0.1', port=11211)
cache_backend = RedisBackend(host='127.0.0.1', port=6379)


# DB CONFIGURATION
def configure_sql_lite(db_path):
    logger.info('Configure SQLiteStorage connection')
    sql_lite_dir = os.path.dirname(db_path)

    if not os.path.exists(sql_lite_dir):
        logger.error('Invalid path for SQLite')
        exit(0)

    if os.path.exists(db_path):
        logger.info('Remove SQL DB')
        os.remove(db_path)

    logger.info('Init SQLite Storage')
    result = SQLiteStorage(db_path)
    return result


def configure_postgresql():
    logger.info('Configure SQLiteStorage connection')
    result = PostgreSQLStorage(dbname='edu_db', user='edu_user', password='edu_pass', host='127.0.0.1', port=5432)

    try:
        result.drop_tables()
    except Exception as e:
        logger.warning('Drop tables on init connection failed: {}'.format(e))

    return result


# db_full_path = '/home/otegelman/PROJECTS/itea/py4a/projects/currency_exchange/var/db/db.sqlite3'
# storage = configure_sql_lite(db_full_path)

storage = configure_postgresql()

logger.info('Run DB migration')
storage.migrate()

logger.info('Init CurrencyService')
service = CurrencyService(storage, cache_backend)


def download_data(days_before_today=1):
    now = datetime.date.today()

    for days_delta in range(0, days_before_today):
        date_elem = now - datetime.timedelta(days=days_delta)

        logger.info('Download data per {}'.format(date_elem))
        try:
            service.download_data(date_elem)
        except Exception as e:
            logger.exception('Failed download data per {}. Reason: {}'.format(date_elem, str(e)))


days_past_count = 3
logger.info('Download data for past {} days'.format(days_past_count))
download_data(days_past_count)


def test_convert(backends, amount, from_currency_code, to_currencies_codes):
    logger.info('START CONVERT')

    convert_to = service.convert(backends, amount, from_currency_code, to_currencies_codes)

    context = decimal.getcontext()
    context.prec = 10

    for rec in convert_to:
        record_str = '{provider}\t{from_curr}\t{to_curr}\t{rate}\t{amount}'.format(
            provider=rec['provider'],
            from_curr=rec['from'].get_code(),
            to_curr=rec['to'].get_code(),
            rate=rec['rate'] * decimal.Decimal(1),
            amount=rec['amount'] * decimal.Decimal(1)
        )
        logger.info('\t' + record_str)

    logger.info('END CONVERT')


convert_args = (['NBU'], 100, 'UAH', ['USD', 'EUR', 'RUB'])
test_convert(*convert_args)

try:
    storage.drop_tables()
except Exception as e:
    logger.warning('Drop tables on end failed: {}'.format(e))

