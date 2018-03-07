======================
Stachou's Django Utils
======================

.. image:: https://coveralls.io/repos/github/Starou/django-stachoutils/badge.svg?branch=master
  :target: https://coveralls.io/github/Starou/django-stachoutils?branch=master

.. image:: https://img.shields.io/pypi/v/django_stachoutils.svg
    :target: https://pypi.python.org/pypi/django-stachoutils/
    :alt: Current version

.. image:: https://img.shields.io/pypi/pyversions/django_stachoutils.svg
    :target: https://pypi.python.org/pypi/django-stachoutils/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/django_stachoutils.svg
    :target: https://pypi.python.org/pypi/django-stachoutils/
    :alt: License

.. image:: https://travis-ci.org/Starou/django-stachoutils.svg
    :target: https://travis-ci.org/Starou/django-stachoutils
    :alt: Travis C.I.


This is mostly some common libs shared between several Django project I am working on.


Install
=======

::

    pip install django-stachoutils

Tests
=====

::

    vagrant up
    vagrant ssh
    cd tests
    make tests

There is a demo project you can run (login: ``super:user``):

::

    cd tests/django_project
    export PYTHONPATH=../../..:${PYTHONPATH}
    python manage.py runserver
