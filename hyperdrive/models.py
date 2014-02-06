# -*- coding: utf-8 -*-
from django.db import models
from hyperdrive.utils import get_model_from_config


class BaseModel(object):
    obj = get_model_from_config()


    def finalize(self):

        for yaml_model in self.obj:
            fields = {
                '__unicode__': lambda self: '#%d - %s' % (self.id, yaml_model['name']['fields'][0]['id']),
            }

            f = [(k, v) for k, v in yaml_model['fields'].items()]
            fields.update(f)

            meta_opts = {
                'verbose_name': yaml_model['verbose_name'],
                'verbose_name_plural': yaml_model['verbose_name'],
            }
            admin_opts = {}

            return self.create_model(yaml_model['verbose_name'], fields,
                meta_opts = meta_opts,
                admin_opts = admin_opts,
                app_label = 'hyperdrive',
                module = self.__module__,)


    def create_model(self, name, fields=None, app_label='', module='', meta_opts=None, admin_opts=None):
        """Create specified model"""
        class Meta:
            # Using type('Meta', ...) gives a dictproxy error during model creation
            pass

        if app_label:
            # app_label must be set using the Meta inner class
            setattr(Meta, 'app_label', app_label)

        # Update Meta with any options that were provided
        if meta_opts is not None:
            for key, value in meta_opts.items():
                setattr(Meta, key, value)

        # Set up a dictionary to simulate declarations within a class
        attrs = {'__module__': module, 'Meta': Meta}

        # Add in any fields that were provided
        if fields:
            attrs.update(fields)

        # Create the class, which automatically triggers ModelBase processing
        model = type(name, (models.Model,), attrs)

        # Create an Admin class if admin options were provided
        if admin_opts is not None:
            from django.contrib import admin
            class Admin(admin.ModelAdmin):
                pass
            for key, value in admin_opts:
                setattr(Admin, key, value)
            admin.site.register(model, Admin)

        return model


class HDModel(models.Model):
    models = BaseModel()
    models.finalize()
    models = BaseModel()
    models.finalize()
