# -*- coding: utf-8 -*-

from django import forms
from django.test import TestCase

from .models import Car


class WidgetsTest(TestCase):
    def test_render_admin_texte_editeur_widget(self):
        from django_stachoutils.forms.widgets import AdminTexteEditeur

        class CarForm(forms.ModelForm):
            description = forms.CharField(widget=AdminTexteEditeur,
                                          label="Describe the car",
                                          required=False)

            class Meta:
                model = Car
                fields = ('name', 'brand', 'description')

        form = CarForm()
        self.assertHTMLEqual(
            form.as_table(),
            """
            <tr>
              <th><label for="id_name">Name:</label></th>
              <td><input type="text" name="name" required id="id_name" maxlength="20" /></td>
            </tr>
            <tr>
              <th><label for="id_brand">Brand:</label></th>
              <td><input type="text" name="brand" required id="id_brand" maxlength="100" /></td>
            </tr>
            <tr>
              <th><label for="id_description">Describe the car:</label></th>
              <td>
                <div class="editeur">
                  <div class="toolbar">
                    <button type="button" accesskey="g" class="gras">Gras</button>
                    <button type="button" accesskey="s" class="sup">Supérieur</button>
                    <button type="button" accesskey="b" class="bas">Bas de casse</button>
                    <button type="button" accesskey="G" class="gras_phrases">Gras phrases</button>
                  </div>
                  <textarea name="description" id="id_description" rows="10" cols="40" class="vLargeTextField">
                  </textarea>
                </div>
              </td>
            </tr>
            """
        )
        self.assertHTMLEqual(
            str(form.media),
            """
            <script type="text/javascript" src="/static/django_stachoutils/js/jquery.charcounter.js"></script>
            <script type="text/javascript" src="/static/django_stachoutils/js/jquery.fieldselection.js"></script>
            <script type="text/javascript" src="/static/django_stachoutils/js/editeur.js"></script>
            """
        )

    def test_render_textarea_counter_widget(self):
        from django_stachoutils.forms.widgets import TextareaCounter

        class CarForm(forms.ModelForm):
            description = forms.CharField(widget=TextareaCounter(max_signs=200),
                                          label="Describe the car",
                                          required=False)

            class Meta:
                model = Car
                fields = ('name', 'brand', 'description')

        form = CarForm()
        self.assertHTMLEqual(
            form.as_table(),
            """
            <tr>
              <th><label for="id_name">Name:</label></th>
              <td><input type="text" name="name" required id="id_name" maxlength="20" /></td>
            </tr>
            <tr>
              <th><label for="id_brand">Brand:</label></th>
              <td><input type="text" name="brand" required id="id_brand" maxlength="100" /></td>
            </tr>
            <tr>
              <th><label for="id_description">Describe the car:</label></th>
              <td>
                <div class="editeur">
                  <div class="toolbar">
                    <button type="button" accesskey="g" class="gras">Gras</button>
                    <button type="button" accesskey="s" class="sup">Supérieur</button>
                    <button type="button" accesskey="b" class="bas">Bas de casse</button>
                    <button type="button" accesskey="G" class="gras_phrases">Gras phrases</button>
                  </div>
                  <textarea name="description" id="id_description" rows="10" cols="40" class="vLargeTextField">
                  </textarea>
                </div>
                <script type="text/javascript">$(document).ready(function () { $("#id_description").charCounter(200, {container: "<div></div>",direction: "up",format: "%1 signe(s)",limit: false,limit_class: "error"});});</script>
              </td>
            </tr>
            """
        )
        self.assertHTMLEqual(
            str(form.media),
            """
            <script type="text/javascript" src="/static/django_stachoutils/js/jquery.charcounter.js"></script>
            <script type="text/javascript" src="/static/django_stachoutils/js/jquery.fieldselection.js"></script>
            <script type="text/javascript" src="/static/django_stachoutils/js/editeur.js"></script>
            """
        )

    def test_render_textarea_counter_widget_reversed_counter(self):
        from django_stachoutils.forms.widgets import TextareaCounter

        class CarForm(forms.ModelForm):
            description = forms.CharField(widget=TextareaCounter(max_signs=200, direction='down'),
                                          label="Describe the car",
                                          required=False)

            class Meta:
                model = Car
                fields = ('name', 'brand', 'description')

        form = CarForm()
        self.assertHTMLEqual(
            form.as_table(),
            """
            <tr>
              <th><label for="id_name">Name:</label></th>
              <td><input type="text" name="name" required id="id_name" maxlength="20" /></td>
            </tr>
            <tr>
              <th><label for="id_brand">Brand:</label></th>
              <td><input type="text" name="brand" required id="id_brand" maxlength="100" /></td>
            </tr>
            <tr>
              <th><label for="id_description">Describe the car:</label></th>
              <td>
                <div class="editeur">
                  <div class="toolbar">
                    <button type="button" accesskey="g" class="gras">Gras</button>
                    <button type="button" accesskey="s" class="sup">Supérieur</button>
                    <button type="button" accesskey="b" class="bas">Bas de casse</button>
                    <button type="button" accesskey="G" class="gras_phrases">Gras phrases</button>
                  </div>
                  <textarea name="description" id="id_description" rows="10" cols="40" class="vLargeTextField">
                  </textarea>
                </div>
                <script type="text/javascript">$(document).ready(function () { $("#id_description").charCounter(200, {container: "<div></div>",direction: "down",format: "%1 signe(s) restant(s)",limit: false,limit_class: "error"});});</script>
              </td>
            </tr>
            """
        )

    def test_render_textinput_counter_widget(self):
        from django_stachoutils.forms.widgets import TextInputCounter

        class CarForm(forms.ModelForm):
            name = forms.CharField(widget=TextInputCounter(max_signs=100),
                                          label="Name of the car",
                                          required=True)

            class Meta:
                model = Car
                fields = ('name', 'brand')

        form = CarForm()
        self.assertHTMLEqual(
            form.as_table(),
            """
            <tr>
              <th><label for="id_name">Name of the car:</label></th>
              <td>
                <input type="text" name="name" required id="id_name" />
                <script type="text/javascript">$(document).ready(function () { $("#id_name").charCounter(100, {container: "<span></span>",direction: "up",format: "%1 signe(s)",limit: false,limit_class: "error"});});</script>
              </td>
            </tr>
            <tr>
              <th><label for="id_brand">Brand:</label></th>
              <td><input type="text" name="brand" required id="id_brand" maxlength="100" /></td>
            </tr>
            """
        )
        self.assertHTMLEqual(
            str(form.media),
            """
            <script type="text/javascript" src="/static/django_stachoutils/js/jquery.charcounter.js"></script>
            <script type="text/javascript" src="/static/django_stachoutils/js/jquery.fieldselection.js"></script>
            <script type="text/javascript" src="/static/django_stachoutils/js/editeur.js"></script>
            """
        )

    def test_render_textinput_counter_widget_reversed_counter(self):
        from django_stachoutils.forms.widgets import TextInputCounter

        class CarForm(forms.ModelForm):
            name = forms.CharField(widget=TextInputCounter(max_signs=100, direction='down'),
                                          label="Name of the car",
                                          required=True)

            class Meta:
                model = Car
                fields = ('name', 'brand')

        form = CarForm()
        self.assertHTMLEqual(
            form.as_table(),
            """
            <tr>
              <th><label for="id_name">Name of the car:</label></th>
              <td>
                <input type="text" name="name" required id="id_name" />
                <script type="text/javascript">$(document).ready(function () { $("#id_name").charCounter(100, {container: "<span></span>",direction: "down",format: "%1 signe(s) restant(s)",limit: false,limit_class: "error"});});</script>
              </td>
            </tr>
            <tr>
              <th><label for="id_brand">Brand:</label></th>
              <td><input type="text" name="brand" required id="id_brand" maxlength="100" /></td>
            </tr>
            """
        )
