# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import flatatt
from django.utils.html import escape, conditional_escape
from django.utils.text import Truncator
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.utils import simplejson

from django.conf import settings

from django.contrib.admin import widgets as admin_widgets
from django.contrib.admin.views.main import TO_FIELD_VAR

from adencf_commons.shortcuts import encode_default


class ForeignKeyRawIdHiddenWidget(forms.HiddenInput):
    class Media:
        css = {
            'all': (
                'adencf_commons/css/forms.css',
            )
        }
        js = (
            'adencf_commons/js/widgets.js',
        )
    
    # TODO, passer onchange devant ajax_*.
    def __init__(self, model, field, ajax_search_url=None, ajax_search_min_chars=3, onchange='null', search_width=200,
                 limit_choices_to={}, select_related_lookup=True, show_related_lookup=True, attrs=None, using=None,
                 ajax_search_params=None, get_label_url=''):
        self.rel = model._meta.get_field(field).rel
        self.db = using
        self.limit_choices_to = limit_choices_to
        self.select_related_lookup = select_related_lookup
        self.show_related_lookup = show_related_lookup
        self.ajax_search_url = ajax_search_url
        self.ajax_search_min_chars = ajax_search_min_chars
        self.onchange = onchange
        self.search_width = search_width
        self.get_label_url = get_label_url
        self.ajax_search_params = ajax_search_params or {}
        super(ForeignKeyRawIdHiddenWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        related_url = '/admin/%s/%s/' % (self.rel.to._meta.app_label, self.rel.to._meta.object_name.lower())
        params = self.url_parameters()
        if params:
            url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.items()])
        else:
            url = ''
        css_class = self.attrs.get('class','')
        if not attrs.has_key('class'):
            attrs['class'] = css_class + ' vForeignKeyRawIdAdminField' # The JavaScript looks for this hook.
        # On stock le non de l'appli et du modèle pour l'appel ajax qui met à jour le label via contenttype
        output = ['<input class="related_model_name" type="hidden" value="%s" />' % (self.rel.to._meta.object_name.lower(),),
                  '<input class="related_app_name" type="hidden" value="%s" />' % (self.rel.to._meta.app_label,), 
                  '<input class="show_related_lookup" type="hidden" value="%s" />' % (self.show_related_lookup and '1' or '0'), 
                    super(ForeignKeyRawIdHiddenWidget, self).render(name, value, attrs)]
        output.append(self.onchange_tag(name, self.onchange, self.get_label_url))
        output.append('<div class="label_container" style="float:left;">')
        output.append(self.label_for_value(value))
        if self.select_related_lookup:
            output.append("""<a href="%s%s" class="related-lookup" id="lookup_id_%s" onclick="return showRelatedObjectLookupPopup(this);">""" % (related_url, url, name))
            output.append('<img src="%sadmin/img/selector-search.gif" width="16" height="16" alt="%s" /></a>' % (settings.STATIC_URL, _('Lookup')))
        output.append(('<a onclick="return clearRawId2(this);" href="#">'
                       '<img width="10" height="10" title="Vider" alt="Clear" src="%sadmin/img/icon_deletelink.gif"></a>' % settings.STATIC_URL))
        if self.ajax_search_url:
            search_id = "%s_search" % (name,)
            output.append("""<br /><input type="hidden" value="%s" /><input placeholder="Rechercher" 
                          type="search" name="_seach" id="%s"
                          class="ajax_related_lookup" style="width:%dpx;" />%s""" % (
                              self.ajax_search_url,
                              search_id,
                              self.search_width,
                              self.autocomplete_tag(search_id, 
                                                    self.ajax_search_url,
                                                    self.ajax_search_params,
                                                    self.ajax_search_min_chars,
                                                    self.search_width))
                         )
        output.append('</div>')
        return mark_safe(u''.join(output))

    def base_url_parameters(self):
        params = {}
        if self.rel.limit_choices_to and hasattr(self.rel.limit_choices_to, 'items'):
            items = []
            for k, v in self.rel.limit_choices_to.items():
                if isinstance(v, list):
                    v = ','.join([str(x) for x in v])
                else:
                    v = str(v)
                items.append((k, v))
            params.update(dict(items))
        return params

    def url_parameters(self):
        params = self.base_url_parameters()
        params.update(self.limit_choices_to)
        params.update({TO_FIELD_VAR: self.rel.get_related_field().name})
        return params

    def label_for_value(self, value):
        # TODO: mettre le preview ici.
        if value:
            key = self.rel.get_related_field().name
            obj = self.rel.to._default_manager.get(**{key: value})
            url = obj.get_absolute_url()
            preview = ''
            onclick = 'return false;'
            if self.show_related_lookup:
                onclick = "return showRelatedObjectPopup(this);"
            if hasattr(obj, "get_preview_url"):
                preview = '<img src="%s" />' % (obj.get_preview_url() or '')
            label = escape(Truncator(obj).words(14, truncate=" ..."))
            return ('&nbsp;<strong class="label"><a class="preview" href="%(url)s" ' 
                    'onclick="%(onclick)s">%(label)s'
                    '%(preview)s</a> </strong>' % {
                        'label':label, 
                        'onclick': onclick,
                        'url':url,
                        'preview': preview})
        else:
            label = u"<em>Choisissez une valeur</em>"
            return '&nbsp;<strong class="label">%s</strong>' % label

    def autocomplete_tag(self, input_id, url, params, min_chars, width):
        """
        http://www.devbridge.com/projects/autocomplete/jquery/
        """
        return (
            '<script type="text/javascript">'
                '$(document).ready(function () { '
                    '$("#%(input_id)s").autocomplete({ '
                        'serviceUrl: "%(url)s", '
                        'params: %(params)s, '
                        'minChars: %(min_chars)d, '
                        'width: %(width)d, '
                        'onSelect: function(value, chosenId) { '
                            'var fkInput = $("#%(input_id)s").parent().prevAll("input.vForeignKeyRawIdAdminField"); '
                            'fkInput.val(chosenId).change(); '
                        '}'
                    '});'
                '});'
            '</script>' % {
                'input_id': input_id, 
                'url': url, 
                'params': simplejson.dumps(params, default=encode_default), 
                'width': width, 
                'min_chars': min_chars})

    def onchange_tag(self, name, callback, get_label_url):
        """La fonction onForeignKeyChanged est une surcharge d'admin_media."""
        return (
            '<script type="text/javascript">'
                '$(document).ready(function () { '
                    '$("input[name=%(name)s]").change(function(){ '
                    'onForeignKeyChanged($(this), %(callback)s, "%(get_label_url)s");}); '
                '});'
            '</script>' % {
                'name': name, 
                'callback': callback,
                'get_label_url': get_label_url})


BUTTONS = [{'class': 'gras', 'text': u'Gras', 'accesskey': 'g'},
           {'class': 'sup', 'text': u'Supérieur', 'accesskey': 's'},
           {'class': 'bas', 'text': u'Bas de casse', 'accesskey': 'b'}]

STATICS = {'js': ['adencf_commons/js/jquery.charcounter.js',
                  'adencf_commons/js/jquery.fieldselection.js',
                  'adencf_commons/js/widgets.js']}

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
