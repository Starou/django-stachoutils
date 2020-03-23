# -*- coding: utf-8 -*-

import os
import shutil
import tempfile

from django.conf import settings
from django.core.files.images import ImageFile
from django.test import TestCase

from .models import Car


class StorageTest(TestCase):
    def setUp(self):
        self.tmp_media_root = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_media_root)

    def test_overwite_storage(self):
        old_media_root = settings.MEDIA_ROOT
        with self.settings(MEDIA_ROOT=self.tmp_media_root):
            my_car = Car.objects.create(brand="Saab", name="9.3 2.0t")
            with open(os.path.join(old_media_root, "1st_Saab_9-3_SE.jpg"), mode="rb") as f:
                my_car.photo.save("some pic", ImageFile(f))
            self.assertEqual(my_car.photo.name, u'cars/Saab_9.3_2.0t.jpg')
            self.assertEqual(my_car.photo.size, 206420)

            # Change the photo and the name remains the same.
            with open(os.path.join(old_media_root, "Saab_9-3_Vector_sedan.jpg"), mode="rb") as f:
                my_car.photo.save("some pic", ImageFile(f))
            self.assertEqual(my_car.photo.name, u'cars/Saab_9.3_2.0t.jpg')
            self.assertEqual(my_car.photo.size, 384780)
