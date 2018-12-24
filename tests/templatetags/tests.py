# -*- coding: utf-8 -*-

from django.test import TestCase


class TemplateTagsTest(TestCase):
    def test_current_filters_html(self):
        from django_stachoutils.templatetags.stachoutils_extras import current_filters
        filters = [
            (u'statut', [
                ('valide__exact=1&assistant__exact=6', 'All', True),
                ('valide__exact=1&assistant__exact=6&statut__exact=1', u'Relation Client', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=2', u'Production', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=3', u'P.A.O.', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=4', u'Publicité à Valider', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=5', u'Accord Bon à Tirer', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=6', u'Publicité Modifiée', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=7', u'OK Fab', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=8', u'Correction Demandées', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=9', u'BAT Bloqué', False)
            ]),
            (u'BAT demandé', [
                ('valide__exact=1&assistant__exact=6', 'All', None),
                ('valide__exact=1&assistant__exact=6&bat_demande__exact=1', 'Oui', False),
                ('valide__exact=1&assistant__exact=6&bat_demande__exact=0', 'Non', True)
            ]),
            (u'chargé de clientèle', [
                ('valide__exact=1', 'All', None),
                ('valide__exact=1&assistant__exact=8', u'Isabelle G.', False),
                ('valide__exact=1&assistant__exact=6', u'Marie-Françoise B.', True),
                ('valide__exact=1&assistant__exact=41', u'Émilie G.', False),
                ('valide__exact=1&assistant__exact=1445', u'Séverine T.', False),
                ('assistant__isnull=True&valide__exact=1&assistant__exact=6', u'Aucun', None)
            ]),
        ]

        self.assertEqual(current_filters(filters),
                         [u'BAT demandé: <strong>Non</strong>',
                          u'chargé de clientèle: <strong>Marie-Françoise B.</strong>'])

        # Should works with a filter not selected.
        filters = [
            (u'statut', [
                ('valide__exact=1&assistant__exact=6', 'All', None),
                ('valide__exact=1&assistant__exact=6&statut__exact=1', u'Relation Client', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=2', u'Production', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=3', u'P.A.O.', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=4', u'Publicité à Valider', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=5', u'Accord Bon à Tirer', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=6', u'Publicité Modifiée', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=7', u'OK Fab', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=8', u'Correction Demandées', False),
                ('valide__exact=1&assistant__exact=6&statut__exact=9', u'BAT Bloqué', False)
            ]),
            (u'BAT demandé', [
                ('valide__exact=1&assistant__exact=6', 'All', None),
                ('valide__exact=1&assistant__exact=6&bat_demande__exact=1', 'Oui', False),
                ('valide__exact=1&assistant__exact=6&bat_demande__exact=0', 'Non', True)
            ]),
            (u'chargé de clientèle', [
                ('valide__exact=1', 'All', None),
                ('valide__exact=1&assistant__exact=8', u'Isabelle G.', False),
                ('valide__exact=1&assistant__exact=6', u'Marie-Françoise B.', True),
                ('valide__exact=1&assistant__exact=41', u'Émilie G.', False),
                ('valide__exact=1&assistant__exact=1445', u'Séverine T.', False),
                ('assistant__isnull=True&valide__exact=1&assistant__exact=6', u'Aucun', None)
            ]),
        ]

        self.assertEqual(current_filters(filters),
                         [u'BAT demandé: <strong>Non</strong>',
                          u'chargé de clientèle: <strong>Marie-Françoise B.</strong>'])
