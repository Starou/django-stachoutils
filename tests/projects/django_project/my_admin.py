from django.contrib import admin
from django.contrib.admin.templatetags.admin_static import static
from django_stachoutils.admin import ModelAdmin
from my_app import models


class MyAdmin(admin.AdminSite):
    pass


class BandMemberAdmin(ModelAdmin):
    pass
    

admin_site = MyAdmin(name='my-admin')
admin_site.register(models.BandMember, BandMemberAdmin)
