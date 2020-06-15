# -*- coding: utf-8 -*-

import datetime
from django.test import TestCase
from unittest import skipIf

from .models import Car
from .utils import set_templates


class FilterTest(TestCase):
    @set_templates({'template1': '{{ val|iconify }}'})
    def test_iconify(self):
        result = self.engine.render_to_string('template1', {'val': True})
        self.assertHTMLEqual(result, '<img src="/static/django_stachoutils/img/icon-yes.gif" />')

        result = self.engine.render_to_string('template1', {'val': False})
        self.assertHTMLEqual(result, '<img src="/static/django_stachoutils/img/icon-no.gif" />')

    @set_templates({'template1': '{{ val|processing }}'})
    def test_processing(self):
        result = self.engine.render_to_string('template1', {'val': True})
        self.assertHTMLEqual(result, '<img src="/static/django_stachoutils/img/processing.png" />')

        result = self.engine.render_to_string('template1', {'val': False})
        self.assertHTMLEqual(result, '<img src="/static/django_stachoutils/img/icon-yes.gif" />')

    @set_templates({'template1': '{{ obj|default_if_newrecord:current_index }}'})
    def test_default_if_new_record(self):
        car = Car()
        result = self.engine.render_to_string('template1', {'obj': car, 'current_index': 11})
        self.assertHTMLEqual(result, '11')

        car = Car.objects.create(brand='Saab', name='9-5 2.3T', price=23500,
                                 purchased_on=datetime.date(2018, 4, 1))
        result = self.engine.render_to_string('template1', {'obj': car, 'current_index': 11})
        self.assertHTMLEqual(result, '9-5 2.3T')

    @set_templates({'template1': '{{ val|truncate:10 }}'})
    def test_truncate(self):
        result = self.engine.render_to_string('template1', {'val': 'John'})
        self.assertHTMLEqual(result, 'John')

        result = self.engine.render_to_string('template1', {'val': 'John-the-Baptist'})
        self.assertHTMLEqual(result, 'John-the-B...')

    @set_templates({'template1': '{{ val|truncate:by }}'})
    def test_truncate_with_variable(self):
        result = self.engine.render_to_string('template1', {'val': 'John', 'by': 10})
        self.assertHTMLEqual(result, 'John')

        result = self.engine.render_to_string('template1', {'val': 'John-the-Baptist', 'by': 10})
        self.assertHTMLEqual(result, 'John-the-B...')

    @set_templates({'template1': '{{ val|truncate:by }}'})
    def test_bad_truncate(self):
        result = self.engine.render_to_string('template1', {'val': 'John', 'by': 'ten'})
        self.assertHTMLEqual(result, 'John')

        result = self.engine.render_to_string('template1', {'val': 'John-the-Baptist', 'by': 'ten'})
        self.assertHTMLEqual(result, 'John-the-Baptist')

    @set_templates({'template1': '{{ val|mod:3 }}'})
    def test_mod(self):
        result = self.engine.render_to_string('template1', {'val': 10})
        self.assertHTMLEqual(result, '1')

    @set_templates({'template1': '{{ val|progressbar }}'})
    def test_progressbar(self):
        result = self.engine.render_to_string('template1', {'val': 10})
        self.assertHTMLEqual(result,
            """
            <div class="meter-wrap">
                <div class="meter-value" style="background-color: #009ACD; width: 10%;">
                    <div class="meter-text">
                        10
                    </div>
                </div>
            </div>
            """
        )

    @set_templates({'template1': '{{ val|progressbar }}'})
    def test_progressbar_completed(self):
        result = self.engine.render_to_string('template1', {'val': 100})
        self.assertHTMLEqual(result,
            """
            <div class="meter-wrap">
                <div class="meter-value" style="background-color: #BCEE68; width: 100%;">
                    <div class="meter-text">
                        100
                    </div>
                </div>
            </div>
            """
        )

    @set_templates({'template1': '{{ val|progressbar }}'})
    def test_progressbar_with_tuple(self):
        result = self.engine.render_to_string('template1', {'val': (2.0, 5.0)})
        self.assertHTMLEqual(result,
            """
            <div class="meter-wrap">
                <div class="meter-value" style="background-color: #009ACD; width: 40.0%;">
                    <div class="meter-text">
                        2.0/5.0
                    </div>
                </div>
            </div>
            """
        )

    @set_templates({'template1': '{{ val|progressbar }}'})
    def test_progressbar_with_tuple_and_null_values(self):
        result = self.engine.render_to_string('template1', {'val': (0, 0)})
        self.assertHTMLEqual(result,
            """
            <div class="meter-wrap">
                <div class="meter-value" style="background-color: #009ACD; width: 0%;">
                    <div class="meter-text">
                        0/0
                    </div>
                </div>
            </div>
            """
        )

    @skipIf(True, "Need a fix")
    @set_templates({'template1': '{{ val|progressbar }}'})
    def test_progressbar_with_int(self):
        result = self.engine.render_to_string('template1', {'val': (2, 5)})
        self.assertHTMLEqual(result,
            """
            <div class="meter-wrap">
                <div class="meter-value" style="background-color: #009ACD; width: 40%;">
                    <div class="meter-text">
                        2/5
                    </div>
                </div>
            </div>
            """
        )

    @set_templates({'template1': '{{ val|trend_class }}'})
    def test_trend_class(self):
        result = self.engine.render_to_string('template1', {'val': 4})
        self.assertHTMLEqual(result, 'up')

        result = self.engine.render_to_string('template1', {'val': -2})
        self.assertHTMLEqual(result, 'down')
