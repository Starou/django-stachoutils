from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    owner = models.ForeignKey('Person', null=True)

    def __str__(self):
        return self.name


class CarOption(models.Model):
    car = models.ForeignKey('Car')
    name = models.CharField(max_length=100)


class Person(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)
