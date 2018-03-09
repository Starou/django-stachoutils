# -*- coding: utf-8 -*-

from django import forms
from django.test import TestCase
from django_stachoutils.forms import ImageModelChoiceField

from .models import House, Person


class PersonForm(forms.ModelForm):
    house = ImageModelChoiceField(related_fieldname="photo",
                                  queryset=House.objects.all())

    class Meta:
        model = Person
        fields = ('name', 'lastname', 'gender', 'house')


class FieldsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.h1 = House.objects.create(address="12, rue de la Paix", city="Paris")
        cls.h2 = House.objects.create(address="4, rue du Cherche-Midi", city="Paris")

    def test_render_image_model_choice_field(self):
        form = PersonForm()
        self.assertHTMLEqual(
            form.as_table(),
            """
            <tr>
              <th><label for="id_name">Name:</label></th>
              <td><input type="text" name="name" required id="id_name" maxlength="100" /></td>
            </tr>
            <tr>
              <th><label for="id_lastname">Lastname:</label></th>
              <td><input type="text" name="lastname" required id="id_lastname" maxlength="100" /></td>
            </tr>
            <tr>
              <th><label for="id_gender">Gender:</label></th>
              <td>
                <select name="gender" required id="id_gender">
                  <option value="" selected>---------</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                </select>
                <div class="droppableHiddenInput">
                  <input type="hidden" name="house" />
                  <div class="droppableContainer">
                    <span class="delete" title="Vider l'emplacement"></span>
                    <div class="droppable">
                      <div class="draggable"><img /></div>
                    </div>
                  </div>
                  <div class="message"></div>
                </div>
              </td>
            </tr>
            """
        )

    def test_bound_image_model_choice_field(self):
        form = PersonForm({'name': 'Stan',
                           'lastname': 'Guerra',
                           'gender': 'male'})
        self.assertFalse(form.is_valid())

        form = PersonForm({'name': 'Stan',
                           'lastname': 'Guerra',
                           'gender': 'male',
                           'house': self.h1.pk})
        self.assertTrue(form.is_valid())
        form.save()

        person = Person.objects.latest('pk')
        self.assertEqual(person.name, 'Stan')
        self.assertEqual(person.house, self.h1)
