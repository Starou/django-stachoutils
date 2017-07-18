======================
Stachou's Django Utils
======================

This is mostly some common libs shared between several Django project I am working on.


Install
=======


::

    pip install django-stachoutils

Tests
=====

::

    cd tests
    make tests


There is a demo project you can run (login: ``super:user``):

::

    cd tests/django_project
    export PYTHONPATH=../../..:${PYTHONPATH}
    python manage.py runserver
