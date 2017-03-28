WallApp
=======

WallApp is like facebook except it has only one wall

Developed in a TDD fashion

NOTE: all emails appear in terminal for the time being.

Documentation is available on /api/v1/docs/

The system is currently represented as a swagger documentation with No frontend that consumes the backend.

But the Swagger docs has a very good explaination for each endpoint and you can use the docs to try everything out.

:License: MIT


Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test
