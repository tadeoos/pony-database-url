from pony_database_url import __version__
from pony_database_url.parser import parse


def test_version():
    assert __version__ == '0.1.0'


def test_sqlite_url__good():
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


def test_sqlite_url__bad():
    assert parse('sqlite://USER:PASSWORD@HOST:5276/sth') == {
        'provider': 'sqlite',
        'filename': 'sth',
        'create_db': True
    }

    assert parse('sqlite://sometext:wih:@wierda') == {
        'provider': 'sqlite',
        'filename': ':memory:',
        'create_db': True
    }


def test_postgres_url():
    assert parse('postgres://USER:PASSWORD@HOST:5276/NAME') == {
        'provider': 'postgres', 'user': 'USER', 'password': 'PASSWORD', 'host': 'host', 'port': 5276, 'database': 'NAME'
    }
    assert parse('postgres://:@HOST:5276/NAME') == {
        'provider': 'postgres', 'user': '', 'password': '', 'host': 'host', 'port': 5276, 'database': 'NAME'
    }
    assert parse('postgres://:@HOST:/NAME') == {
        'provider': 'postgres', 'user': '', 'password': '', 'host': 'host', 'port': '', 'database': 'NAME'
    }
    assert parse('postgres://:@HOST:/') == {
        'provider': 'postgres', 'user': '', 'password': '', 'host': 'host', 'port': '', 'database': ''
    }


def test_mysql_url():
    assert parse('mysql://USER:PASSWORD@HOST:5276/NAME') == {
        'provider': 'mysql', 'user': 'USER', 'passwd': 'PASSWORD', 'host': 'host', 'port': 5276, 'db': 'NAME'
    }


def test_oracle_url():
    assert parse('oracle://USER:PASSWORD@:/SOME_DSN') == {
        'provider': 'oracle', 'user': 'USER', 'password': 'PASSWORD', 'dsn': 'SOME_DSN'
    }
    assert parse('oracle://USER:PASSWORD@/SOME_DSN') == {
        'provider': 'oracle', 'user': 'USER', 'password': 'PASSWORD', 'dsn': 'SOME_DSN'
    }
