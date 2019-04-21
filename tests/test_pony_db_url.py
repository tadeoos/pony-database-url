from pony_db_url import __version__
from pony_db_url.parser import parse


"""
PostgreSQL 	postgres://USER:PASSWORD@HOST:PORT/NAME [1]
MySQL 	    mysql://USER:PASSWORD@HOST:PORT/NAME
SQLite 	    sqlite:///PATH [2]
Oracle 	    oracle://USER:PASSWORD@HOST:PORT/NAME [3]
"""


def test_version():
    assert __version__ == '0.1.0'


def test_sqlite_url():
    assert parse('sqlite://:memory:') == {'provider': 'sqlite', 'filename': ':memory:'}

    assert parse('sqlite:////full/path/to/file.sqlite') == {
        'provider': 'sqlite',
        'filename': '/full/path/to/file.sqlite',
        'create_db': True
    }

    assert parse('sqlite:///relative/path/to/file.sqlite') == {
        'provider': 'sqlite',
        'filename': 'relative/path/to/file.sqlite',
        'create_db': True
    }


def test_postgres_url():
    assert parse('postgres://USER:PASSWORD@HOST:5276/NAME') == {
        'provider': 'postgres', 'user': 'USER', 'password': 'PASSWORD', 'host': 'host', 'port': 5276, 'database': 'NAME'
    }


def test_mysql_url():
    assert parse('mysql://USER:PASSWORD@HOST:5276/NAME') == {
        'provider': 'mysql', 'user': 'USER', 'passwd': 'PASSWORD', 'host': 'host', 'port': 5276, 'db': 'NAME'
    }


def test_oracle_url():
    assert parse('oracle://USER:PASSWORD@:/NAME') == {
        'provider': 'oracle', 'user': 'USER', 'password': 'PASSWORD', 'dsn': 'NAME'
    }
