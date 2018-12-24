# -*- coding: utf-8 -*-

import datetime
from django.test import TestCase
from django.utils.http import urlencode

from .models import Car
from .utils import set_templates, simple_bool_tag


class TableTagTest(TestCase):
    columns = [
        {'label': 'Name', 'field': 'name', 'link': {'href': 'get_absolute_url', 'style': 'nowrap', 'title': '__str__'}},
        {'label': 'Brand', 'field': 'brand'},
        {'label': 'Price', 'field': 'price_html', 'editable': True},
        {'label': 'Purchased Year', 'field': 'purchased_on', 'filters': [('date', 'Y')]},
        {'label': 'For Sale', 'field': 'for_sale', 'tags': [simple_bool_tag]},
    ]

    @set_templates({'template1': '{% table_header_tag columns full_path %}'})
    def test_table_header_tag(self):
        result = self.engine.render_to_string('template1', {
            'columns': self.columns,
            'full_path': "/cars?theme=dark&paginate_by=25"})

        self.assertHTMLEqual(result, """
            <th class="action-checkbox-column"> <input id="action-toggle" type="checkbox" style="display: inline;"></th>
            <th><a href="?%s">Name</a><input class="fieldname" type="hidden" value="name"/></th>
            <th><a href="?%s">Brand</a><input class="fieldname" type="hidden" value="brand"/></th>
            <th><a href="?%s">Price</a><input class="fieldname" type="hidden" value="price_html"/></th>
            <th><a href="?%s">Purchased Year</a><input class="fieldname" type="hidden" value="purchased_on" /></th>
            <th><a href="?%s">For Sale</a><input class="fieldname" type="hidden" value="for_sale" /></th>
        """ % (
            urlencode([('o', '0'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '1'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '2'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '3'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '4'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
        ))

    @set_templates({'template1': '{% table_header_tag columns full_path %}'})
    def test_table_header_tag_sorted_asc(self):
        result = self.engine.render_to_string('template1', {
            'columns': self.columns,
            'full_path': "/cars?theme=dark&paginate_by=25&ot=asc&o=1"})

        self.assertHTMLEqual(result, """
            <th class="action-checkbox-column"> <input id="action-toggle" type="checkbox" style="display: inline;"></th>
            <th><a href="?%s">Name</a><input class="fieldname" type="hidden" value="name"/></th>
            <th class="ascending sorted"><a href="?%s">Brand</a><input class="fieldname" type="hidden" value="brand"/></th>
            <th><a href="?%s">Price</a><input class="fieldname" type="hidden" value="price_html"/></th>
            <th><a href="?%s">Purchased Year</a><input class="fieldname" type="hidden" value="purchased_on" /></th>
            <th><a href="?%s">For Sale</a><input class="fieldname" type="hidden" value="for_sale" /></th>
        """ % (
            urlencode([('o', '0'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '1'), ('ot', 'desc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '2'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '3'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '4'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
        ))

    @set_templates({'template1': '{% table_header_tag columns full_path %}'})
    def test_table_header_tag_sorted_desc(self):
        result = self.engine.render_to_string('template1', {
            'columns': self.columns,
            'full_path': "/cars?theme=dark&paginate_by=25&ot=desc&o=1"})

        self.assertHTMLEqual(result, """
            <th class="action-checkbox-column"> <input id="action-toggle" type="checkbox" style="display: inline;"></th>
            <th><a href="?%s">Name</a><input class="fieldname" type="hidden" value="name"/></th>
            <th class="descending sorted"><a href="?%s">Brand</a><input class="fieldname" type="hidden" value="brand"/></th>
            <th><a href="?%s">Price</a><input class="fieldname" type="hidden" value="price_html"/></th>
            <th><a href="?%s">Purchased Year</a><input class="fieldname" type="hidden" value="purchased_on" /></th>
            <th><a href="?%s">For Sale</a><input class="fieldname" type="hidden" value="for_sale" /></th>
        """ % (
            urlencode([('o', '0'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '1'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '2'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '3'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
            urlencode([('o', '4'), ('ot', 'asc'), ('paginate_by', '25'), ('theme', 'dark')]),
        ))

    @set_templates({'template1': '{% table_row_tag columns car %}'})
    def test_table_row_tag(self):
        car = Car.objects.create(brand='Saab', name='9.3 2.0t', price=12500,
                                 purchased_on=datetime.date(2015, 7, 29),
                                 for_sale=True)
        result = self.engine.render_to_string('template1', {
            'columns': self.columns,
            'car': car})
        self.assertHTMLEqual(result, """
            <td class="pk"><input type="checkbox" name="_selected_action" value="1" class="action-select"></td>
            <td class=""><a class="nowrap" href="cars/1/" title="9.3 2.0t">9.3 2.0t</a></td>
            <td class="">Saab</td>
            <td class="editable"><em>12500</em>€</td>
            <td class="">2015</td>
            <td class="">yes</td>
        """)


class InlineTagTest(TestCase):
    @set_templates({'template1': '{% inline_display_class inlines_visibles inline counter %}'})
    def test_inline_display_class(self):
        result = self.engine.render_to_string('template1', {
            'inlines_visibles': {'caroption_set': '1,3',
                                 'cardriver_set': '0'},
            'inline': 'caroption_set',
            'counter': '3'})
        self.assertHTMLEqual(result, '')

        result = self.engine.render_to_string('template1', {
            'inlines_visibles': {'caroption_set': '1,3',
                                 'cardriver_set': '0'},
            'inline': 'caroption_set',
            'counter': '2'})
        self.assertHTMLEqual(result, 'closed')

        result = self.engine.render_to_string('template1', {
            'inlines_visibles': {'caroption_set': '1,3',
                                 'cardriver_set': '0'},
            'inline': 'carbuyer_set',
            'counter': '2'})
        self.assertHTMLEqual(result, '')

    @set_templates({'template1': '{% inline_display_style inlines_visibles inline counter %}'})
    def test_inline_display_style(self):
        result = self.engine.render_to_string('template1', {
            'inlines_visibles': {'caroption_set': '1,3',
                                 'cardriver_set': '0'},
            'inline': 'caroption_set',
            'counter': '3'})
        self.assertHTMLEqual(result, '')

        result = self.engine.render_to_string('template1', {
            'inlines_visibles': {'caroption_set': '1,3',
                                 'cardriver_set': '0'},
            'inline': 'caroption_set',
            'counter': '2'})
        self.assertHTMLEqual(result, 'display: none;')
