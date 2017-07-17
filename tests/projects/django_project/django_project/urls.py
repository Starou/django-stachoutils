from django.conf.urls import include, url
from my_admin import admin_site

urlpatterns = [
    url(r'^admin/', include(admin_site.urls)),
]
