# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import flatatt
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.contrib.admin import widgets as admin_widgets


BUTTONS = [{'class': 'gras', 'text': u'Gras', 'accesskey': 'g'},
           {'class': 'sup', 'text': u'Supérieur', 'accesskey': 's'},
           {'class': 'bas', 'text': u'Bas de casse', 'accesskey': 'b'}]

STATICS = {'js': ['django_stachoutils/js/jquery.charcounter.js',
                  'django_stachoutils/js/jquery.fieldselection.js',
                  'django_stachoutils/js/widgets.js']}


class TexteEditeur(forms.Textarea):
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        html = []
        html.append(u'<div class="editeur"><div class="toolbar">')
        for button in BUTTONS:
            html.append(u'<button type="button" accesskey="%(accesskey)s" class="%(class)s">%(text)s</button>' % button)
        html.append(u'</div>')
        html.append(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                                                    conditional_escape(force_unicode(value))))
        html.append(u'</div>')
        return mark_safe(u'\n'.join(html))

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

    def render(self, name, value, attrs=None):
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

    def render(self, name, value, attrs=None):
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
