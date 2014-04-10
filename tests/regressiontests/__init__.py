# -*- coding: utf-8 -*-

import unittest


class StachoutilsTestCase(unittest.TestCase):
    def test_lowerize(self):
        from django_stachoutils import lowerize

        self.assertEqual(lowerize(u"L'ARBRE à CHAT"), u"L'Arbre à Chat")


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(StachoutilsTestCase)
    return suite
