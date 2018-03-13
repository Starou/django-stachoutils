from django.test import RequestFactory, TestCase

from django_stachoutils import options
from .models import Car


class PaginateTestCase(TestCase):
    def test_paginate(self):
        Car.objects.create(brand='Saab', name='9.3')
        Car.objects.create(brand='Saab', name='900')
        Car.objects.create(brand='Saab', name='9.5')
        Car.objects.create(brand='Alfa-Romeo', name='Giullia')
        Car.objects.create(brand='Alfa-Romeo', name='Sprint')
        Car.objects.create(brand='Subaru', name='Forester')
        Car.objects.create(brand='Subaru', name='Impreza')

        rf = RequestFactory()
        request = rf.get('/')
        pages = options.paginate(request, Car.objects.all().order_by('brand', 'name'), paginate_by=4)
        self.assertEqual(len(pages.object_list), 4)
        self.assertEqual(pages.next_page_number(), 2)
