import datetime
import copy


class EventStatus:
    STATUS_OK = 'OK'
    STATUS_FAILED = 'FAILED'


class EventsLogger:
    def __init__(self):
        self.events = []

    def log_event(self, checker_name, status, name, exception_text=None):
        event = [datetime.datetime.now(), checker_name, status, name, exception_text or '--']
        self.events.append(event)

    def print(self):
        for event in self.events:
            event_str = '{}\t{}\t{}\t{}\t{}'.format(*event)
            print(event_str)


class BaseConfigChecker:
    check_functions = None
    checker_name = None

    def __init__(self, logger):
        assert isinstance(logger, EventsLogger)
        assert isinstance(self.check_functions, tuple)
        self.logger = logger

    def run_check(self):
        for check_name, check_func, break_on_exception in self.check_functions:
            try:
                check_func()
                self.logger.log_event(self.checker_name, EventStatus.STATUS_OK, check_name)
            except Exception as e:
                self.logger.log_event(self.checker_name, EventStatus.STATUS_FAILED, check_name, str(e))
                if break_on_exception:
                    break


class MemcachedChecker(BaseConfigChecker):
    checker_name = 'MEMCACHED'

    def check_import():
        import pymemcache

    def check_connection():
        from pymemcache.client import base
        conn = base.Client(('127.0.0.1', 11211))

    def check_read_write():
        from pymemcache.client import base
        conn = base.Client(('127.0.0.1', 11211))

        test_key = 'test_key'
        test_value = 'test_value'
        conn.set(test_key, test_value, expire=10)
        value = conn.get(test_key, None)

        if value.decode() != test_value:
            raise Exception('Read/Write Failed')

    check_functions = (
        ('Import module', check_import, True),
        ('Connection', check_connection,  True),
        ('Read/Write', check_read_write, True)
    )


class RedisChecker(BaseConfigChecker):
    checker_name = 'REDIS'

    def check_import():
        import redis

    def check_connection():
        from redis import Redis
        conn = Redis(host='127.0.0.1', port=6379)

    def check_read_write():
        from redis import Redis
        conn = Redis(host='127.0.0.1', port=6379)

        test_key = 'test_key'
        test_value = 'test_value'
        conn.set(test_key, test_value, ex=10)
        value = conn.get(test_key)

        if value.decode() != test_value:
            raise Exception('Read/Write Failed')

    check_functions = (
        ('Import module', check_import, True),
        ('Connection', check_connection,  True),
        ('Read/Write', check_read_write, True)
    )


class PostgreSQLChecker(BaseConfigChecker):
    checker_name = 'POSTGRESQL'

    def check_import():
        import psycopg2

    def check_connection():
        import psycopg2
        conn = psycopg2.connect(dbname='edu_db', user='edu_user', password='edu_pass', host='127.0.0.1', port=5432)

    def check_read_write():
        import psycopg2
        conn = psycopg2.connect(dbname='edu_db', user='edu_user', password='edu_pass', host='127.0.0.1', port=5432)
        cursor = conn.cursor()

        cursor.execute('CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);')

        test_data = (1, 'test')
        cursor.execute('INSERT INTO test (num, data) VALUES (%s, %s)', test_data)
        cursor.execute('SELECT * FROM test;')
        result = cursor.fetchone()

        if test_data != tuple(result[1:]):
            raise Exception('Read/Write Failed')

        cursor.execute('DROP TABLE test;')

    check_functions = (
        ('Import module', check_import, True),
        ('Connection', check_connection,  True),
        ('Read/Write', check_read_write, True)
    )


class PyMongoChecker(BaseConfigChecker):
    checker_name = 'PY_MONGO'

    def check_import():
        import pymongo

    def check_connection():
        from pymongo import MongoClient
        conn = MongoClient(host='127.0.0.1', port=27017, username='edu_user', password='edu_password')

    def check_read_write():
        from pymongo import MongoClient
        conn = MongoClient(host='127.0.0.1', port=27017, username='edu_user', password='edu_password')
        db = conn.test_db
        collection = db.test_collection

        test_data = {
            'identity': 1,
            'value': 'test_value'
        }

        inserted_id = collection.insert_one(copy.deepcopy(test_data)).inserted_id
        result = collection.find_one()

        for key, val in test_data.items():
            res_data = result.get(key)
            if res_data != val:
                raise Exception('Read/Write Failed')

        conn.drop_database('test_db')

    check_functions = (
        ('Import module', check_import, True),
        ('Connection', check_connection,  True),
        ('Read/Write', check_read_write, True)
    )


class MongoEngineChecker(BaseConfigChecker):
    checker_name = 'MONGO_ENGINE'

    def check_import():
        import mongoengine

    def check_connection():
        from mongoengine import connect

        _connection_params = {
            'db': 'test_db',
            'host': '127.0.0.1',
            'port': 27017,
            'username': 'edu_user',
            'password': 'edu_password',
            'tz_aware': True
        }

        connect(**_connection_params)

    def check_read_write():
        def create_drop_db(is_create=True):
            from pymongo import MongoClient
            conn = MongoClient(host='127.0.0.1', port=27017, username='edu_user', password='edu_password')

            if is_create:
                conn.test_db.add_user('edu_user', 'edu_password', roles=[{'role': 'readWrite', 'db': 'test_db'}])
            else:
                conn.drop_database('test_db')

        create_drop_db()

        from mongoengine import connect, Document, IntField, StringField
        _connection_params = {
            'db': 'test_db',
            'host': '127.0.0.1',
            'port': 27017,
            'username': 'edu_user',
            'password': 'edu_password'
        }

        connect(**_connection_params)

        class TestDocument(Document):
            identity = IntField()
            value = StringField()

        doc = TestDocument(1, 'test_value')
        doc.save()

        doc = TestDocument.objects.all()[0]

        if doc.identity != 1 or doc.value != 'test_value':
            raise Exception('Read/Write Failed')

        create_drop_db(is_create=False)

    check_functions = (
        ('Import module', check_import, True),
        ('Connection', check_connection,  True),
        ('Read/Write', check_read_write, True)
    )


if __name__ == '__main__':
    logger = EventsLogger()
    config_checkers = [
        MemcachedChecker(logger),
        RedisChecker(logger),
        PostgreSQLChecker(logger),
        PyMongoChecker(logger),
        MongoEngineChecker(logger),
    ]

    for checker in config_checkers:
        checker.run_check()

    logger.print()
