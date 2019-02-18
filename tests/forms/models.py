from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=20)
    brand = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey('Person', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class CarOption(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    name = models.CharField(max_length=15)


class Person(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)
    house = models.ForeignKey('House', on_delete=models.CASCADE, null=True)


def house_photo_path(instance, filename):
    return 'houses/{}_{}.jpg'.format(instance.address, instance.city)


class House(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=house_photo_path, null=True)
