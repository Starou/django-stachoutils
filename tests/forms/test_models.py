# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import inlineformset_factory
from django.test import TestCase

from django_stachoutils.forms import ModelForm
from .models import Car, CarOption


CarOptionFormSet = inlineformset_factory(Car, CarOption, fields=['name'])


class CarForm(ModelForm):
    pk = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Car
        fields = ('name', 'brand')

    class Forms:
        inlines = {
            'options': CarOptionFormSet
        }


class ModelFormTestCase(TestCase):
    def test_render_model_form(self):
        form = CarForm()
        self.assertHTMLEqual(
            form.as_table(),
            """<tr>
                <th><label for="id_name">Name:</label></th>
                <td><input type="text" name="name" required id="id_name" maxlength="20" /></td>
               </tr>
               <tr>
                 <th><label for="id_brand">Brand:</label></th>
                 <td>
                   <input type="text" name="brand" required id="id_brand" maxlength="100" />
                   <input id="id_pk" name="pk" type="hidden" />
                 </td>
               </tr>"""
        )
        self.assertHTMLEqual(
            form.as_tr(),
            """<td>
                 <input type="text" name="name" required id="id_name" maxlength="20" />
               </td>
               <td>
                 <input type="text" name="brand" required id="id_brand" maxlength="100" />
               </td>
               <input id="id_pk" name="pk" type="hidden" /><span class="row_end" />"""
        )
        self.assertHTMLEqual(
            form.labels_as_tr(),
            """<tr><th><label for="id_name">Name</label></th><th><label for="id_brand">Brand</label></th></tr>"""
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
                   <td><input type="text" name="None_OPTIONS-0-name" id="id_None_OPTIONS-0-name" maxlength="15" /></td>
               </tr>
               <tr><th><label for="id_None_OPTIONS-0-DELETE">Delete:</label></th>
                   <td><input type="checkbox" name="None_OPTIONS-0-DELETE" id="id_None_OPTIONS-0-DELETE" />
                       <input type="hidden" name="None_OPTIONS-0-id" id="id_None_OPTIONS-0-id" />
                       <input type="hidden" name="None_OPTIONS-0-car" id="id_None_OPTIONS-0-car" />
                   </td>
               </tr>
               <tr>
                 <th><label for="id_None_OPTIONS-1-name">Name:</label></th>
                 <td><input type="text" name="None_OPTIONS-1-name" id="id_None_OPTIONS-1-name" maxlength="15" /></td>
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
                <td><input type="text" name="None_OPTIONS-2-name" id="id_None_OPTIONS-2-name" maxlength="15" /></td>
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

    def test_model_form_not_valid(self):
        form = CarForm({
            'name': '9.3 2.0t',
            'None_OPTIONS-INITIAL_FORMS': '0',
            'None_OPTIONS-TOTAL_FORMS': '3',
            'None_OPTIONS-MIN_NUM_FORMS': '0',
            'None_OPTIONS-MAX_NUM_FORMS': '1000',
        })
        self.assertFalse(form.is_valid())

    def test_model_form_is_valid(self):
        form = CarForm({
            'name': '9.3 2.0t',
            'brand': 'Saab',
            'None_OPTIONS-INITIAL_FORMS': '0',
            'None_OPTIONS-TOTAL_FORMS': '3',
            'None_OPTIONS-MIN_NUM_FORMS': '0',
            'None_OPTIONS-MAX_NUM_FORMS': '1000',
        })
        self.assertTrue(form.is_valid())

    def test_model_form_with_inlines_not_valid(self):
        form = CarForm({
            'name': '900 Turbo 16',
            'brand': 'Saab',
            'None_OPTIONS-INITIAL_FORMS': '0',
            'None_OPTIONS-TOTAL_FORMS': '3',
            'None_OPTIONS-MIN_NUM_FORMS': '0',
            'None_OPTIONS-MAX_NUM_FORMS': '1000',
            'None_OPTIONS-0-name': 'Climatisation',
            'None_OPTIONS-1-name': 'Cruise-Control',
            'None_OPTIONS-2-name': 'Super extra audio sound system',
        })
        self.assertFalse(form.is_valid())

    def test_model_form_with_inlines_is_valid(self):
        form = CarForm({
            'name': '900 Turbo 16',
            'brand': 'Saab',
            'None_OPTIONS-INITIAL_FORMS': '0',
            'None_OPTIONS-TOTAL_FORMS': '3',
            'None_OPTIONS-MIN_NUM_FORMS': '0',
            'None_OPTIONS-MAX_NUM_FORMS': '1000',
            'None_OPTIONS-0-name': 'Climatisation',
            'None_OPTIONS-1-name': 'Cruise-Control',
            'None_OPTIONS-2-name': 'Sound system',
        })
        self.assertTrue(form.is_valid())

    def test_model_form_save(self):
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
            'id': my_car.pk,
            'name': '900 Turbo 16',
            'brand': 'Saab',
            'None_OPTIONS-INITIAL_FORMS': '0',
            'None_OPTIONS-TOTAL_FORMS': '3',
            'None_OPTIONS-MIN_NUM_FORMS': '0',
            'None_OPTIONS-MAX_NUM_FORMS': '1000',
        })
        self.assertTrue(form.has_changed())

    def test_model_form_save_with_inlines(self):
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

        form = CarForm({
            'id': my_car.pk,
            'name': '900 Turbo 16',
            'brand': 'Saab',
            'None_OPTIONS-INITIAL_FORMS': '3',
            'None_OPTIONS-TOTAL_FORMS': '3',
            'None_OPTIONS-MIN_NUM_FORMS': '0',
            'None_OPTIONS-MAX_NUM_FORMS': '1000',
            'None_OPTIONS-0-id': 1,
            'None_OPTIONS-0-name': 'Climatisation',
            'None_OPTIONS-1-id': 2,
            'None_OPTIONS-1-name': 'Cruise-Control',
            'None_OPTIONS-2-id': 3,
            'None_OPTIONS-2-name': 'Alarm',
        }, instance=my_car)
        self.assertFalse(form.has_changed())

        form = CarForm({
            'id': my_car.pk,
            'name': '900 Turbo 16',
            'brand': 'Saab',
            'None_OPTIONS-INITIAL_FORMS': '3',
            'None_OPTIONS-TOTAL_FORMS': '3',
            'None_OPTIONS-MIN_NUM_FORMS': '0',
            'None_OPTIONS-MAX_NUM_FORMS': '1000',
            'None_OPTIONS-0-id': 1,
            'None_OPTIONS-0-name': 'Air-conditioning',
            'None_OPTIONS-1-id': 2,
            'None_OPTIONS-1-name': 'Cruise-Control',
            'None_OPTIONS-2-id': 3,
            'None_OPTIONS-2-name': 'Alarm',
        }, instance=my_car)
        self.assertTrue(form.has_changed())
