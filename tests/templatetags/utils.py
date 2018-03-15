from django.template.engine import Engine
from functools import wraps


def set_templates(templates):
    templates = dict((name, '{% load stachoutils %}' + html) for name, html in templates.items())
    loaders = [
        ('django.template.loaders.cached.Loader', [
            ('django.template.loaders.locmem.Loader', templates),
        ]),
    ]
    engine = Engine(
        libraries={
           'stachoutils': 'django_stachoutils.templatetags.stachoutils_extras',
        },
        loaders=loaders,
    )
    def decorator(f):
        @wraps(f)
        def wrapper(self):
            self.engine = engine
            f(self)
        return wrapper
    return decorator


def simple_bool_tag(value):
    return "yes" if value else "Hell No!"


