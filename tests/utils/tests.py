# -*- coding: utf-8 -*-

import os
from django.test import TestCase
from django.conf import settings


class UtilsTestCase(TestCase):
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
