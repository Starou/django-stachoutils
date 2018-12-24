# -*- coding: utf-8 -*-

import datetime
from django.test import RequestFactory, TestCase
from django_stachoutils import options
from .models import Car
from .utils import set_templates


class PaginationTagTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Car.objects.create(brand='Saab', name='9.3', price=12500, purchased_on=datetime.date(2015, 7, 29))
        Car.objects.create(brand='Saab', name='900', price=1800, purchased_on=datetime.date(2001, 3, 29))
        Car.objects.create(brand='Saab', name='9.5', price=23700, purchased_on=datetime.date(2012, 2, 11))
        Car.objects.create(brand='Alfa-Romeo', name='Giullia', price=19500, purchased_on=datetime.date(2014, 7, 12))
        Car.objects.create(brand='Alfa-Romeo', name='Sprint', price=11200, purchased_on=datetime.date(2015, 9, 29))
        Car.objects.create(brand='Subaru', name='Forester', price=34500, purchased_on=datetime.date(2016, 1, 29))
        Car.objects.create(brand='Subaru', name='Impreza', price=11200, purchased_on=datetime.date(2012, 6, 29))

    def setUp(self):
        self.queryset = Car.objects.all().order_by('brand', 'name')
        self.rf = RequestFactory()

    @set_templates({'template1': '{% paginator_number page current_page_index get_params %}'})
    def test_paginator_number(self):
        request = self.rf.get('/cars?page=2')
        page = options.paginate(request, self.queryset, paginate_by=3)

        # The usage is to loop over all pages of page (current_page_index being the
        # iterator position).
        result = self.engine.render_to_string('template1', {
            'page': page,
            'current_page_index': 0,
            'get_params': {'page': 2},
        })
        self.assertHTMLEqual(result, '<a href="?page=1">1</a>')

        result = self.engine.render_to_string('template1', {
            'page': page,
            'current_page_index': 1,
            'get_params': {'page': 2},
        })
        self.assertHTMLEqual(result, '<span class="this-page">2</span>')

        result = self.engine.render_to_string('template1', {
            'page': page,
            'current_page_index': 2,
            'get_params': {'page': 2},
        })
        self.assertHTMLEqual(result, '<a class="end" href="?page=3">3</a>')

    @set_templates({'template1': '{% paginate_by_number page paginate_by current_pagination get_params %}'})
    def test_paginate_by_number(self):
        request = self.rf.get('/cars?page=2&paginate_by=3')
        page = options.paginate(request, self.queryset, paginate_by=3)

        result = self.engine.render_to_string('template1', {
            'page': page,
            'paginate_by': 5,
            'get_params': {'page': 2, 'paginate_by': 3},
        })
        self.assertHTMLEqual(result, '<a href="?page=2&paginate_by=5">5</a>')

    @set_templates({'template1': '{% pagination page get_params %}'})
    def test_pagination(self):
        request = self.rf.get('/cars?page=2&paginate_by=3')
        page = options.paginate(request, self.queryset, paginate_by=3)
        result = self.engine.render_to_string('template1', {
            'page': page,
            'get_params': {'page': 2, 'paginate_by': 3},
        })
        self.assertHTMLEqual(result,
            """
            <p class="paginator">
                <a href="?page=1">1</a>
                <span class="this-page">2</span>
                <a href="?page=3" class="end">3</a>
            7 entrées
            </p>
            """
        )

    @set_templates({'template1': '{% pagination page get_params %}'})
    def test_pagination_with_more_than_10_pages(self):
        Car.objects.create(brand='Volvo', name='850', price=11500, purchased_on=datetime.date(2011, 7, 29))
        Car.objects.create(brand='Triumph', name='SpitFire', price=5800, purchased_on=datetime.date(2002, 4, 29))
        Car.objects.create(brand='Fiat', name='126', price=2700, purchased_on=datetime.date(2014, 2, 11))
        Car.objects.create(brand='Honda', name='Civic', price=9500, purchased_on=datetime.date(2012, 7, 11))
        Car.objects.create(brand='Honda', name='S2000', price=11900, purchased_on=datetime.date(2010, 9, 9))
        Car.objects.create(brand='Mercedes', name='Class G', price=44500, purchased_on=datetime.date(2017, 1, 21))
        Car.objects.create(brand='Jaguar', name='XJ12', price=12200, purchased_on=datetime.date(2011, 5, 29))

        request = self.rf.get('/cars?page=10&paginate_by=1')
        page = options.paginate(request, self.queryset, paginate_by=1)
        result = self.engine.render_to_string('template1', {
            'page': page,
            'get_params': {'page': 10, 'paginate_by': 1},
        })
        self.assertHTMLEqual(result,
            """
            <p class="paginator">
                <a href="?page=1">1</a>
                <a href="?page=2">2</a>
                ...
                <a href="?page=8">8</a>
                <a href="?page=9">9</a>
                <span class="this-page">10</span>
                <a href="?page=11">11</a>
                <a href="?page=12">12</a>
                <a href="?page=13">13</a>
                <a href="?page=14" class="end">14</a>
            14 entrées
            </p>
            """
        )

        request = self.rf.get('/cars?page=1&paginate_by=1')
        page = options.paginate(request, self.queryset, paginate_by=1)
        result = self.engine.render_to_string('template1', {
            'page': page,
            'get_params': {'page': 1, 'paginate_by': 1},
        })
        self.assertHTMLEqual(result,
            """
            <p class="paginator">
                <span class="this-page">1</span>
                <a href="?page=2">2</a>
                <a href="?page=3">3</a>
                <a href="?page=4">4</a>
                <a href="?page=5">5</a>
                ...
                <a href="?page=13">13</a>
                <a href="?page=14" class="end">14</a>
            14 entrées
            </p>
            """
        )
