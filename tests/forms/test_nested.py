# -*- coding: utf-8 -*-

from django import forms
from django.test import TestCase

from django_stachoutils.forms import NestedModelForm
from .models import Car, Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'lastname', 'gender')


class CarForm(NestedModelForm):
    owner = forms.ModelChoiceField(queryset=Person.objects.all(),
                                   initial=None, required=False,
                                   widget=forms.HiddenInput())
    class Meta:
        model = Car
        fields = ('name', 'brand', 'owner')

    class Nested:
        form = PersonForm
        fk = 'owner'


class NestedModelFormTest(TestCase):
    def test_render_nested_model_form(self):
        form = CarForm()
        self.assertHTMLEqual(
            form.as_table(),
            """
            <tr>
              <th><label for="id_name">Name:</label></th>
              <td><input type="text" name="name" required id="id_name" maxlength="20" /></td>
            </tr>
            <tr>
              <th><label for="id_brand">Brand:</label></th>
              <td>
                <input type="text" name="brand" required id="id_brand" maxlength="100" />
                <input id="id_owner" name="owner" type="hidden" />
              </td>
            </tr>
            """
        )
        self.assertHTMLEqual(
            form.nested_form.as_table(),
            """
            <tr>
              <th><label for="id_None_OWNER-name">Name:</label></th>
              <td><input type="text" name="None_OWNER-name" required id="id_None_OWNER-name" maxlength="100" /></td>
            </tr>
            <tr>
              <th><label for="id_None_OWNER-lastname">Lastname:</label></th>
              <td><input type="text" name="None_OWNER-lastname" required id="id_None_OWNER-lastname" maxlength="100" /></td>
            </tr>
            <tr>
              <th><label for="id_None_OWNER-gender">Gender:</label></th>
              <td><select name="None_OWNER-gender" required id="id_None_OWNER-gender">
                    <option value="" selected>---------</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                  </select>
              </td>
            </tr>
            """
        )

    def test_bound_nested_model_form(self):
        form = CarForm({
            'name': '9.3 2.0t',
            'brand': 'Saab',
            'owner': '',
        })
        self.assertTrue(form.is_valid())
        form.save()
        my_car = Car.objects.latest('pk')
        self.assertEqual(my_car.brand, 'Saab')
        self.assertEqual(my_car.name, '9.3 2.0t')

        # Data hasn't changed.
        form = CarForm({
            'name': '9.3 2.0t',
            'brand': 'Saab',
            'owner': '',
        }, instance=my_car)
        self.assertFalse(form.has_changed())

        # Data has changed.
        form = CarForm({
            'name': '9.3 2.0T Biopower',
            'brand': 'Saab',
            'owner': '',
        }, instance=my_car)
        self.assertTrue(form.has_changed())

        form.save()
        my_car = Car.objects.get(pk=my_car.pk)
        self.assertEqual(my_car.brand, 'Saab')
        self.assertEqual(my_car.name, '9.3 2.0T Biopower')

        # With nested data.
        form = CarForm({
            'name': '900 Turbo 16',
            'brand': 'Saab',
            'owner': '',
            'None_OWNER-name': 'Stan',
            'None_OWNER-lastname': 'Guerra',
            'None_OWNER-gender': 'male',
        })
        self.assertTrue(form.is_valid())
        form.save()
        my_car = Car.objects.latest('pk')
        self.assertEqual(my_car.brand, 'Saab')
        self.assertEqual(my_car.name, '900 Turbo 16')
        self.assertEqual(my_car.owner.name, 'Stan')

    def test_bound_nested_model_form_with_invalid_data(self):
        form = CarForm({
            'name': 'Nine Three Two-liters Turbocharged',
            'brand': 'Saab',
            'owner': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.non_nested_errors, {'name':['Ensure this value has at most 20 characters (it has 34).']})

    def test_prefixed_bound_nested_model_form(self):
        form = CarForm({
            'car-name': '9.3 2.0t',
            'car-brand': 'Saab',
            'car-owner': '',
        }, prefix='car')
        self.assertTrue(form.is_valid())
        form.save()
        my_car = Car.objects.latest('pk')
        self.assertEqual(my_car.brand, 'Saab')
        self.assertEqual(my_car.name, '9.3 2.0t')

        form = CarForm({
            'car-name': '900 Turbo 16',
            'car-brand': 'Saab',
            'car-owner': '',
            'car_OWNER-name': 'Stan',
            'car_OWNER-lastname': 'Guerra',
            'car_OWNER-gender': 'male',
        }, prefix='car')
        self.assertTrue(form.is_valid())
        form.save()
        my_car = Car.objects.latest('pk')
        self.assertEqual(my_car.brand, 'Saab')
        self.assertEqual(my_car.name, '900 Turbo 16')
        self.assertEqual(my_car.owner.name, 'Stan')
