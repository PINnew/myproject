# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings


# Указываем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
# Загружаем конфигурацию из Django
app.config_from_object('django.conf:settings')
# Автоматически обнаруживаем задачи в приложениях
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
