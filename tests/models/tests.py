from django.test import TestCase
from django_stachoutils import models
from .models import Car, Person


class ModelsTestCase(TestCase):
    def test_get_obj_dict(self):
        person = Person.objects.create(name='Stan', lastname='Guerra', gender='male')
        car = Car.objects.create(brand='Saab', name='9.3', owner=person)
        self.assertEqual(models.get_obj_dict(car), {
            '_owner_cache': person,
            'brand': 'Saab',
            'description': None,
            'name': '9.3',
            'owner_id': person.pk}
        )
