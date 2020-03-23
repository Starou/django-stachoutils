# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile

from django import forms
from django.conf import settings
from django.core.files.images import ImageFile
from django.test import TestCase, modify_settings

from .models import House, Person


@modify_settings(INSTALLED_APPS={'append': 'django_thumbor', 'remove': 'sorl.thumbnail'})
class ThumborFieldsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.h1 = House.objects.create(address="12, rue de la Paix", city="Paris")

    def setUp(self):
        self.tmp_media_root = tempfile.mkdtemp()
        # widgets.py has to be reloaded for contextual import to be performed.
        if 'django_stachoutils.forms.widgets' in sys.modules:
            self.widgets_mod = sys.modules.pop('django_stachoutils.forms.widgets')
            self.fields_mod = sys.modules.pop('django_stachoutils.forms.fields')
            self.forms_mod = sys.modules.pop('django_stachoutils.forms')

    def tearDown(self):
        shutil.rmtree(self.tmp_media_root)
        sys.modules['django_stachoutils.forms.widgets'] = self.widgets_mod
        sys.modules['django_stachoutils.forms.fields'] = self.fields_mod
        sys.modules['django_stachoutils.forms'] = self.forms_mod

    def test_bound_image_model_choice_field_with_thumbor(self):
        from django_stachoutils.forms import ImageModelChoiceField

        class PersonForm(forms.ModelForm):
            house = ImageModelChoiceField(related_fieldname="photo",
                                          queryset=House.objects.all())

            class Meta:
                model = Person
                fields = ('name', 'lastname', 'gender', 'house')

        old_media_root = settings.MEDIA_ROOT
        with self.settings(MEDIA_ROOT=self.tmp_media_root):
            with open(os.path.join(old_media_root, "home_1.jpg"), mode="rb") as f:
                self.h1.photo.save("some pic", ImageFile(f))
            form = PersonForm({'name': 'Stan',
                               'lastname': 'Guerra',
                               'gender': 'male',
                               'house': self.h1.pk})
            self.assertHTMLEqual(
                form.as_table(),
                """
                <tr>
                  <th>
                    <label for="id_name">Name:</label>
                  </th>
                  <td>
                    <input type="text" name="name" value="Stan" required id="id_name" maxlength="100" />
                  </td>
                </tr>
                <tr>
                  <th><label for="id_lastname">Lastname:</label></th>
                  <td><input type="text" name="lastname" value="Guerra" required id="id_lastname" maxlength="100" /></td>
                </tr>
                <tr>
                  <th><label for="id_gender">Gender:</label></th>
                  <td>
                    <select name="gender" required id="id_gender">
                      <option value="">---------</option>
                      <option value="male" selected>Male</option>
                      <option value="female">Female</option>
                    </select>
                    <div class="droppableHiddenInput">
                      <input type="hidden" name="house" value="1" />
                      <div class="droppableContainer">
                        <span class="delete" title="Vider l'emplacement"></span>
                        <div class="droppable">
                          <div class="draggable">
                            <img src="http://my_thumbor.com:8888/dj6AHY7DZM35q5rrDngbOZhKp68=/120x0/http%3A//media.my_project.com/houses/12_rue_de_la_Paix_Paris.jpg" width="120">
                          </div>
                        </div>
                      </div>
                      <div class="message"></div>
                    </div>
                  </td>
                </tr>
                """.format()
            )
            self.assertTrue(form.is_valid())
            form.save()

            person = Person.objects.latest('pk')
            self.assertEqual(person.name, 'Stan')
            self.assertEqual(person.house, self.h1)
