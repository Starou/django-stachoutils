# -*- coding: utf-8 -*-

from django.test import TestCase
from .models import Car


class AggregateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c1 = Car.objects.create(brand=u"Saab", name=u"9-3", type=u"Coupé")
        cls.c2 = Car.objects.create(brand=u"Saab", name=u"900 Turbo16", type=u"Coupé")
        cls.c3 = Car.objects.create(brand=u"Alfa Roméo", name=u"Giulietta", type=u"Sedan")
        cls.c4 = Car.objects.create(brand=u"Alfa Roméo", name=u"GTV", type=u"Coupé")
        cls.c5 = Car.objects.create(brand=u"Lada", name=u"Niva", type=u"4x4")

    def test_count_case(self):
        from django_stachoutils.sql import CountCase
        qset = Car.objects.all().aggregate(nb_coupes=CountCase('type', when=u"Coupé"))
        self.assertEqual(qset['nb_coupes'], 3)
