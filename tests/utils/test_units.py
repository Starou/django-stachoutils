# -*- coding: utf-8 -*-

import unittest


class StachoutilsTestCase(unittest.TestCase):
    def test_truncate_chars(self):
        from django_stachoutils import truncate_chars
        self.assertEqual(truncate_chars("A quick brown fox jumps", 7), "A quick...")
        self.assertEqual(truncate_chars(u"¿ Holà señor, como estas ?", 12), u"¿ Holà señor...")

    def test_strip_accents(self):
        from django_stachoutils import strip_accents
        self.assertEqual(strip_accents(u"Midi-Pyrénées"), 'Midi-Pyrenees')

    def test_format_xml_entity(self):
        from django_stachoutils import format_xml_entity
        self.assertEqual(format_xml_entity(u"Côtes d'Armor"), 'COTES-D-ARMOR')

    def test_latin1_safe_xml_encode(self):
        from django_stachoutils import latin1_safe_xml_encode
        self.assertEqual(latin1_safe_xml_encode(u"ϟϟ"), '&#991;&#991;')


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(StachoutilsTestCase)
    return suite
