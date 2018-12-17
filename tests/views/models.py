# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    purchased_on = models.DateField()
    for_sale = models.BooleanField(default=False)
    last_driver = models.ForeignKey('Person', null=True, blank=True)
    maintained_by = models.ForeignKey('Garage', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "cars/{}/".format(self.pk)

    def price_html(self):
        return u'<em>{}</em>€'.format(self.price)
    price_html.allow_tags = True
    price_html.short_description = 'price'
    price_html.ordering = ['price', 'name']


@python_2_unicode_compatible
class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    employed_by = models.ForeignKey('Company', null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


@python_2_unicode_compatible
class Company(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return self.short_name or self.name


class Garage(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('Person', null=True, blank=True)

    def __str__(self):
        return self.name
