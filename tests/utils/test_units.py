# -*- coding: utf-8 -*-

import unittest


class StachoutilsTestCase(unittest.TestCase):
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


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(StachoutilsTestCase)
    return suite
