from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'hyperdrive.views.index', name='index'),
    url(r'^hd/', include('hyperdrive.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
