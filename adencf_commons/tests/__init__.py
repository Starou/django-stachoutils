# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.testcases import to_list
from django.conf import settings
import tempfile
import os, shutil

from adencf_commons import lowerize, NO_CAPFIRST

class PublishTestCase(TestCase):
    def setUp(self):
        self.old_dossier_watch_dir  = settings.DOSSIERS_WATCH_DIR 
        settings.DOSSIERS_WATCH_DIR = os.path.join(tempfile.gettempdir(), 'watch')
        if os.path.exists(settings.DOSSIERS_WATCH_DIR):
            shutil.rmtree(settings.DOSSIERS_WATCH_DIR)
        os.mkdir(settings.DOSSIERS_WATCH_DIR)

    def tearDown(self):
        shutil.rmtree(settings.DOSSIERS_WATCH_DIR)
        settings.DOSSIERS_WATCH_DIR = self.old_dossier_watch_dir


def get_obj_dict(obj, extras=('id',)):
    out = obj.__dict__.copy()
    del out['_state']
    for extra in extras:
        del out[extra]
    return out


###


class UtilsTestCase(PublishTestCase):

    def test_files_are_equal(self):
        from django.core.files.base import ContentFile
        from adencf_commons import files_are_equal
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
