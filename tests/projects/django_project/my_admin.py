from django.contrib import admin
from my_app import models


class MyAdmin(admin.AdminSite):
    pass


class BandMemberAdmin(admin.ModelAdmin):
    pass


admin_site = MyAdmin(name='my-admin')
admin_site.register(models.BandMember, BandMemberAdmin)
