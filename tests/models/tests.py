from django.test import TestCase
from django import VERSION as DJ_VERSION
from django_stachoutils import models
from .models import Car, Person


class ModelsTest(TestCase):
    def test_get_obj_dict(self):
        person = Person.objects.create(name='Stan', lastname='Guerra', gender='male')
        car = Car.objects.create(brand='Saab', name='9.3', owner=person)
        expected = {
            'brand': 'Saab',
            'description': None,
            'name': '9.3',
            'owner_id': person.pk
        }
        if DJ_VERSION < (2, 0):
            expected['_owner_cache'] = person

        self.assertEqual(models.get_obj_dict(car), expected)
