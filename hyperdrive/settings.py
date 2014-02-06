# -*- coding: utf-8 -*-
import os
from django.conf import settings


APP_PATH = os.path.abspath(os.path.dirname(__file__))

# Конфигурация для приложения dynamic
CONFIG_FILE = getattr(settings, 'DYNAMIC_CONFIG_FILE', os.path.join(APP_PATH, 'config.yaml'))
MAX_LENGTH_CHAR = getattr(settings, 'DYNAMIC_MAX_LENGTH_CHAR', 64)
MAX_LENGTH_INT = getattr(settings, 'DYNAMIC_MAX_LENGTH_INT', 5)
