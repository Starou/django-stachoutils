import datetime
from django.test import RequestFactory, TestCase
from django_stachoutils import options
from .models import Car
from .utils import set_templates


class PaginationTagTestCase(TestCase):
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
        self.assertHTMLEqual(result, '<a href="?paginate_by=5&page=2">5</a>')
