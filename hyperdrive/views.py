# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import get_model
from django.http import HttpResponse, Http404
import datetime
import json

from hyperdrive.models import HDModel

def dynamic_tabs(request):
    model_dict = HDModel.model_dict
    models_name = {}

    counter = 0

    for k in model_dict.keys():
        models_name[counter] = k
        counter += 1

    if request.is_ajax():
        raise Http404

    return render(request, 'sidebar.html', {'models': models_name,})


def get_data(request, model_name):
    model_name = model_name.capitalize()
    model = get_model('hyperdrive', model_name)

    if not model:
        raise Http404

    fields = [f.name for f in model._meta.fields]
    qsd = model.objects.all().values_list(*fields)

    date_handler = lambda qsd: (
        qsd.isoformat()
        if isinstance(qsd, datetime.datetime)
        or isinstance(qsd, datetime.date)
        else None
    )

    fields = [f.verbose_name for f in model._meta.fields]
    result = {'fields': fields, 'qsd': list(qsd)}

    if request.is_ajax():
        return HttpResponse(json.dumps(result, default = date_handler), content_type = 'application/json')
    else:
        raise Http404
