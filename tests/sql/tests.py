# -*- coding: utf-8 -*-

from django.db import connection
from django.test import TestCase
from unittest import skipIf
from .models import Car


class AggregateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c1 = Car.objects.create(brand=u"Saab", name=u"9-3 2.0T", type=u"Coupé",
                                    horsepower=200, weight=1300, top_speed=230, sales=150000)
        cls.c2 = Car.objects.create(brand=u"Saab", name=u"900 Turbo16", type=u"Coupé",
                                    horsepower=175, weight=1200, top_speed=215, sales=225000)
        cls.c3 = Car.objects.create(brand=u"Alfa Roméo", name=u"Giulietta 2.0", type=u"Sedan",
                                    horsepower=130, weight=1100, top_speed=185, sales=115000)
        cls.c4 = Car.objects.create(brand=u"Alfa Roméo", name=u"GTV", type=u"Coupé",
                                    horsepower=150, weight=1050, top_speed=195, sales=65000)
        cls.c5 = Car.objects.create(brand=u"Lada", name=u"Niva", type=u"4x4",
                                    horsepower=70, weight=1100, top_speed=150, sales=300000)

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

    @skipIf(connection.vendor == 'sqlite', "SQLite does not respect the cast of integer")
    def test_sum_extra(self):
        from django_stachoutils.sql import SumExtra
        qset = Car.objects.all().aggregate(
            total_horses_per_kg=SumExtra('horsepower',
                                         sum_expression="horsepower/(1.0*weight)"))
        self.assertEqual(qset['total_horses_per_kg'], (200+175+130+150+70)/(1.0*(1300+1200+1100+1050+1100)))
