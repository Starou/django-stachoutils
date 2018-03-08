# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.utils.http import quote
from django.utils.safestring import mark_safe

if "django_thumbor" in settings.INSTALLED_APPS:
    from django_thumbor import generate_url
else:
    from django.template import Context, Template

from .models import ModelFormOptions, ModelFormMetaclass, ModelForm
from .nested import NestedModelFormOptions, NestedModelFormMetaclass, NestedModelForm


# TODO: Déplacer dans widgets.py.
class ImageDroppableHiddenInput(forms.HiddenInput):
    def __init__(self, *args, **kwargs):
        super(ImageDroppableHiddenInput, self).__init__(*args, **kwargs)
        self.related_model, self.related_fieldname = None, None
        self.image_container_html = ''
        self.message = ''

    class Media:
        css = {
            'all': ('django_stachoutils/css/forms.css',)
        }
        js = ('django_stachoutils/js/forms.js',)

    def render(self, name, value, attrs=None):
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


class ImageModelChoiceField(forms.ModelChoiceField):
    def __init__(self, related_fieldname, queryset, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = ImageDroppableHiddenInput
        super(ImageModelChoiceField, self).__init__(queryset, *args, **kwargs)
        self.widget.related_model = queryset.model
        self.widget.related_fieldname = related_fieldname

    def set_image_container_html(self, html):
        self.widget.image_container_html = html

    def set_message(self, html):
        self.widget.message = html
