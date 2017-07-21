# -*- coding: utf-8 -*-

import unittest


class StachoutilsTestCase(unittest.TestCase):
    def test_lowerize(self):
        from django_stachoutils import lowerize
        self.assertEqual(lowerize(u"L'ARBRE à CHAT"), u"L'Arbre à Chat")

    def test_truncate_chars(self):
        from django_stachoutils import truncate_chars
        self.assertEqual(truncate_chars("A quick brown fox jumps", 7), "A quick...")
        self.assertEqual(truncate_chars(u"¿ Holà señor, como estas ?", 12), u"¿ Holà señor...")


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(StachoutilsTestCase)
    return suite
