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


class ModelFormTest(TestCase):
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
            """<input type="hidden" name="OPTIONS-TOTAL_FORMS" value="3" id="id_OPTIONS-TOTAL_FORMS" />
            <input type="hidden" name="OPTIONS-INITIAL_FORMS" value="0" id="id_OPTIONS-INITIAL_FORMS" />
            <input type="hidden" name="OPTIONS-MIN_NUM_FORMS" value="0" id="id_OPTIONS-MIN_NUM_FORMS" />
            <input type="hidden" name="OPTIONS-MAX_NUM_FORMS" value="1000" id="id_OPTIONS-MAX_NUM_FORMS" />"""
        )
        self.assertHTMLEqual(
            form.inlineformsets['options'].as_table(),
            """<input type="hidden" name="OPTIONS-TOTAL_FORMS" value="3" id="id_OPTIONS-TOTAL_FORMS" />
               <input type="hidden" name="OPTIONS-INITIAL_FORMS" value="0" id="id_OPTIONS-INITIAL_FORMS" />
               <input type="hidden" name="OPTIONS-MIN_NUM_FORMS" value="0" id="id_OPTIONS-MIN_NUM_FORMS" />
               <input type="hidden" name="OPTIONS-MAX_NUM_FORMS" value="1000" id="id_OPTIONS-MAX_NUM_FORMS" />
               <tr><th><label for="id_OPTIONS-0-name">Name:</label></th>
                   <td><input type="text" name="OPTIONS-0-name" id="id_OPTIONS-0-name" maxlength="15" /></td>
               </tr>
               <tr><th><label for="id_OPTIONS-0-DELETE">Delete:</label></th>
                   <td><input type="checkbox" name="OPTIONS-0-DELETE" id="id_OPTIONS-0-DELETE" />
                       <input type="hidden" name="OPTIONS-0-id" id="id_OPTIONS-0-id" />
                       <input type="hidden" name="OPTIONS-0-car" id="id_OPTIONS-0-car" />
                   </td>
               </tr>
               <tr>
                 <th><label for="id_OPTIONS-1-name">Name:</label></th>
                 <td><input type="text" name="OPTIONS-1-name" id="id_OPTIONS-1-name" maxlength="15" /></td>
              </tr>
              <tr>
                <th><label for="id_OPTIONS-1-DELETE">Delete:</label></th>
                <td><input type="checkbox" name="OPTIONS-1-DELETE" id="id_OPTIONS-1-DELETE" />
                    <input type="hidden" name="OPTIONS-1-id" id="id_OPTIONS-1-id" />
                    <input type="hidden" name="OPTIONS-1-car" id="id_OPTIONS-1-car" />
                </td>
              </tr>
              <tr>
                <th><label for="id_OPTIONS-2-name">Name:</label></th>
                <td><input type="text" name="OPTIONS-2-name" id="id_OPTIONS-2-name" maxlength="15" /></td>
              </tr>
              <tr>
                <th><label for="id_OPTIONS-2-DELETE">Delete:</label></th>
                <td><input type="checkbox" name="OPTIONS-2-DELETE" id="id_OPTIONS-2-DELETE" />
                    <input type="hidden" name="OPTIONS-2-id" id="id_OPTIONS-2-id" />
                    <input type="hidden" name="OPTIONS-2-car" id="id_OPTIONS-2-car" />
                </td>
              </tr>
            """
        )

    def test_model_form_not_valid(self):
        form = CarForm({
            'name': '9.3 2.0t',
            'OPTIONS-INITIAL_FORMS': '0',
            'OPTIONS-TOTAL_FORMS': '3',
            'OPTIONS-MIN_NUM_FORMS': '0',
            'OPTIONS-MAX_NUM_FORMS': '1000',
        })
        self.assertFalse(form.is_valid())

    def test_model_form_is_valid(self):
        form = CarForm({
            'name': '9.3 2.0t',
            'brand': 'Saab',
            'OPTIONS-INITIAL_FORMS': '0',
            'OPTIONS-TOTAL_FORMS': '3',
            'OPTIONS-MIN_NUM_FORMS': '0',
            'OPTIONS-MAX_NUM_FORMS': '1000',
        })
        self.assertTrue(form.is_valid())

    def test_model_form_with_inlines_not_valid(self):
        form = CarForm({
            'name': '900 Turbo 16',
            'brand': 'Saab',
            'OPTIONS-INITIAL_FORMS': '0',
            'OPTIONS-TOTAL_FORMS': '3',
            'OPTIONS-MIN_NUM_FORMS': '0',
            'OPTIONS-MAX_NUM_FORMS': '1000',
            'OPTIONS-0-name': 'Climatisation',
            'OPTIONS-1-name': 'Cruise-Control',
            'OPTIONS-2-name': 'Super extra audio sound system',
        })
        self.assertFalse(form.is_valid())

    def test_model_form_with_inlines_is_valid(self):
        form = CarForm({
            'name': '900 Turbo 16',
            'brand': 'Saab',
            'OPTIONS-INITIAL_FORMS': '0',
            'OPTIONS-TOTAL_FORMS': '3',
            'OPTIONS-MIN_NUM_FORMS': '0',
            'OPTIONS-MAX_NUM_FORMS': '1000',
            'OPTIONS-0-name': 'Climatisation',
            'OPTIONS-1-name': 'Cruise-Control',
            'OPTIONS-2-name': 'Sound system',
        })
        self.assertTrue(form.is_valid())

    def test_model_form_save(self):
        form = CarForm({
            'name': '9.3 2.0t',
            'brand': 'Saab',
            'OPTIONS-INITIAL_FORMS': '0',
            'OPTIONS-TOTAL_FORMS': '3',
            'OPTIONS-MIN_NUM_FORMS': '0',
            'OPTIONS-MAX_NUM_FORMS': '1000',
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
            'OPTIONS-INITIAL_FORMS': '0',
            'OPTIONS-TOTAL_FORMS': '3',
            'OPTIONS-MIN_NUM_FORMS': '0',
            'OPTIONS-MAX_NUM_FORMS': '1000',
        })
        self.assertTrue(form.has_changed())

    def test_model_form_save_with_inlines(self):
        form = CarForm({
            'name': '900 Turbo 16',
            'brand': 'Saab',
            'OPTIONS-INITIAL_FORMS': '0',
            'OPTIONS-TOTAL_FORMS': '3',
            'OPTIONS-MIN_NUM_FORMS': '0',
            'OPTIONS-MAX_NUM_FORMS': '1000',
            'OPTIONS-0-name': 'Climatisation',
            'OPTIONS-1-name': 'Cruise-Control',
            'OPTIONS-2-name': 'Alarm',
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
            'OPTIONS-INITIAL_FORMS': '3',
            'OPTIONS-TOTAL_FORMS': '3',
            'OPTIONS-MIN_NUM_FORMS': '0',
            'OPTIONS-MAX_NUM_FORMS': '1000',
            'OPTIONS-0-id': 1,
            'OPTIONS-0-name': 'Climatisation',
            'OPTIONS-1-id': 2,
            'OPTIONS-1-name': 'Cruise-Control',
            'OPTIONS-2-id': 3,
            'OPTIONS-2-name': 'Alarm',
        }, instance=my_car)
        self.assertFalse(form.has_changed())

        form = CarForm({
            'id': my_car.pk,
            'name': '900 Turbo 16',
            'brand': 'Saab',
            'OPTIONS-INITIAL_FORMS': '3',
            'OPTIONS-TOTAL_FORMS': '3',
            'OPTIONS-MIN_NUM_FORMS': '0',
            'OPTIONS-MAX_NUM_FORMS': '1000',
            'OPTIONS-0-id': 1,
            'OPTIONS-0-name': 'Air-conditioning',
            'OPTIONS-1-id': 2,
            'OPTIONS-1-name': 'Cruise-Control',
            'OPTIONS-2-id': 3,
            'OPTIONS-2-name': 'Alarm',
        }, instance=my_car)
        self.assertTrue(form.has_changed())


