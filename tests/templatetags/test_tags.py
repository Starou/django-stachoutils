# -*- coding: utf-8 -*-

from django.template.engine import Engine
from django.test import TestCase
from django.utils.http import urlencode
from functools import wraps

from .models import Car


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


class TableTagTestCase(TestCase):
    column = [
        {'label': 'Name', 'field': 'name', 'link': {'href': 'get_absolute_url'}},
        {'label': 'Brand', 'field': 'brand'},
        {'label': 'Price', 'field': 'price_html'},
    ]

    @set_templates({'template1': '{% table_header_tag columns full_path %}'})
    def test_table_header_tag(self):
        result = self.engine.render_to_string('template1', {
            'columns': self.column,
            'full_path': "/cars?theme=dark&paginate_by=25"})

        self.assertHTMLEqual(result, """
            <th class="action-checkbox-column"> <input id="action-toggle" type="checkbox" style="display: inline;"></th>
            <th><a href="?%s">Name</a><input class="fieldname" type="hidden" value="name"/></th>
            <th><a href="?%s">Brand</a><input class="fieldname" type="hidden" value="brand"/></th>
            <th><a href="?%s">Price</a><input class="fieldname" type="hidden" value="price_html"/></th>
        """ % (
            urlencode([('o', '0'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '1'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '2'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
        ))

    @set_templates({'template1': '{% table_header_tag columns full_path %}'})
    def test_table_header_tag_sorted_asc(self):
        result = self.engine.render_to_string('template1', {
            'columns': self.column,
            'full_path': "/cars?theme=dark&paginate_by=25&ot=asc&o=1"})

        self.assertHTMLEqual(result, """
            <th class="action-checkbox-column"> <input id="action-toggle" type="checkbox" style="display: inline;"></th>
            <th><a href="?%s">Name</a><input class="fieldname" type="hidden" value="name"/></th>
            <th class="ascending sorted"><a href="?%s">Brand</a><input class="fieldname" type="hidden" value="brand"/></th>
            <th><a href="?%s">Price</a><input class="fieldname" type="hidden" value="price_html"/></th>
        """ % (
            urlencode([('o', '0'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '1'), ('ot', 'desc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '2'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
        ))

    @set_templates({'template1': '{% table_header_tag columns full_path %}'})
    def test_table_header_tag_sorted_desc(self):
        result = self.engine.render_to_string('template1', {
            'columns': self.column,
            'full_path': "/cars?theme=dark&paginate_by=25&ot=desc&o=1"})

        self.assertHTMLEqual(result, """
            <th class="action-checkbox-column"> <input id="action-toggle" type="checkbox" style="display: inline;"></th>
            <th><a href="?%s">Name</a><input class="fieldname" type="hidden" value="name"/></th>
            <th class="descending sorted"><a href="?%s">Brand</a><input class="fieldname" type="hidden" value="brand"/></th>
            <th><a href="?%s">Price</a><input class="fieldname" type="hidden" value="price_html"/></th>
        """ % (
            urlencode([('o', '0'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '1'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '2'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
        ))

    @set_templates({'template1': '{% table_row_tag columns car %}'})
    def test_table_row_tag(self):
        car = Car.objects.create(brand='Saab', name='9.3 2.0t', price=12500)
        result = self.engine.render_to_string('template1', {
            'columns': self.column,
            'car': car})
        self.assertHTMLEqual(result, """
            <td class="pk"><input type="checkbox" name="_selected_action" value="1" class="action-select"></td>
            <td class=""><a title="" href="cars/1/">9.3 2.0t</a></td> <td class="">Saab</td> <td class=""><em>12500</em>€</td>
        """)
