# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.db.models import get_model
from django.http import HttpResponse, Http404
import datetime
import json

from hyperdrive.models import HDModel


def hyper_tabs(request):
    '''
    Динамическая навигация. Получаем словарь моделей из класса HDModel,
    потом в цикле получаем ключи и всовываем в словарь models_name.
    '''
    model_dict = HDModel.model_dict
    models_name = {}

    counter = 0

    for k in model_dict.keys():
        models_name[counter] = k
        counter += 1

    if request.is_ajax():
        raise Http404

    return render(request, 'sidebar.html', {'models': models_name,})


def hyper_data(request, model_name):
    '''
    Здесь динамически получаем данные, и с помощью jQuery обрабатываем данные
    и помещаем их в таблицу. Никаких кусков html-кода!
    '''

    # Получаем название модели и адрессной строки и делаем капитализацию.
    # Потом получаем модель с помощью метода get_model.
    model_name = model_name.capitalize()
    model = get_model('hyperdrive', model_name)

    if not model:
        raise Http404

    # Получаем название полей в модели
    fields = [f.name for f in model._meta.fields]

    # Получаем кортеж со значениями указанными в values_list
    qsd = model.objects.all().values_list(*fields)

    # Чтобы не было ошибок с датой при json.dumps(obj)
    date_handler = lambda qsd: (
        qsd.isoformat()
        if isinstance(qsd, datetime.datetime)
        or isinstance(qsd, datetime.date)
        else None
    )

    # Теперь получаем человеческие названи полей модели
    fields = [f.verbose_name for f in model._meta.fields]

    result = {'fields': fields, 'qsd': list(qsd),}

    if request.is_ajax():
        return HttpResponse(
            json.dumps(result, default = date_handler),
            content_type = 'application/json')
    else:
        raise Http404
