# -*- coding: utf-8 -*-

from builtins import str
from django import forms
from django import VERSION as DJ_VERSION
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.test import RequestFactory, TestCase

from django_stachoutils import options
from .models import Car, CarOption


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('name', 'brand')


class LogsTest(TestCase):
    rf = RequestFactory()
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def setUp(self):
        self.request = self.rf.get('/')
        self.request.user = self.user

    def test_log_addition(self):
        car = Car.objects.create(brand='Saab', name='9-3')
        options.log_addition(self.request, car)

        log = LogEntry.objects.latest('pk')
        self.assertTrue(log.is_addition())
        self.assertEqual(log.object_repr, u'9-3')
        self.assertEqual(log.object_id, str(car.pk))
        self.assertEqual(log.user_id, self.user.pk)

    def test_log_change(self):
        car = Car.objects.create(brand='Saab', name='9-3')
        car.name = '9-3t Biopower'
        options.log_change(self.request, car, "Fixed the name of the damned car")

        log = LogEntry.objects.latest('pk')
        self.assertTrue(log.is_change())
        self.assertEqual(log.object_repr, u'9-3t Biopower')
        self.assertEqual(log.object_id, str(car.pk))
        self.assertEqual(log.user_id, self.user.pk)

    def test_log_deletion(self):
        car = Car.objects.create(brand='Saab', name='9-3')
        options.log_deletion(self.request, car, str(car))

        log = LogEntry.objects.latest('pk')
        self.assertTrue(log.is_deletion())
        self.assertEqual(log.object_repr, u'9-3')
        self.assertEqual(log.object_id, str(car.pk))
        self.assertEqual(log.user_id, self.user.pk)

    def test_log_change_for_user(self):
        car = Car.objects.create(brand='Saab', name='9-3')
        car.name = '9-3t Biopower'
        options.log_change_for_user(self.user, car, "Fixed the name of the damned car")

        log = LogEntry.objects.latest('pk')
        self.assertTrue(log.is_change())
        self.assertEqual(log.object_repr, u'9-3t Biopower')
        self.assertEqual(log.object_id, str(car.pk))
        self.assertEqual(log.user_id, self.user.pk)

    def test_logs_for_forms(self):
        # Addition
        form = CarForm({
            'name': '9.3 2.0t',
            'brand': 'Saab',
        })
        car = form.save()
        options.logs_for_formsets('addition', self.request, car, [form])
        log = LogEntry.objects.latest('pk')
        self.assertTrue(log.is_addition())
        self.assertEqual(log.user, self.user)
        if DJ_VERSION >= (3, 0):
            self.assertEqual(str(log), 'Added “9.3 2.0t”.')
        else:
            self.assertEqual(str(log), 'Added "9.3 2.0t".')

        # Modification
        form = CarForm({
            'id': car.pk,
            'name': '900 Turbo 16',
            'brand': 'Saab',
        }, instance=car)
        car = form.save()
        options.logs_for_formsets('change', self.request, car, [form])
        log = LogEntry.objects.latest('pk')
        self.assertFalse(log.is_addition())
        self.assertEqual(log.user, self.user)
        if DJ_VERSION >= (3, 0):
            self.assertEqual(str(log), u'Changed “900 Turbo 16” — a modifié : name (car [900 Turbo 16]) ; ')
        else:
            self.assertEqual(str(log), u'Changed "900 Turbo 16" - a modifié : name (car [900 Turbo 16]) ; ')

    def test_logs_for_formsets(self):
        car = Car.objects.create(brand='Lada', name='Niva')

        CarOptionFormSet = inlineformset_factory(Car, CarOption, fields=['name'])
        formset = CarOptionFormSet({
            'caroption_set-INITIAL_FORMS': '0',
            'caroption_set-TOTAL_FORMS': '1',
            'caroption_set-MIN_NUM_FORMS': '0',
            'caroption_set-MAX_NUM_FORMS': '10',
            'caroption_set-0-id': '',
            'caroption_set-0-car': car.pk,
            'caroption_set-0-name': 'BVA',
            'caroption_set-0-DELETE': '',
        }, instance=car)
        formset.is_valid()
        formset.save()

        options.logs_for_formsets('change', self.request, car, [formset])
        log = LogEntry.objects.latest('pk')
        self.assertEqual(log.change_message, u'a modifié : name (car option [BVA]) ; ')
