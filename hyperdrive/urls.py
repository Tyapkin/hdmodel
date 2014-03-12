# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('hyperdrive.views',
    url(r'^$', 'hyper_tabs', name = 'hyper_tabs'),
    url(r'^(?P<model_name>[\w]+)/$', 'hyper_data', name = 'hyper_data'),
)

urlpatterns += patterns('hyperdrive.hdforms',
    url(r'^(?P<model_name>[\w]+)/add/$', 'hyper_form', name = 'hyper_form'),
)
