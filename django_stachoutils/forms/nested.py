# -*- coding: utf-8 -*-

from builtins import object
from django import forms
from django.forms.models import ModelFormMetaclass
from django.shortcuts import get_object_or_404
from future.utils import with_metaclass

NESTED_NON_FIELD_ERRORS = '__nested__'


class NestedModelFormOptions(object):
    def __init__(self, options=None):
        self.Form = getattr(options, 'form', None)  # Class.
        self.fk = getattr(options, 'fk', None)      # fk name.


class NestedModelFormMetaclass(ModelFormMetaclass):
    """ Ajoute les attributs self._nested.Form et self._nested.fk"""
    def __new__(cls, name, bases, attrs):
        new_class = super(NestedModelFormMetaclass, cls).__new__(cls, name, bases, attrs)
        # Declarez une class Nested.
        new_class._nested = NestedModelFormOptions(getattr(new_class, 'Nested', None))
        return new_class


class NestedModelForm(with_metaclass(NestedModelFormMetaclass, forms.ModelForm)):
    def __init__(self, *args, **kwargs):
        self.forms = []
        self.nested_form = None
        self._non_nested_errors = None
        nested_initial, nested_instance = {}, None
        if ('initial' in kwargs) and ('NESTED' in kwargs['initial']):
            nested_initial = kwargs['initial'].pop('NESTED')
        super(NestedModelForm, self).__init__(*args, **kwargs)
        # self.initial est un merge du paramètre 'initial' et des attrs de l'instance.
        nested_id = self.initial.get(self._nested.fk, None)
        # POST écrase initial si présent.
        if '%s-%s' % (self.prefix, self._nested.fk) in self.data:
            nested_id = self.data['%s-%s' % (self.prefix, self._nested.fk)]
        if nested_id:
            nested_instance = get_object_or_404(self._nested.Form.Meta.model, pk=nested_id)
        self._init_nested_form(nested_instance, nested_initial)

    def _init_nested_form(self, instance, initial):
        prefix = '%s_%s' % (self.prefix, self._nested.fk.upper())
        self.nested_form = self._nested.Form(self.data or None, self.files or None,
                                             prefix=prefix, initial=initial, instance=instance)
        self.forms.append(self.nested_form)

    def _get_errors(self):
        if self._errors is None:
            super(NestedModelForm, self).errors
            if not self.is_bound:  # Stop further processing.
                return self._errors
            if self.has_changed() or self.nested_form.has_changed():
                self.nested_form.empty_permitted = True
            nested_errors = self.nested_form.errors
            if nested_errors:
                self._errors[NESTED_NON_FIELD_ERRORS] = self.nested_form.non_field_errors()
        return self._errors
    errors = property(_get_errors)

    def _get_non_nested_errors(self):
        if self._non_nested_errors is None:
            self._non_nested_errors = self.errors.copy()
            if NESTED_NON_FIELD_ERRORS in self._non_nested_errors:
                del self._non_nested_errors[NESTED_NON_FIELD_ERRORS]
        return self._non_nested_errors
    non_nested_errors = property(_get_non_nested_errors)

    def has_changed(self, *args, **kwargs):
        nested_has_changed = self.nested_form.has_changed()
        host_has_changed = super(NestedModelForm, self).has_changed(*args, **kwargs)
        if host_has_changed or nested_has_changed:
            return True
        self.nested_form._errors = {}  # Why do we need to do that ? If not, next
        # call to errors (i.e. from the template) will revalidate and add errors although
        # It (the nested form) has not changed.
        return False

    def save(self, *args, **kwargs):
        instance = self.instance
        self.nested_instance = None
        if self.nested_form.has_changed():
            self.nested_instance = self.nested_form.save()
        instance = super(NestedModelForm, self).save(*args, **kwargs)
        if self.nested_instance:
            setattr(instance, self._nested.fk, self.nested_instance)
            instance.save()
        return instance
