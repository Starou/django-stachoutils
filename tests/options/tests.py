from django.core.paginator import EmptyPage
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

        queryset = Car.objects.all().order_by('brand', 'name')
        rf = RequestFactory()

        request = rf.get('/')
        pages = options.paginate(request, queryset, paginate_by=4)
        self.assertEqual(len(pages.object_list), 4)
        self.assertEqual(pages.next_page_number(), 2)

        request = rf.get('/?page=2')
        pages = options.paginate(request, queryset, paginate_by=4)
        self.assertEqual(len(pages.object_list), 3)
        self.assertRaises(EmptyPage, pages.next_page_number)

        request = rf.get('/?page=2&paginate_by=2')
        pages = options.paginate(request, queryset)
        self.assertEqual(len(pages.object_list), 2)
        self.assertEqual(pages.next_page_number(), 3)

        request = rf.get('/?page=2&paginate_by=All')
        pages = options.paginate(request, queryset)
        self.assertEqual(len(pages.object_list), 7)
        self.assertRaises(EmptyPage, pages.next_page_number)

        # With an invalid 'page' parameter, paginate will returns the first one.
        request = rf.get('/?page=two')
        pages = options.paginate(request, queryset, paginate_by=4)
        self.assertEqual(pages.number, 1)

        # With an 'page' parameter greater than last page, paginate will returns the last one.
        request = rf.get('/?page=5')
        pages = options.paginate(request, queryset, paginate_by=4)
        self.assertEqual(pages.number, 2)

        # With an invalid 'paginate_by' GET parameter, paginate will use the default value.
        request = rf.get('/?page=2&paginate_by=five')
        pages = options.paginate(request, queryset)
        self.assertFalse(pages.has_next())
