# -*- coding: utf-8 -*-

import unittest


class GenericTestCase(unittest.TestCase):
    def test_regroup_actions(self):
        from django_stachoutils.views.actions import regroup_actions
        
        def action1():
            pass
        action1.group = "groupA"

        def action2():
            pass
        action2.group = "groupB"


        def action3():
            pass
        action3.group = "groupA"

        def action4():
            pass

        self.assertEqual(
            regroup_actions([action1, action2, action3]),
            [('groupA', [action1, action3]),
             ('groupB', [action2])]
        )

        self.assertEqual(
            regroup_actions([action1, action2, action3, action4]),
            [('groupA', [action1, action3]),
             ('groupB', [action2]),
             ('autres', [action4])]
        )


def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(GenericTestCase)
    return suite
