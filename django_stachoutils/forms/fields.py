# -*- coding: utf-8 -*-

from django import forms
from .widgets import ImageDroppableHiddenInput


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
