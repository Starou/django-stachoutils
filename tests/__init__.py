# -*- coding: utf-8 -*-

import os
from django.test import TestCase
from django.conf import settings

from django_stachoutils import lowerize, NO_CAPFIRST


class UtilsTestCase(TestCase):
    def test_files_are_equal(self):
        from django.core.files.base import ContentFile
        from django_stachoutils import files_are_equal
        MEDIA_ROOT = os.path.join(settings.MEDIA_ROOT, 'test')
        img_root = os.path.join(MEDIA_ROOT, 'images')

        image1 = os.path.join(img_root, 'jardin.jpg')
        image2 = os.path.join(img_root, 'terrasse.jpg')
        f1 = ContentFile(open(image1, 'rb').read())
        f2 = ContentFile(open(image2, 'rb').read())

        self.assertFalse(files_are_equal(f1, f2))

        f1bis = ContentFile(open(image1, 'rb').read())
        self.assertTrue(files_are_equal(f1, f1bis))

    def test_lowerize(self):
        for test_string, expected in [
                    ('LOWER THIS', 'Lower This'),
                    ('Les Carrés De Monthoux', 'Les Carrés de Monthoux'),
                ]:
            self.assertEqual(lowerize(test_string, NO_CAPFIRST), expected)
