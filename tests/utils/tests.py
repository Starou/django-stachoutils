# -*- coding: utf-8 -*-

import os
from datetime import datetime
from django.core.files.base import ContentFile
from django.conf import settings
from django.test import SimpleTestCase
from pathlib import Path

import django_stachoutils as utils


class UtilsTest(SimpleTestCase):
    def test_format_datetime(self):
        self.assertEqual(utils.format_datetime(datetime(2017, 1, 31, 16, 58, 33)), u'Jan. 31, 2017, 4:58 p.m.')
        self.assertEqual(utils.format_datetime(datetime(2017, 1, 31, 16, 58, 33), time=False), u'Jan. 31, 2017')
        self.assertEqual(utils.format_datetime(datetime(2017, 1, 31, 16, 58, 33), date=False), u'4:58 p.m.')

    def test_format_number(self):
        self.assertEqual(utils.format_number(2312), "2,312")
        self.assertEqual(utils.format_number(2312, u" "), "2 312")
        self.assertEqual(utils.format_number(), "")

    def test_truncate_chars(self):
        self.assertEqual(utils.truncate_chars("A quick brown fox jumps", 7), "A quick...")
        self.assertEqual(utils.truncate_chars(u"¿ Holà señor, como estas ?", 12), u"¿ Holà señor...")

    def test_strip_accents(self):
        self.assertEqual(utils.strip_accents(u"Midi-Pyrénées"), u'Midi-Pyrenees')

    def test_format_xml_entity(self):
        self.assertEqual(utils.format_xml_entity(u"Côtes d'Armor"), b'COTES-D-ARMOR')

    def test_latin1_safe_xml_encode(self):
        self.assertEqual(utils.latin1_safe_xml_encode(u"ϟϟ"), '&#991;&#991;')

    def test_clean_lettrine(self):
        self.assertEqual(utils.clean_lettrine(u"P aris. Superbe appartement"),
                         u"Paris. Superbe appartement")
        self.assertEqual(utils.clean_lettrine(u"A 2 pas de la Seine"),
                         u"A 2 pas de la Seine")

    def test_int_to_roman(self):
        self.assertEqual(utils.int_to_roman(13), u"XIII")

    def test_filter_non_printable(self):
        self.assertEqual(utils.filter_non_printable(u"This is ϞϞ !\x04"), u"This is ϞϞ !")

    def test_camelize(self):
        self.assertEqual(utils.camelize(u"this is a string"), u"This Is A String")

    def test_urldecode(self):
        self.assertEqual(utils.urldecode(u"?foo=1&bar=2"), {u"foo": u"1", u"bar": u"2"})

    def test_files_are_equal(self):
        image1 = os.path.join(settings.MEDIA_ROOT, 'jardin.jpg')
        image2 = os.path.join(settings.MEDIA_ROOT, 'terrasse.jpg')
        f1 = ContentFile(Path(image1).read_bytes())
        f2 = ContentFile(Path(image2).read_bytes())

        # Files are differents by size
        self.assertFalse(utils.files_are_equal(f1, f2))
        self.assertNotEqual(f1.size, f2.size)

        # Files are equals
        f1bis = ContentFile(Path(image1).read_bytes())
        self.assertTrue(utils.files_are_equal(f1, f1bis))

        # Files are differents by content
        f1_altered = ContentFile(Path(image1).read_bytes().replace(b'\x14', b'\xff'))
        self.assertFalse(utils.files_are_equal(f1, f1_altered))
        self.assertEqual(f1.size, f1_altered.size)

    def test_simple_decorator(self):
        @utils.simple_decorator
        def mess_with_the_data(func):
            def new_function(a, b):
                return func(a**2, b**2)
            return new_function

        @mess_with_the_data
        def addition(a, b):
            """A basic mathematical function"""
            return a + b

        self.assertEqual(addition(2, 3), 13)
        self.assertEqual(addition.__doc__, 'A basic mathematical function')
        self.assertEqual(addition.__name__, 'addition')