class PrefixedModelFormTest(TestCase):
    def test_render_model_form(self):
        form = CarForm(prefix="customer")
        self.maxDiff = None
        self.assertHTMLEqual(
            form.as_table(),
            """<tr>
                <th><label for="id_customer-name">Name:</label></th>
                <td><input type="text" name="customer-name" required id="id_customer-name" maxlength="20" /></td>
               </tr>
               <tr>
                 <th><label for="id_customer-brand">Brand:</label></th>
                 <td>
                   <input type="text" name="customer-brand" required id="id_customer-brand" maxlength="100" />
                   <input id="id_customer-pk" name="customer-pk" type="hidden" />
                 </td>
               </tr>"""
        )
        self.assertHTMLEqual(
            form.as_tr(),
            """<td>
                 <input type="text" name="customer-name" required id="id_customer-name" maxlength="20" />
               </td>
               <td>
                 <input type="text" name="customer-brand" required id="id_customer-brand" maxlength="100" />
               </td>
               <input id="id_customer-pk" name="customer-pk" type="hidden" /><span class="row_end" />"""
        )
        self.assertHTMLEqual(
            form.labels_as_tr(),
            """<tr><th><label for="id_customer-name">Name</label></th><th><label for="id_customer-brand">Brand</label></th></tr>"""
        )
        self.assertHTMLEqual(
            form.inlineformsets['options'].management_form.as_table(),
            """<input type="hidden" name="customer_OPTIONS-TOTAL_FORMS" value="3" id="id_customer_OPTIONS-TOTAL_FORMS" />
            <input type="hidden" name="customer_OPTIONS-INITIAL_FORMS" value="0" id="id_customer_OPTIONS-INITIAL_FORMS" />
            <input type="hidden" name="customer_OPTIONS-MIN_NUM_FORMS" value="0" id="id_customer_OPTIONS-MIN_NUM_FORMS" />
            <input type="hidden" name="customer_OPTIONS-MAX_NUM_FORMS" value="1000" id="id_customer_OPTIONS-MAX_NUM_FORMS" />"""
        )
        self.assertHTMLEqual(
            form.inlineformsets['options'].as_table(),
            """<input type="hidden" name="customer_OPTIONS-TOTAL_FORMS" value="3" id="id_customer_OPTIONS-TOTAL_FORMS" />
               <input type="hidden" name="customer_OPTIONS-INITIAL_FORMS" value="0" id="id_customer_OPTIONS-INITIAL_FORMS" />
               <input type="hidden" name="customer_OPTIONS-MIN_NUM_FORMS" value="0" id="id_customer_OPTIONS-MIN_NUM_FORMS" />
               <input type="hidden" name="customer_OPTIONS-MAX_NUM_FORMS" value="1000" id="id_customer_OPTIONS-MAX_NUM_FORMS" />
               <tr><th><label for="id_customer_OPTIONS-0-name">Name:</label></th>
                   <td><input type="text" name="customer_OPTIONS-0-name" id="id_customer_OPTIONS-0-name" maxlength="15" /></td>
               </tr>
               <tr><th><label for="id_customer_OPTIONS-0-DELETE">Delete:</label></th>
                   <td><input type="checkbox" name="customer_OPTIONS-0-DELETE" id="id_customer_OPTIONS-0-DELETE" />
                       <input type="hidden" name="customer_OPTIONS-0-id" id="id_customer_OPTIONS-0-id" />
                       <input type="hidden" name="customer_OPTIONS-0-car" id="id_customer_OPTIONS-0-car" />
                   </td>
               </tr>
               <tr>
                 <th><label for="id_customer_OPTIONS-1-name">Name:</label></th>
                 <td><input type="text" name="customer_OPTIONS-1-name" id="id_customer_OPTIONS-1-name" maxlength="15" /></td>
              </tr>
              <tr>
                <th><label for="id_customer_OPTIONS-1-DELETE">Delete:</label></th>
                <td><input type="checkbox" name="customer_OPTIONS-1-DELETE" id="id_customer_OPTIONS-1-DELETE" />
                    <input type="hidden" name="customer_OPTIONS-1-id" id="id_customer_OPTIONS-1-id" />
                    <input type="hidden" name="customer_OPTIONS-1-car" id="id_customer_OPTIONS-1-car" />
                </td>
              </tr>
              <tr>
                <th><label for="id_customer_OPTIONS-2-name">Name:</label></th>
                <td><input type="text" name="customer_OPTIONS-2-name" id="id_customer_OPTIONS-2-name" maxlength="15" /></td>
              </tr>
              <tr>
                <th><label for="id_customer_OPTIONS-2-DELETE">Delete:</label></th>
                <td><input type="checkbox" name="customer_OPTIONS-2-DELETE" id="id_customer_OPTIONS-2-DELETE" />
                    <input type="hidden" name="customer_OPTIONS-2-id" id="id_customer_OPTIONS-2-id" />
                    <input type="hidden" name="customer_OPTIONS-2-car" id="id_customer_OPTIONS-2-car" />
                </td>
              </tr>
            """
        )

    def test_model_form_not_valid(self):
        form = CarForm({
            'customer-name': '9.3 2.0t',
            'customer_OPTIONS-INITIAL_FORMS': '0',
            'customer_OPTIONS-TOTAL_FORMS': '3',
            'customer_OPTIONS-MIN_NUM_FORMS': '0',
            'customer_OPTIONS-MAX_NUM_FORMS': '1000',
        }, prefix="customer")
        self.assertFalse(form.is_valid())

    def test_model_form_is_valid(self):
        form = CarForm({
            'customer-name': '9.3 2.0t',
            'customer-brand': 'Saab',
            'customer_OPTIONS-INITIAL_FORMS': '0',
            'customer_OPTIONS-TOTAL_FORMS': '3',
            'customer_OPTIONS-MIN_NUM_FORMS': '0',
            'customer_OPTIONS-MAX_NUM_FORMS': '1000',
        }, prefix="customer")
        self.assertTrue(form.is_valid())

    def test_model_form_with_inlines_not_valid(self):
        form = CarForm({
            'customer-name': '900 Turbo 16',
            'customer-brand': 'Saab',
            'customer_OPTIONS-INITIAL_FORMS': '0',
            'customer_OPTIONS-TOTAL_FORMS': '3',
            'customer_OPTIONS-MIN_NUM_FORMS': '0',
            'customer_OPTIONS-MAX_NUM_FORMS': '1000',
            'customer_OPTIONS-0-name': 'Climatisation',
            'customer_OPTIONS-1-name': 'Cruise-Control',
            'customer_OPTIONS-2-name': 'Super extra audio sound system',
        }, prefix="customer")
        self.assertFalse(form.is_valid())

    def test_model_form_with_inlines_is_valid(self):
        form = CarForm({
            'customer-name': '900 Turbo 16',
            'customer-brand': 'Saab',
            'customer_OPTIONS-INITIAL_FORMS': '0',
            'customer_OPTIONS-TOTAL_FORMS': '3',
            'customer_OPTIONS-MIN_NUM_FORMS': '0',
            'customer_OPTIONS-MAX_NUM_FORMS': '1000',
            'customer_OPTIONS-0-name': 'Climatisation',
            'customer_OPTIONS-1-name': 'Cruise-Control',
            'customer_OPTIONS-2-name': 'Sound system',
        }, prefix="customer")
        self.assertTrue(form.is_valid())

    def test_model_form_save(self):
        form = CarForm({
            'customer-name': '9.3 2.0t',
            'customer-brand': 'Saab',
            'customer_OPTIONS-INITIAL_FORMS': '0',
            'customer_OPTIONS-TOTAL_FORMS': '3',
            'customer_OPTIONS-MIN_NUM_FORMS': '0',
            'customer_OPTIONS-MAX_NUM_FORMS': '1000',
        }, prefix="customer")
        form.save()
        my_car = Car.objects.latest('pk')
        self.assertEqual(my_car.brand, 'Saab')
        self.assertEqual(my_car.name, '9.3 2.0t')
        self.assertEqual(my_car.caroption_set.all().count(), 0)

        form = CarForm({
            'customer-id': my_car.pk,
            'customer-name': '900 Turbo 16',
            'customer-brand': 'Saab',
            'customer_OPTIONS-INITIAL_FORMS': '0',
            'customer_OPTIONS-TOTAL_FORMS': '3',
            'customer_OPTIONS-MIN_NUM_FORMS': '0',
            'customer_OPTIONS-MAX_NUM_FORMS': '1000',
        }, prefix="customer")
        self.assertTrue(form.has_changed())

    def test_model_form_save_with_inlines(self):
        form = CarForm({
            'customer-name': '900 Turbo 16',
            'customer-brand': 'Saab',
            'customer_OPTIONS-INITIAL_FORMS': '0',
            'customer_OPTIONS-TOTAL_FORMS': '3',
            'customer_OPTIONS-MIN_NUM_FORMS': '0',
            'customer_OPTIONS-MAX_NUM_FORMS': '1000',
            'customer_OPTIONS-0-name': 'Climatisation',
            'customer_OPTIONS-1-name': 'Cruise-Control',
            'customer_OPTIONS-2-name': 'Alarm',
        }, prefix="customer")
        form.save()
        my_car = Car.objects.latest('pk')
        self.assertEqual(my_car.brand, 'Saab')
        self.assertEqual(my_car.name, '900 Turbo 16')
        self.assertEqual(my_car.caroption_set.all().count(), 3)

        form = CarForm({
            'customer-id': my_car.pk,
            'customer-name': '900 Turbo 16',
            'customer-brand': 'Saab',
            'customer_OPTIONS-INITIAL_FORMS': '3',
            'customer_OPTIONS-TOTAL_FORMS': '3',
            'customer_OPTIONS-MIN_NUM_FORMS': '0',
            'customer_OPTIONS-MAX_NUM_FORMS': '1000',
            'customer_OPTIONS-0-id': 1,
            'customer_OPTIONS-0-name': 'Climatisation',
            'customer_OPTIONS-1-id': 2,
            'customer_OPTIONS-1-name': 'Cruise-Control',
            'customer_OPTIONS-2-id': 3,
            'customer_OPTIONS-2-name': 'Alarm',
        }, prefix="customer", instance=my_car)
        self.assertFalse(form.has_changed())

        form = CarForm({
            'customer-id': my_car.pk,
            'customer-name': '900 Turbo 16',
            'customer-brand': 'Saab',
            'customer_OPTIONS-INITIAL_FORMS': '3',
            'customer_OPTIONS-TOTAL_FORMS': '3',
            'customer_OPTIONS-MIN_NUM_FORMS': '0',
            'customer_OPTIONS-MAX_NUM_FORMS': '1000',
            'customer_OPTIONS-0-id': 1,
            'customer_OPTIONS-0-name': 'Air-conditioning',
            'customer_OPTIONS-1-id': 2,
            'customer_OPTIONS-1-name': 'Cruise-Control',
            'customer_OPTIONS-2-id': 3,
            'customer_OPTIONS-2-name': 'Alarm',
        }, prefix="customer" , instance=my_car)
        self.assertTrue(form.has_changed())
