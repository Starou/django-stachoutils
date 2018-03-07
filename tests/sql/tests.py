# -*- coding: utf-8 -*-

from django.test import TestCase


class SQLTestCase(TestCase):
    def test_count_case(self):
        from django_stachoutils.sql import CountCase
        nb_hits_9 = CountCase('score', when='nine')
