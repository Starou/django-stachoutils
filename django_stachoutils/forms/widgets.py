# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from django.contrib.admin import widgets as admin_widgets


STATICS = {
    'js': [
        'django_stachoutils/js/jquery.charcounter.js',
        'django_stachoutils/js/jquery.fieldselection.js',
        'django_stachoutils/js/widgets.js',
    ]
}


class TexteEditeur(forms.Textarea):
    template_name = 'django_stachoutils/forms/widgets/texte_editeur.html'

    def _media(self):
        return forms.Media(**STATICS)
    media = property(_media)


class AdminTexteEditeur(admin_widgets.AdminTextareaWidget, TexteEditeur):
    pass


class TextareaCounter(AdminTexteEditeur):
    def __init__(self, max_signs=None, direction='up', attrs=None):
        self.max_signs = max_signs
        self.direction = direction
        super(TextareaCounter, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        textarea = super(TextareaCounter, self).render(name, value, attrs)
        jscounter = ''
        if self.max_signs:
            label = "signe(s)"
            if self.direction == 'down':
                label += ' restant(s)'
            jscounter = (
                '<script type="text/javascript">'
                    '$(document).ready(function () { '
                        '$("#%(id)s").charCounter(%(max_signs)d, {'
                              'container: "<div></div>",'
                              'direction: "%(direction)s",'
                              'format: "%%1 %(label)s",'
                              'limit: false,'
                              'limit_class: "error"'
                        '});'
                    '});'
                '</script>' % {
                    'id': attrs['id'],
                    'direction': self.direction,
                    'label': label,
                    'max_signs': self.max_signs})
        return mark_safe(textarea + jscounter)


class TextInputCounter(forms.TextInput):
    def __init__(self, max_signs=None, direction='up', attrs=None):
        self.max_signs = max_signs
        self.direction = direction
        super(TextInputCounter, self).__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        textinput = super(TextInputCounter, self).render(name, value, attrs)
        jscounter = ''
        if self.max_signs:
            label = "signe(s)"
            if self.direction == 'down':
                label += ' restant(s)'
            jscounter = (
                '<script type="text/javascript">'
                    '$(document).ready(function () { '
                        '$("#%(id)s").charCounter(%(max_signs)d, {'
                              'container: "<span></span>",'
                              'direction: "%(direction)s",'
                              'format: "%%1 %(label)s",'
                              'limit: false,'
                              'limit_class: "error"'
                        '});'
                    '});'
                '</script>' % {
                    'id': attrs['id'],
                    'direction': self.direction,
                    'label': label,
                    'max_signs': self.max_signs})
        return mark_safe(textinput + jscounter)

    def _media(self):
        return forms.Media(**STATICS)
    media = property(_media)
