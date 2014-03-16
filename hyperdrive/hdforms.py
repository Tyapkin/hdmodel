# -*- coding: utf-8 -*-
from django.db.models import get_model
from django.forms import ModelForm
from django.forms.models import modelform_factory
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
import json


def hyper_form(request, model_name):
    model = get_model('hyperdrive', model_name.capitalize())

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
        form = Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../../thanks/')
    else:
        form = Form()

    return render(request, 'form.html', {'form': form, 'model': model_name,})

# Сделать форму информативней...
