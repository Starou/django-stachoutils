from django.db import models
from django_stachoutils.storage import OverwriteStorage


def car_photo_path(instance, filename):
    return 'cars/{}_{}.jpg'.format(instance.brand, instance.name)


class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=car_photo_path, storage=OverwriteStorage(), null=True)

    def __str__(self):
        return self.name
