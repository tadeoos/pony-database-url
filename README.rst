Pony-Database-URL
~~~~~~~~~~~~~~~~~

    This is a port of `DJ-Database-URL <https://github.com/kennethreitz/dj-database-url>`_  library for `PonyORM <https://ponyorm.org/>`_

This simple utility allows you to utilize the
`12factor <http://www.12factor.net/backing-services>`_ inspired
``DATABASE_URL`` environment variable to configure your Pony database.

The ``pony_database_url.get_bind_kwargs`` method returns a PonyORM ``db.bind`` kwargs
dictionary, populated with all the data specified in your URL.

If you'd rather not use an environment variable, you can pass a URL in directly
instead to ``pony_database_url.get_bind_kwargs``.


Supported Databases
-------------------

Support currently exists for PostgreSQL, MySQL, Oracle and SQLite.

Installation
------------

Installation is simple::

    $ pip install pony-database-url

Usage
-----

::

    from pony.orm import Database
    from pony_database_url import get_bind_kwargs

    db = Database()

    # configure from `DATABASE_URL` environment variable:
    db.bind(**get_bind_kwargs())

    # or with a default:
    db.bind(**get_bind_kwargs(default='postgres://...'))

    # or give the URL explicitly:
    db.bind(**get_bind_kwargs('postgres://...'))


URL schema
----------

+-------------+--------------------------------------------------+
| Engine      | URL                                              |
+=============+==================================================+
| PostgreSQL  | ``postgres://USER:PASSWORD@HOST:PORT/NAME`` [1]_ |
+-------------+--------------------------------------------------+
| MySQL       | ``mysql://USER:PASSWORD@HOST:PORT/NAME``         |
+-------------+--------------------------------------------------+
| SQLite      | ``sqlite:///PATH`` [2]_                          |
+-------------+--------------------------------------------------+
| Oracle      | ``oracle://USER:PASSWORD@/DSN`` [3]_             |
+-------------+--------------------------------------------------+

.. [1] With PostgreSQL, you can also use unix domain socket paths with
       `percent encoding <http://www.postgresql.org/docs/9.2/interactive/libpq-connect.html#AEN38162>`_:
       ``postgres://%2Fvar%2Flib%2Fpostgresql/dbname``.
.. [2] SQLite connects to file based databases. The same URL format is used, omitting
       the hostname, and using the "file" portion as the filename of the database.
       This has the effect of four slashes being present for an absolute file path:
       ``sqlite:////full/path/to/your/database/file.sqlite``.
.. [3] Note that when connecting to Oracle the URL isn't in the form you may know
       from using other Oracle tools (like SQLPlus) i.e. user and password are separated
       by ``:`` not by ``/``. Also you can omit ``HOST`` and ``PORT``
       and provide a full DSN string or TNS name in ``NAME`` part.
