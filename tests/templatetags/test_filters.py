# -*- coding: utf-8 -*-

from django.test import TestCase
from .utils import set_templates


class FilterTestCase(TestCase):
    @set_templates({'template1': '{{ val|iconify }}'})
    def test_iconify(self):
        result = self.engine.render_to_string('template1', {'val': True})
        self.assertHTMLEqual(result, '<img src="/static/django_stachoutils/img/icon-yes.gif" />')

        result = self.engine.render_to_string('template1', {'val': False})
        self.assertHTMLEqual(result, '<img src="/static/django_stachoutils/img/icon-no.gif" />')
