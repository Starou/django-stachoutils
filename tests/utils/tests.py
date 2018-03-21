# -*- coding: utf-8 -*-

import os
from django.test import SimpleTestCase
from django.conf import settings


class UtilsTestCase(SimpleTestCase):
    def test_format_datetime(self):
        from django_stachoutils import format_datetime
        from datetime import datetime
        self.assertEqual(format_datetime(datetime(2017, 1, 31, 16, 58, 33)), u'Jan. 31, 2017, 4:58 p.m.')
        self.assertEqual(format_datetime(datetime(2017, 1, 31, 16, 58, 33), time=False), u'Jan. 31, 2017')
        self.assertEqual(format_datetime(datetime(2017, 1, 31, 16, 58, 33), date=False), u'4:58 p.m.')

    def test_format_number(self):
        from django_stachoutils import format_number
        self.assertEqual(format_number(2312), "2,312")
        self.assertEqual(format_number(2312, u" "), "2 312")
        self.assertEqual(format_number(), "")

    def test_truncate_chars(self):
        from django_stachoutils import truncate_chars
        self.assertEqual(truncate_chars("A quick brown fox jumps", 7), "A quick...")
        self.assertEqual(truncate_chars(u"¿ Holà señor, como estas ?", 12), u"¿ Holà señor...")

    def test_strip_accents(self):
        from django_stachoutils import strip_accents
        self.assertEqual(strip_accents(u"Midi-Pyrénées"), b'Midi-Pyrenees')

    def test_format_xml_entity(self):
        from django_stachoutils import format_xml_entity
        self.assertEqual(format_xml_entity(u"Côtes d'Armor"), b'COTES-D-ARMOR')

    def test_latin1_safe_xml_encode(self):
        from django_stachoutils import latin1_safe_xml_encode
        self.assertEqual(latin1_safe_xml_encode(u"ϟϟ"), '&#991;&#991;')

    def test_clean_lettrine(self):
        from django_stachoutils import clean_lettrine
        self.assertEqual(clean_lettrine(u"P aris. Superbe appartement"),
                         u"Paris. Superbe appartement")
        self.assertEqual(clean_lettrine(u"A 2 pas de la Seine"),
                         u"A 2 pas de la Seine")

    def test_int_to_roman(self):
        from django_stachoutils import int_to_roman
        self.assertEqual(int_to_roman(13), u"XIII")

    def test_filter_non_printable(self):
        from django_stachoutils import filter_non_printable
        self.assertEqual(filter_non_printable(u"This is ϞϞ !\x04"), u"This is ϞϞ !")

    def test_camelize(self):
        from django_stachoutils import camelize
        self.assertEqual(camelize(u"this is a string"), u"This Is A String")

    def test_urldecode(self):
        from django_stachoutils import urldecode
        self.assertEqual(urldecode(u"?foo=1&bar=2"), {u"foo": u"1", u"bar": u"2"})

    def test_files_are_equal(self):
        from django.core.files.base import ContentFile
        from django_stachoutils import files_are_equal

        image1 = os.path.join(settings.MEDIA_ROOT, 'jardin.jpg')
        image2 = os.path.join(settings.MEDIA_ROOT, 'terrasse.jpg')
        f1 = ContentFile(open(image1, 'rb').read())
        f2 = ContentFile(open(image2, 'rb').read())

        # Files are differents by size
        self.assertFalse(files_are_equal(f1, f2))
        self.assertNotEqual(f1.size, f2.size)

        # Files are equals
        f1bis = ContentFile(open(image1, 'rb').read())
        self.assertTrue(files_are_equal(f1, f1bis))

        # Files are differents by content
        f1_altered = ContentFile(open(image1, 'rb').read().replace(b'\x14', b'\xff'))
        self.assertFalse(files_are_equal(f1, f1_altered))
        self.assertEqual(f1.size, f1_altered.size)

    def test_simple_decorator(self):
        from django_stachoutils import simple_decorator

        @simple_decorator
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
