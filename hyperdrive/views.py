# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import get_model, CharField, IntegerField, DateField
from django.http import HttpResponse, Http404
from django import forms
import datetime
import json

from hyperdrive.models import HDModel, JSON_FIELDS_TYPE

VALIDATION_FORM_FIELD = {IntegerField: forms.IntegerField, CharField: forms.CharField, DateField: forms.DateField,}


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

    Получаем название модели из адрессной строки и делаем капитализацию.
    Затем получаем модель с помощью метода get_model.
    '''
    if request.is_ajax() and request.method == 'GET':
        model_name = model_name.capitalize()
        model = get_model('hyperdrive', model_name)

        if not model:
            raise Http404

        # Получаем поля модели
        fields = model._meta.fields

        # Создаем список с человекопонятными названиями полей
        fields_name = [f.verbose_name for f in fields]

        items = []

        for item in model.objects.all():
            items.append([{'name': f.name, 'type': JSON_FIELDS_TYPE[f.__class__], 'value': getattr(item, f.name)} for f in fields])

        # Чтобы не было ошибок с датой при json.dumps(obj)
        date_handler = lambda items: (
            items.isoformat()
            if isinstance(items, datetime.datetime)
            or isinstance(items, datetime.date)
            else None
        )

        return HttpResponse(json.dumps({'fields_name': fields_name,
                                        'items': items,
                                        'model': model.__name__
                                        },
                                       default = date_handler),
            content_type = 'application/json')
    else:
        raise Http404


class ValidatorDataFromForm(forms.Form):
    def __init__(self, model_field_class, *args, **kwargs):
        super(ValidatorDataFromForm, self).__init__(*args, **kwargs)
        self.fields['field'] = VALIDATION_FORM_FIELD[model_field_class]()


def edit_data(request):
    result = False
    data = {}

    if request.is_ajax() and request.method == 'POST':
        model = get_model(__name__.split('.')[0], request.POST['model'])
        object_id = int(request.POST['obj_id'])
        data[request.POST['field_name']] = request.POST['value']
        result = model.objects.filter(pk=object_id).update(**data)

    return HttpResponse(json.dumps(result), content_type='application/json')
