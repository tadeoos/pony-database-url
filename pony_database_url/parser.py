# -*- coding: utf-8 -*-

import os

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


# Register database schemes in URLs.
urlparse.uses_netloc.append('postgres')
urlparse.uses_netloc.append('postgresql')
urlparse.uses_netloc.append('pgsql')
urlparse.uses_netloc.append('mysql')
urlparse.uses_netloc.append('sqlite')
urlparse.uses_netloc.append('oracle')

DEFAULT_ENV = 'DATABASE_URL'


def get_bind_kwargs(env=DEFAULT_ENV, default=None):
    """Returns configured DATABASE dictionary from DATABASE_URL."""

    config = {}

    s = os.environ.get(env, default)

    if s:
        config = parse(s)

    return config


def argument_name(arg, provider):
    if arg == 'db':
        return arg if provider == 'mysql' else 'database'
    if arg == 'passwd':
        return arg if provider == 'mysql' else 'password'


def parse(url):
    """Parses a database URL."""

    if url == 'sqlite://:memory:':
        # this is a special case, because if we pass this URL into
        # urlparse, urlparse will choke trying to interpret "memory"
        # as a port number
        return {
            'provider': 'sqlite',
            'filename': ':memory:'
        }
        # note: no other settings are required for sqlite

    # otherwise parse the url as normal
    config = {}

    url = urlparse.urlparse(url)

    # Split query strings from path.
    path = url.path[1:]
    if '?' in path and not url.query:
        path, query = path.split('?', 2)
    else:
        path, query = path, url.query
    query = urlparse.parse_qs(query)

    # If we are using sqlite and we have no path, then assume we
    # want an in-memory database (this is the behaviour of sqlalchemy)
    if url.scheme == 'sqlite' and path == '':
        path = ':memory:'

    # Handle postgres percent-encoded paths.
    hostname = url.hostname or ''
    if '%2f' in hostname.lower():
        # Switch to url.netloc to avoid lower cased paths
        hostname = url.netloc
        if "@" in hostname:
            hostname = hostname.rsplit("@", 1)[1]
        if ":" in hostname:
            hostname = hostname.split(":", 1)[0]
        hostname = hostname.replace('%2f', '/').replace('%2F', '/')

    port = url.port
    provider = url.scheme

    if provider == 'sqlite':
        return {
            'filename': path,
            'provider': provider,
            'create_db': True
        }
    if provider == 'oracle':
        return {
            'provider': provider,
            'password': urlparse.unquote(url.password or ''),
            'user': urlparse.unquote(url.username or ''),
            'dsn': urlparse.unquote(path or ''),
        }

    return {
        'provider': provider,
        argument_name('db', provider): urlparse.unquote(path or ''),
        argument_name('passwd', provider): urlparse.unquote(url.password or ''),
        'user': urlparse.unquote(url.username or ''),
        'host': hostname,
        'port': port or '',
    }
