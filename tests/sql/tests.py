# -*- coding: utf-8 -*-

from django.test import TestCase
from .models import Car


class AggregateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c1 = Car.objects.create(brand=u"Saab", name=u"9-3 2.0T",
                                    type=u"Coupé", top_speed=230, sales=150000)
        cls.c2 = Car.objects.create(brand=u"Saab", name=u"900 Turbo16",
                                    type=u"Coupé", top_speed=215, sales=225000)
        cls.c3 = Car.objects.create(brand=u"Alfa Roméo", name=u"Giulietta 2.0",
                                    type=u"Sedan", top_speed=185, sales=115000)
        cls.c4 = Car.objects.create(brand=u"Alfa Roméo", name=u"GTV",
                                    type=u"Coupé", top_speed=195, sales=65000)
        cls.c5 = Car.objects.create(brand=u"Lada", name=u"Niva",
                                    type=u"4x4", top_speed=150, sales=300000)

    def test_count_case(self):
        from django_stachoutils.sql import CountCase
        qset = Car.objects.all().aggregate(nb_coupes=CountCase('type', when=u"Coupé"))
        self.assertEqual(qset['nb_coupes'], 3)

    def test_count_case2(self):
        from django_stachoutils.sql import CountCase2
        qset = Car.objects.all().aggregate(nb_rapides=CountCase2('type',
                                                                 when=u"top_speed > 190",
                                                                 quote=""))
        self.assertEqual(qset['nb_rapides'], 3)

    def test_sum_case(self):
        from django_stachoutils.sql import SumCase
        qset = Car.objects.all().aggregate(
            nb_ventes_coupes=SumCase('sales',
                                     case_expression="type",
                                     when=u"Coupé"))
        self.assertEqual(qset['nb_ventes_coupes'], 440000)
