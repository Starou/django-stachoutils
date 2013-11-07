from django.conf.urls import patterns, include, url
from my_admin import admin_site

urlpatterns = patterns('',
    (r'^admin/', include(admin_site.urls)),
)
