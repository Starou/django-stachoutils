# -*- coding: utf-8 -*-

from builtins import str
from django import forms
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase

from django_stachoutils import options
from .models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('name', 'brand')


class LogsForFormsetTestCase(TestCase):
    def test_logs_for_formsets(self):
        rf = RequestFactory()
        request = rf.get('/')
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        request.user = user

        # Addition
        form = CarForm({
            'name': '9.3 2.0t',
            'brand': 'Saab',
        })
        car = form.save()
        options.logs_for_formsets('addition', request, car, [form])
        log = LogEntry.objects.latest('pk')
        self.assertTrue(log.is_addition())
        self.assertEqual(log.user, user)
        self.assertEqual(str(log), 'Added "9.3 2.0t".')

        # Modification
        form = CarForm({
            'id': car.pk,
            'name': '900 Turbo 16',
            'brand': 'Saab',
        }, instance=car)
        car = form.save()
        options.logs_for_formsets('change', request, car, [form])
        log = LogEntry.objects.latest('pk')
        self.assertFalse(log.is_addition())
        self.assertEqual(log.user, user)
        self.assertEqual(str(log), u'Changed "900 Turbo 16" - a modifié : name (car [900 Turbo 16]) ; ')
