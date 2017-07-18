from django.contrib import admin
from django.db.models import TextField
from django_stachoutils.forms.widgets import AdminTexteEditeur
from my_app import models



class BandMemberAdmin(admin.ModelAdmin):
    formfield_overrides = {
        TextField: {'widget': AdminTexteEditeur},
    }

    class Media:
        js = ("https://code.jquery.com/jquery-2.2.4.min.js",)


admin.site.register(models.BandMember, BandMemberAdmin)
