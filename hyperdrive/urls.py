# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('hyperdrive.views',
    url(r'^$', 'dynamic_tabs', name = 'dynamic_tabs'),
    url(r'^(?P<model_name>[\w]+)/$', 'get_data', name = 'get_data'),
)
