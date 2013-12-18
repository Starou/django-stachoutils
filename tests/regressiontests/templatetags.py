# -*- coding: utf-8 -*-

import os
import unittest



class TemplateTagsTestCase(unittest.TestCase):
    def test_current_filters_html(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = "settings"
        from django_stachoutils.templatetags.stachoutils_extras import current_filters
        filters = [
            (u'statut', False, [
                ('valide__exact=1&assistant__exact=6', u'Tout', True),
                ('valide__exact=1&assistant__exact=6&statut__exact=1', u'Relation Client', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=2', u'Production', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=3', u'P.A.O.', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=4', u'Publicit\xe9 \xe0 Valider', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=5', u'Accord Bon \xe0 Tirer', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=6', u'Publicit\xe9 Modifi\xe9e', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=7', u'OK Fab', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=8', u'Correction Demand\xe9es', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=9', u'BAT Bloqu\xe9', False)
            ]),
            (u'BAT demand\xe9', False, [
                ('valide__exact=1&assistant__exact=6', u'Tout', None),
                ('valide__exact=1&assistant__exact=6&bat_demande__exact=1', 'Oui', False),
                ('valide__exact=1&assistant__exact=6&bat_demande__exact=0', 'Non', True)
            ]),
            (u'charg\xe9 de client\xe8le', False, [
                ('valide__exact=1', u'Tout', None),
                ('valide__exact=1&assistant__exact=8', u'Isabelle G.', False),
                ('valide__exact=1&assistant__exact=6', u'Marie-Fran\xe7oise B.', True),
                ('valide__exact=1&assistant__exact=41', u'\xc9milie G.', False),
                ('valide__exact=1&assistant__exact=1445', u'S\xe9verine T.', False),
                ('assistant__isnull=True&valide__exact=1&assistant__exact=6', u'Aucun', None)
            ]),
        ]

        self.assertEqual(current_filters(filters),
                         [u'BAT demand\xe9: <strong>Non</strong>',
                          u'charg\xe9 de client\xe8le: <strong>Marie-Fran\xe7oise B.</strong>'])
        
        # Should works with a filter not selected.
        filters = [
            (u'statut', False, [
                ('valide__exact=1&assistant__exact=6', u'Tout', None),
                ('valide__exact=1&assistant__exact=6&statut__exact=1', u'Relation Client', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=2', u'Production', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=3', u'P.A.O.', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=4', u'Publicit\xe9 \xe0 Valider', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=5', u'Accord Bon \xe0 Tirer', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=6', u'Publicit\xe9 Modifi\xe9e', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=7', u'OK Fab', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=8', u'Correction Demand\xe9es', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=9', u'BAT Bloqu\xe9', False)
            ]),
            (u'BAT demand\xe9', False, [
                ('valide__exact=1&assistant__exact=6', u'Tout', None),
                ('valide__exact=1&assistant__exact=6&bat_demande__exact=1', 'Oui', False),
                ('valide__exact=1&assistant__exact=6&bat_demande__exact=0', 'Non', True)
            ]),
            (u'charg\xe9 de client\xe8le', False, [
                ('valide__exact=1', u'Tout', None),
                ('valide__exact=1&assistant__exact=8', u'Isabelle G.', False),
                ('valide__exact=1&assistant__exact=6', u'Marie-Fran\xe7oise B.', True),
                ('valide__exact=1&assistant__exact=41', u'\xc9milie G.', False),
                ('valide__exact=1&assistant__exact=1445', u'S\xe9verine T.', False),
                ('assistant__isnull=True&valide__exact=1&assistant__exact=6', u'Aucun', None)
            ]),
        ]

        self.assertEqual(current_filters(filters),
                         [u'BAT demand\xe9: <strong>Non</strong>',
                          u'charg\xe9 de client\xe8le: <strong>Marie-Fran\xe7oise B.</strong>'])



def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TemplateTagsTestCase)
    return suite
