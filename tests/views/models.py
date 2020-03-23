# -*- coding: utf-8 -*-

from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    purchased_on = models.DateField()
    for_sale = models.BooleanField(default=False)
    last_driver = models.ForeignKey('Person', on_delete=models.CASCADE, null=True, blank=True)
    maintained_by = models.ForeignKey('Garage', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "cars/{}/".format(self.pk)

    def price_html(self):
        return u'<em>{}</em>€'.format(self.price)
    price_html.allow_tags = True
    price_html.short_description = 'price'
    price_html.ordering = ['price', 'name']


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    employed_by = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Company(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.short_name or self.name


class Garage(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('Person', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
