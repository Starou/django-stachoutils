# -*- coding: utf-8 -*-

from builtins import range
from builtins import object
from django import forms
from django.forms.models import ModelFormMetaclass
from django.utils.encoding import force_str
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from future.utils import with_metaclass


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


class ModelForm(with_metaclass(ModelFormMetaclass, forms.ModelForm)):
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
        formset_prefix = key.upper()
        if self.prefix:
            formset_prefix = u'{}_{}'.format(self.prefix, formset_prefix)
        return formset_prefix

    def _clean_form(self):
        super(ModelForm, self)._clean_form()
        for key, fset in self.inlineformsets.items():
            if any(fset.errors):
                self._errors['_%s' % fset.prefix] = fset.non_form_errors()
            for i in range(0, fset.total_form_count()):
                f = fset.forms[i]
                if not f.has_changed():
                    continue
                if f.errors:
                    self._errors['_%s_%d' % (fset.prefix, i)] = f.non_field_errors()

    # This should be in forms.Form.
    def as_tr(self):
        return self._html_output(
            normal_row=u'<td%(html_class_attr)s>%(field)s</td>',
            error_row=u'%s',
            row_ender='<span class="row_end"></span>',
            help_text_html=u'',
            errors_on_separate_row=True
        )

    def labels_as_tr(self):
        out = []
        for name in self.fields.keys():
            bf = self[name]
            if bf.is_hidden:
                continue
            if bf.label:
                label = conditional_escape(force_str(bf.label))
                label = bf.label_tag(label, label_suffix="") or ''
            else:
                label = ''
            out.append(u"<th>%s</th>" % force_str(label))

        return mark_safe(u'<tr>%s</tr>' % ''.join(out))
