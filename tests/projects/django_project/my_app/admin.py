from django.contrib import admin
from django.db.models import TextField, CharField
from django_stachoutils.forms.widgets import AdminTexteEditeur, TextInputCounter, TextareaCounter
from my_app import models



class BandMemberAdmin(admin.ModelAdmin):
    formfield_overrides = {
        TextField: {'widget': AdminTexteEditeur(attrs={"class": "vMediumTextField"})},
        CharField: {'widget': TextInputCounter(max_signs=35)},
    }

    class Media:
        js = ("https://code.jquery.com/jquery-2.2.4.min.js",)


class MusicGenreAdmin(admin.ModelAdmin):
    formfield_overrides = {
        TextField: {'widget': TextareaCounter(max_signs=200)},
    }

    class Media:
        js = ("https://code.jquery.com/jquery-2.2.4.min.js",)


admin.site.register(models.BandMember, BandMemberAdmin)
admin.site.register(models.MusicGenre, MusicGenreAdmin)
