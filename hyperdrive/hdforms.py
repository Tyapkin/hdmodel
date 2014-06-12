# -*- coding: utf-8 -*-
from django.db.models import get_model
from django.forms import ModelForm
from django.forms.models import modelform_factory
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django import forms
from django.core.urlresolvers import reverse


def hyper_form(request, model_name):
    model = get_model(__name__.split('.')[0], model_name.capitalize())

    if not model:
        raise Http404

    fields = [f.name for f in model._meta.fields]

    Form = modelform_factory(
        model,
        form = ModelForm,
        fields = fields,
        exclude = None,
        formfield_callback = None,
        widgets = None
    )

    if request.method == 'POST':
        form = Form(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('hyper_tabs'))
    else:
        form = Form()

    return render(request, 'form.html', {'form': form, 'model': model_name,})
