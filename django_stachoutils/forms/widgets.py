# -*- coding: utf-8 -*-

from builtins import object
from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.utils.http import quote
from django.utils.safestring import mark_safe

if "django_thumbor" in settings.INSTALLED_APPS:
    from django_thumbor import generate_url
else:
    from django.template import Context, Template


STATICS = {
    'js': [
        'django_stachoutils/js/jquery.charcounter.js',
        'django_stachoutils/js/jquery.fieldselection.js',
        'django_stachoutils/js/editeur.js',
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


class ImageDroppableHiddenInput(forms.HiddenInput):
    def __init__(self, *args, **kwargs):
        super(ImageDroppableHiddenInput, self).__init__(*args, **kwargs)
        self.related_model, self.related_fieldname = None, None
        self.image_container_html = ''
        self.message = ''

    class Media(object):
        css = {
            'all': ('django_stachoutils/css/forms.css',)
        }
        js = ('django_stachoutils/js/forms.js',)

    def render(self, name, value, attrs=None, renderer=None):
        hidden_input = super(ImageDroppableHiddenInput, self).render(name, value, attrs=None)
        image_tag = '<img />'
        if value:
            rel_obj = self.related_model.objects.get(pk=value)  # TODO: Faire un get_object_or_none
            image_tag = self._get_thumbnail(rel_obj)

        tag = (
            '<div class="droppableHiddenInput">%s'
            '    <div class="droppableContainer"><span class="delete" title="Vider l\'emplacement"></span>%s'
            '        <div class="droppable"><div class="draggable">%s</div></div>'
            '    </div>'
            '    <div class="message">%s</div>'
            '</div>' % (hidden_input, self.image_container_html, image_tag, self.message)
        )
        return mark_safe(tag)

    def _get_thumbnail(self, rel_obj):
        image_field = getattr(rel_obj, self.related_fieldname)
        if "django_thumbor" in settings.INSTALLED_APPS:
            return get_thumbor_thumbnail_tag(image_field)
        else:
            t = Template('{% load thumbnail %}{% thumbnail img_field "120" as im %}<img src="{{ im.url }}"'
                         'width="{{ im.width }}" height="{{ im.height }}">{% endthumbnail %}')
            d = {"img_field": image_field}
            return mark_safe(t.render(Context(d)))


def get_thumbor_thumbnail_tag(image, width=120):
    return mark_safe('<img src="%s" width="%d">' % (
        get_thumbor_thumbnail_url(image, width=width),
        width))


def get_thumbor_thumbnail_url(image, **kwargs):
    storage = image.storage
    thumbor_server = settings.THUMBOR_SERVER_EXTERNAL
    url = quote(image.url)
    if hasattr(storage, "key"):
        try:
            url = storage.key(image.name)
        except NotImplementedError:
            pass
        else:
            thumbor_server = settings.THUMBOR_SERVER
    return generate_url(url, thumbor_server=thumbor_server, **kwargs)
