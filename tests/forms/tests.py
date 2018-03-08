# -*- coding: utf-8 -*-

from django.forms.models import inlineformset_factory
from django.test import TestCase

from django_stachoutils.forms import ModelForm
from .models import Car, CarOption


CarOptionFormSet = inlineformset_factory(Car, CarOption, fields=['name'])


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ('name', 'brand')

    class Forms:
        inlines = {
            'options': CarOptionFormSet
        }


class ModelFormTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ModelFormTestCase, cls).setUpClass()


    @classmethod
    def setUpTestData(cls):
        pass

    def test_render_model_form(self):
        form = CarForm()
        self.assertHTMLEqual(
            form.as_table(),
            """<tr><th><label for="id_name">Name:</label></th>
                   <td><input type="text" name="name" required id="id_name" maxlength="100" /></td></tr>
               <tr><th><label for="id_brand">Brand:</label></th>
                   <td><input type="text" name="brand" required id="id_brand" maxlength="100" /></td></tr>"""
        )
        self.assertHTMLEqual(
            form.inlineformsets['options'].management_form.as_table(),
            """<input type="hidden" name="None_OPTIONS-TOTAL_FORMS" value="3" id="id_None_OPTIONS-TOTAL_FORMS" />
            <input type="hidden" name="None_OPTIONS-INITIAL_FORMS" value="0" id="id_None_OPTIONS-INITIAL_FORMS" />
            <input type="hidden" name="None_OPTIONS-MIN_NUM_FORMS" value="0" id="id_None_OPTIONS-MIN_NUM_FORMS" />
            <input type="hidden" name="None_OPTIONS-MAX_NUM_FORMS" value="1000" id="id_None_OPTIONS-MAX_NUM_FORMS" />"""
        )
        self.assertHTMLEqual(
            form.inlineformsets['options'].as_table(),
            """<input type="hidden" name="None_OPTIONS-TOTAL_FORMS" value="3" id="id_None_OPTIONS-TOTAL_FORMS" />
               <input type="hidden" name="None_OPTIONS-INITIAL_FORMS" value="0" id="id_None_OPTIONS-INITIAL_FORMS" />
               <input type="hidden" name="None_OPTIONS-MIN_NUM_FORMS" value="0" id="id_None_OPTIONS-MIN_NUM_FORMS" />
               <input type="hidden" name="None_OPTIONS-MAX_NUM_FORMS" value="1000" id="id_None_OPTIONS-MAX_NUM_FORMS" />
               <tr><th><label for="id_None_OPTIONS-0-name">Name:</label></th>
                   <td><input type="text" name="None_OPTIONS-0-name" id="id_None_OPTIONS-0-name" maxlength="100" /></td>
               </tr>
               <tr><th><label for="id_None_OPTIONS-0-DELETE">Delete:</label></th>
                   <td><input type="checkbox" name="None_OPTIONS-0-DELETE" id="id_None_OPTIONS-0-DELETE" />
                       <input type="hidden" name="None_OPTIONS-0-id" id="id_None_OPTIONS-0-id" />
                       <input type="hidden" name="None_OPTIONS-0-car" id="id_None_OPTIONS-0-car" />
                   </td>
               </tr>
               <tr>
                 <th><label for="id_None_OPTIONS-1-name">Name:</label></th>
                 <td><input type="text" name="None_OPTIONS-1-name" id="id_None_OPTIONS-1-name" maxlength="100" /></td>
              </tr>
              <tr>
                <th><label for="id_None_OPTIONS-1-DELETE">Delete:</label></th>
                <td><input type="checkbox" name="None_OPTIONS-1-DELETE" id="id_None_OPTIONS-1-DELETE" />
                    <input type="hidden" name="None_OPTIONS-1-id" id="id_None_OPTIONS-1-id" />
                    <input type="hidden" name="None_OPTIONS-1-car" id="id_None_OPTIONS-1-car" />
                </td>
              </tr>
              <tr>
                <th><label for="id_None_OPTIONS-2-name">Name:</label></th>
                <td><input type="text" name="None_OPTIONS-2-name" id="id_None_OPTIONS-2-name" maxlength="100" /></td>
              </tr>
              <tr>
                <th><label for="id_None_OPTIONS-2-DELETE">Delete:</label></th>
                <td><input type="checkbox" name="None_OPTIONS-2-DELETE" id="id_None_OPTIONS-2-DELETE" />
                    <input type="hidden" name="None_OPTIONS-2-id" id="id_None_OPTIONS-2-id" />
                    <input type="hidden" name="None_OPTIONS-2-car" id="id_None_OPTIONS-2-car" />
                </td>
              </tr>
            """
        )

    def test_bound_model_form(self):
        form = CarForm({
            'name': '9.3 2.0t',
            'brand': 'Saab',
            'None_OPTIONS-INITIAL_FORMS': '0',
            'None_OPTIONS-TOTAL_FORMS': '3',
            'None_OPTIONS-MIN_NUM_FORMS': '0',
            'None_OPTIONS-MAX_NUM_FORMS': '1000',
        })
        form.save()
        my_car = Car.objects.latest('pk')
        self.assertEqual(my_car.brand, 'Saab')
        self.assertEqual(my_car.name, '9.3 2.0t')
        self.assertEqual(my_car.caroption_set.all().count(), 0)

        form = CarForm({
            'name': '900 Turbo 16',
            'brand': 'Saab',
            'None_OPTIONS-INITIAL_FORMS': '0',
            'None_OPTIONS-TOTAL_FORMS': '3',
            'None_OPTIONS-MIN_NUM_FORMS': '0',
            'None_OPTIONS-MAX_NUM_FORMS': '1000',
            'None_OPTIONS-0-name': 'Climatisation',
            'None_OPTIONS-1-name': 'Cruise-Control',
            'None_OPTIONS-2-name': 'Alarm',
        })
        form.save()
        my_car = Car.objects.latest('pk')
        self.assertEqual(my_car.brand, 'Saab')
        self.assertEqual(my_car.name, '900 Turbo 16')
        self.assertEqual(my_car.caroption_set.all().count(), 3)

