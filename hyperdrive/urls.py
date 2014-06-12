# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'hyperdrive.views.hyper_tabs', name='hyper_tabs'),
    url(r'^edit/$', 'hyperdrive.views.edit_data', name='edit'),
    url(r'^(?P<model_name>[\w]+)/$', 'hyperdrive.views.hyper_data', name='hyper_data'),
    url(r'^(?P<model_name>[\w]+)/add/$', 'hyperdrive.hdforms.hyper_form', name='hyper_form'),
)
