from django.core.paginator import EmptyPage
from django.test import RequestFactory, TestCase

from django_stachoutils import options
from .models import Car


class PaginateTest(TestCase):
    def test_paginate(self):
        Car.objects.create(brand='Saab', name='9.3')
        Car.objects.create(brand='Saab', name='900')
        Car.objects.create(brand='Saab', name='9.5')
        Car.objects.create(brand='Alfa-Romeo', name='Giullia')
        Car.objects.create(brand='Alfa-Romeo', name='Sprint')
        Car.objects.create(brand='Subaru', name='Forester')
        Car.objects.create(brand='Subaru', name='Impreza')

        queryset = Car.objects.all().order_by('brand', 'name')
        rf = RequestFactory()

        request = rf.get('/')
        page = options.paginate(request, queryset, paginate_by=4)
        self.assertEqual(len(page.object_list), 4)
        self.assertEqual(page.next_page_number(), 2)

        request = rf.get('/?page=2')
        page = options.paginate(request, queryset, paginate_by=4)
        self.assertEqual(len(page.object_list), 3)
        self.assertRaises(EmptyPage, page.next_page_number)

        request = rf.get('/?page=2&paginate_by=2')
        page = options.paginate(request, queryset)
        self.assertEqual(len(page.object_list), 2)
        self.assertEqual(page.next_page_number(), 3)

        request = rf.get('/?page=2&paginate_by=All')
        page = options.paginate(request, queryset)
        self.assertEqual(len(page.object_list), 7)
        self.assertRaises(EmptyPage, page.next_page_number)

        # With an invalid 'page' parameter, paginate will returns the first one.
        request = rf.get('/?page=two')
        page = options.paginate(request, queryset, paginate_by=4)
        self.assertEqual(page.number, 1)

        # With an 'page' parameter greater than last page, paginate will returns the last one.
        request = rf.get('/?page=5')
        page = options.paginate(request, queryset, paginate_by=4)
        self.assertEqual(page.number, 2)

        # With an invalid 'paginate_by' GET parameter, paginate will use the default value.
        request = rf.get('/?page=2&paginate_by=five')
        page = options.paginate(request, queryset)
        self.assertFalse(page.has_next())
