# -*- coding: utf-8 -*-

from past.builtins import basestring
from django.db.models import Aggregate, IntegerField

class SumExtra(Aggregate):
    function = 'SUM'
    template = "%(function)s(%(sum_expression)s)"


class SumCase(Aggregate):
    function = 'SUM'
    template = "%(function)s(CASE %(case_expression)s WHEN %(when)s THEN %(expressions)s ELSE 0 END)"

    def __init__(self, expression, **extra):
        if isinstance(extra['when'], basestring):
            extra['when'] = "'%s'" % extra['when']
        if extra['when'] is None:
            extra['when'] = True
        super(SumCase, self).__init__(
            expression,
            output_field=IntegerField(),
            **extra)


class CountCase(Aggregate):
    function = 'Count'
    template = "%(function)s(CASE %(expressions)s WHEN %(when)s THEN 1 ELSE null END)"

    def __init__(self, expression, **extra):
        if isinstance(extra['when'], basestring):
            quote = extra.get('quote', "'")
            extra['when'] = "(%s%s%s)" % (quote, extra['when'], quote)
        # Pas de cas d'utilisation. A vérifier car réécriture pour Django-1.8.
        if extra['when'] is None:
            extra['when'] = True
            extra['case'] += ' IS NULL '
        super(CountCase, self).__init__(
            expression,
            output_field=IntegerField(),
            **extra)


class CountCase2(Aggregate):
    function = 'Count'
    template = "%(function)s(CASE WHEN %(when)s THEN 1 ELSE null END)"

    def __init__(self, expression, **extra):
        if isinstance(extra['when'], basestring):
            quote = extra.get('quote', "'")
            extra['when'] = "(%s%s%s)" % (quote, extra['when'], quote)
        super(CountCase2, self).__init__(
            expression,
            output_field=IntegerField(),
            **extra)
