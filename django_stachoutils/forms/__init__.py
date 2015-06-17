# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from django.forms.models import ModelFormMetaclass


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


class NestedModelForm(forms.ModelForm):
    __metaclass__ = NestedModelFormMetaclass

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


# http://djangosnippets.org/snippets/2248/

class ModelFormOptions(object):
    def __init__(self, options=None):
        self.inlines = getattr(options, 'inlines', {})


class ModelFormMetaclass(ModelFormMetaclass):
    """ Ajoute les attributs self._forms.inlines """
    def __new__(cls, name, bases, attrs):
        new_class = super(ModelFormMetaclass, cls).__new__(cls, name, bases, attrs)
        new_class._forms = ModelFormOptions(getattr(new_class, 'Forms', None))
        return new_class


class ModelForm(forms.ModelForm):
    """
    Add to ModelForm the ability to declare inline formsets.

    It save you from the boiler-plate implementation of cross validation/saving of such forms
    in the views.
    You should use It in the admin's forms if you need the inherit them in your apps because
    there is not multi-inherance.

    >>> from myapp import models
    >>> class Program(models.Model):
    ...     name = models.CharField(max_length=100, blank=True)

    >>> class ImageProgram(models.Model):
    ...     image = models.ImageField('image')
    ...     program = models.ForeignKey(Program)

    >>> class Ringtone(models.Model):
    ...     sound = models.FileField('sound')
    ...     program = models.ForeignKey(Program)

    Use It in your admin.py instead of django.forms.ModelForm:
    >>> class ProgramAdminForm(ModelForm):
    ...     class Meta:
    ...         model = Program
    ...         def clean(self):
    ...             cleaned_data = self.cleaned_data
    ...             # stuff
    ...             return cleaned_data

    In your app, say you declare the following inline formsets:
    >>> from django.forms.models import inlineformset_factory
    >>> from myapp.forms import ImageProgramForm, RingtoneProgramForm
    >>> ImageProgramFormSet = inlineformset_factory(models.Program, models.ImageProgram,
    ...                                             form=ImageProgramForm, max_num=6)
    >>> RingToneFormSet = inlineformset_factory(models.Program, models.RingTone,
    ...                                         form=RingtoneProgramForm)

    You can bind them in your program's form:
    >>> class MyProgramForm(ProgramAdminForm):
    ...     class Forms:
    ...         inlines = {
    ...             'images': ImageProgramFormSet,
    ...             'ringtones': RingToneFormSet,
    ...         }

    And instanciate It:
    >>> def my_view(request):
    ...     program_form = MyProgramForm(request.POST, request.FILES, prefix='prog')

    In the template, you access the inlines like that :
    {{ program_form.inlineformsets.images.management_form }}
    {{ program_form.inlineformsets.images.non_form_errors }}
    <table>
    {{ program_form.inlineformsets.images.as_table }}
    </table>


    """
    __metaclass__ = ModelFormMetaclass

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        if hasattr(self._forms, 'inlines'):
            self.inlineformsets = {}
            fset_initial = kwargs.get('initial', {}).get("_INLINES", {})
            for key, FormSet in self._forms.inlines.items():
                initial = fset_initial.get(key, {})
                self.inlineformsets[key] = FormSet(self.data or None, self.files or None,
                                                   prefix=self._get_formset_prefix(key),
                                                   initial=initial, instance=self.instance)

    def save(self, *args, **kwargs):
        instance = super(ModelForm, self).save(*args, **kwargs)
        if hasattr(self._forms, 'inlines'):
            for fset in self.inlineformsets.values():
                if not fset.has_changed():
                    continue
                fset.save()
        return instance

    def has_changed(self, *args, **kwargs):
        has_changed = super(ModelForm, self).has_changed(*args, **kwargs)
        if has_changed:
            return True
        else:
            for fset in self.inlineformsets.values():
                for i in range(0, fset.total_form_count()):
                    form = fset.forms[i]
                    if form.has_changed():
                        return True
        return False

    def _get_formset_prefix(self, key):
        return u'%s_%s' % (self.prefix, key.upper())

    def _clean_form(self):
        super(ModelForm, self)._clean_form()
        for key, fset in self.inlineformsets.items():
            for i in range(0, fset.total_form_count()):
                f = fset.forms[i]
                if not f.has_changed():
                    continue
                if f.errors:
                    self._errors['_%s_%d' % (fset.prefix, i)] = f.non_field_errors  # Pourquoi non_field_errors ?

    # This should be in forms.Form.
    def as_tr(self):
        return self._html_output(
            normal_row=u'<td%(html_class_attr)s>%(field)s</td>',
            error_row=u'%s',
            row_ender='',
            help_text_html=u'',
            errors_on_separate_row=True
        )


# Image Fields.


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
            from django_thumbor import generate_url
            thumbor_server = settings.THUMBOR_SERVER_EXTERNAL
            url = image_field.url
            storage = image_field.storage
            if hasattr(storage, "key"):
                try:
                    url = storage.key(image_field.name)
                # Cas du ThumborMigrationStorage avec image non-migrée sur Thumbor.
                except NotImplementedError:
                    pass
                else:
                    thumbor_server = settings.THUMBOR_SERVER
            return mark_safe('<img src="%s" width="120">' % generate_url(url, thumbor_server=thumbor_server, width=120))
        else:
            from django.template import Context, Template
            t = Template('{% load thumbnail %}{% thumbnail img_field "120" as im %}<img src="{{ im.url }}"'
                         'width="{{ im.width }}" height="{{ im.height }}">{% endthumbnail %}')
            d = {"img_field": image_field}
            return mark_safe(t.render(Context(d)))


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
