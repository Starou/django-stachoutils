from django.db import models

# http://djangosnippets.org/snippets/2100/
# https://code.djangoproject.com/ticket/11305

class SQLCountCase(models.sql.aggregates.Aggregate):
    is_ordinal = True
    sql_function = 'COUNT'
    sql_template = "%(function)s(CASE %(case)s WHEN %(when)s THEN 1 ELSE null END)"

    def __init__(self, col, **extra):
        if isinstance(extra['when'], basestring):
            quote = extra.get('quote', "'")
            extra['when'] = "(%s%s%s)" % (quote, extra['when'], quote)

        if not extra.get('case', None) and not extra.has_key('case'):
            extra['case'] = '"%s"."%s"'%(extra['source'].model._meta.db_table, extra['source'].name)

        if extra['when'] is None:
            extra['when'] = True
            extra['case'] += ' IS NULL '

        super(SQLCountCase, self).__init__(col, **extra)

class CountCase(models.Aggregate):
    name = 'COUNT'

    def add_to_query(self, query, alias, col, source, is_summary):
        aggregate = SQLCountCase(col, source=source, is_summary=is_summary, **self.extra)
        query.aggregates[alias] = aggregate


class SQLSumExtra(models.sql.aggregates.Aggregate):
    is_ordinal = False
    sql_function = 'SUM'
    sql_template = "%(function)s(%(sum)s)"

    def __init__(self, col, **extra):
        super(SQLSumExtra, self).__init__(col, **extra)

class SumExtra(models.Aggregate):
    name = 'SUM'

    def add_to_query(self, query, alias, col, source, is_summary):
        aggregate = SQLSumExtra(col, source=source, is_summary=is_summary, **self.extra)
        query.aggregates[alias] = aggregate

#http://djangosnippets.org/snippets/2099/
class SQLSumCase(models.sql.aggregates.Aggregate):
    is_ordinal = True
    sql_function = 'SUM'
    sql_template = "%(function)s(CASE %(case)s WHEN %(when)s THEN %(field)s ELSE 0 END)"

    def __init__(self, col, **extra):
        if isinstance(extra['when'], basestring):
            extra['when'] = "'%s'"%extra['when']

        if not extra.get('case', None):
            extra['case'] = '"%s"."%s"'%(extra['source'].model._meta.db_table, extra['source'].name)
        # FIXME: gerer les relation via double underscore. 
        else:
            extra['case'] = '"%s"."%s"'%(extra['source'].model._meta.db_table, extra['case'])

        if extra['when'] is None:
            extra['when'] = True
            extra['case'] += ' IS NULL '

        super(SQLSumCase, self).__init__(col, **extra)

class SumCase(models.Aggregate): # TODO
    name = 'SUM'

    def add_to_query(self, query, alias, col, source, is_summary):
        aggregate = SQLSumCase(col, source=source, is_summary=is_summary, **self.extra)
        query.aggregates[alias] = aggregate