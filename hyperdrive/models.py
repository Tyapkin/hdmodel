# -*- coding: utf-8 -*-
from django.db.models import Model, AutoField, IntegerField, DateField, CharField
from hyperdrive.utils import get_model_from_config

FIELDS_TYPE = {'auto': AutoField, 'char': CharField, 'date': DateField, 'int': IntegerField}
JSON_FIELDS_TYPE = dict((v, k) for k, v in FIELDS_TYPE.items())


class BaseModel(object):
    obj = get_model_from_config()

    def finalize(self):

        for yaml_model in self.obj:
            fields = {
                '__unicode__': lambda self: '#%d - %s' % (self.id, yaml_model['verbose_name']),
            }

            f = [(k, v) for k, v in yaml_model['fields'].items()]
            fields.update(f)

            meta_opts = {
                'verbose_name': yaml_model['verbose_name'],
                'verbose_name_plural': yaml_model['verbose_name'],
            }
            admin_opts = {}

            model = self.create_model(yaml_model['verbose_name'], fields,
                meta_opts = meta_opts,
                admin_opts = admin_opts,
                app_label = 'hyperdrive',
                module = self.__module__,)

            return model

    def create_model(self, name, fields=None, app_label='', module='', meta_opts=None, admin_opts=None):
        '''Создание указанной модели'''
        class Meta:
            # Использование type('Мета', ...) вызовет dictproxy ошибку во время создания модели
            pass

        if app_label:
            # app_label должна быть установлена с помощью внутреннего класса Meta
            setattr(Meta, 'app_label', app_label)

        # Обновление класса Meta со всеми предоставленными опциями
        if meta_opts is not None:
            for key, value in meta_opts.items():
                setattr(Meta, key, value)

        # Определяем словарь для имитации описаний в классе
        attrs = {'__module__': module, 'Meta': Meta}

        # Добавляем все поля в атрибуты, которые были предоставленны
        if fields:
            attrs.update(fields)

        # Создать класс, который автоматически запускает обработку ModelBase
        model = type(name, (Model,), attrs)

        # Создание класса администратора системы, если были предоставлены опции
        if admin_opts is not None:
            from django.contrib import admin
            class Admin(admin.ModelAdmin):
                pass
            for key, value in admin_opts:
                setattr(Admin, key, value)
            admin.site.register(model, Admin)

        return model


class HDModel(Model):
    model_dict = {}
    obj = get_model_from_config()
    
    for rec in obj:
        models = BaseModel()
        model = models.finalize()
        model_dict[model._meta.verbose_name] = model


    class Meta:
        abstract = True
