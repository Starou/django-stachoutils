# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.conf.urls import patterns
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext


class DumpdataForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput, required=True)
    selected = forms.CharField(widget=forms.HiddenInput, required=True)
    use_natural_keys = forms.BooleanField(label="Use natural Keys", initial=True, required=False)
    dump_format = forms.ChoiceField(choices=[('json', 'Json'), ('xml', 'XML')], initial='json', required=True)
    indent_level = forms.IntegerField(min_value=0, max_value=8, initial=2, widget=forms.TextInput(attrs={"size": "2"}), required=True)


class ModelAdmin(admin.ModelAdmin):
    actions = ["dumpdata"]

    def get_actions(self, request):
        actions = super(ModelAdmin, self).get_actions(request)
        if not request.user.is_superuser and "dumpdata" in actions:
            del actions["dumpdata"]
        return actions

    def get_urls(self):
        return patterns('',
            (r'^dumpdata/$', self.admin_site.admin_view(self.dumpdata_form)),
        ) + super(ModelAdmin, self).get_urls()

    def dumpdata(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("dumpdata/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))

    def dumpdata_form(self, request):
        if request.method == "GET":
            initial = {
                'content_type': request.GET["ct"],
                'selected': request.GET["ids"]
            }
            form = DumpdataForm(None, initial=initial)
        elif request.method == "POST":
            form = DumpdataForm(request.POST)
            if form.is_valid():
                json = {}
                fmt = form.cleaned_data['dump_format']
                indent = form.cleaned_data['indent_level']
                use_natural_keys = form.cleaned_data['use_natural_keys']

                ctype = ContentType.objects.get_for_id(form.cleaned_data["content_type"])
                queryset = ctype.get_all_objects_for_this_type().filter(
                    pk__in=form.cleaned_data["selected"].split(","))

                objects = list(queryset)
                dependancies = []
                for obj in queryset:
                    append_obj_dependancies(obj, dependancies) 
                objects = dependancies + objects
                #TODO sort object by appname.modelname.
                # use_natural_keys fout la merde dans les dossiers pour les ref user.

                stream = serializers.serialize(fmt, objects, indent=indent,
                                               use_natural_keys=use_natural_keys)
                return HttpResponse(stream, content_type='application/json')
        return render_to_response('django_stachoutils/admin/dumpdata_form.html', {
            'title': "Dump data",
            'is_popup': request.REQUEST.has_key('_popup'),
            'form': form,
        }, context_instance=RequestContext(request))
    dumpdata.short_description = u'Dump the selected objects'


def append_obj_dependancies(obj, dependancies, add_m2m=True):
    for field in obj.__class__._meta.fields:
        if isinstance(field, models.ForeignKey):
            rel = getattr(obj, field.name)
            if rel and rel not in dependancies:
                dependancies.insert(0, rel)
                append_obj_dependancies(rel, dependancies, add_m2m=False)
    if add_m2m:
        for related in obj._meta.get_all_related_objects():
            try:
                objs = getattr(obj, related.get_accessor_name()).all()
            # Cas des OneToOne.
            except AttributeError:
                objs = [getattr(obj, related.field.related_query_name())]
            for rel in objs:
                dependancies.insert(0, rel)
                append_obj_dependancies(rel, dependancies, add_m2m=False)
