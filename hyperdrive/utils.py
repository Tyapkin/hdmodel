# -*- coding: utf-8 -*-
from django.db import models
from hyperdrive.settings import CONFIG_FILE, MAX_LENGTH_CHAR, MAX_LENGTH_INT
import yaml


def yaml_to_field(field_type, **kwargs):

	# Функция возвращает тип поля для Django-модели
	if field_type == 'int':
		field = models.IntegerField(max_length = MAX_LENGTH_INT, **kwargs)

	if field_type == 'char':
		field = models.CharField(max_length = MAX_LENGTH_CHAR, **kwargs)

	if field_type == 'date':
		field = models.DateField(**kwargs)

	return field


def get_model_from_config(config_file = CONFIG_FILE):

	stream = None
	
	# Пробуем открыть файл конфигурации
	try:
		stream = open(config_file, 'r').read()
	except FileNotFoundError:
		print ('Ooops! No such file or directory: ', config_file)

	obj = yaml.load(stream, Loader = yaml.Loader)

	for model in obj.keys():
		fields = [f for f in obj[model]['fields']]
		fields_dict = {}

		for field in fields:
			kwargs = {
				'verbose_name': field['title'],
				'blank': True,
				'null': True,
			}

			f = {field['id']:yaml_to_field(field['type'], **kwargs)}
			fields_dict.update(f)

			result = {
				'name': obj[model],
				'verbose_name': obj[model]['title'],
				'fields': fields_dict
			}

		yield result
