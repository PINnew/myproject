# -*- coding: utf-8 -*-
"""
Django settings for myproject project.
Для дополнительной информации:
https://docs.djangoproject.com/en/1.9/topics/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: не используйте этот ключ в продакшене! Сгенерируйте новый.
SECRET_KEY = 'замените_этот_текст_на_настоящий_секретный_ключ'

# Режим отладки (True для разработки, False для продакшена)
DEBUG = True

ALLOWED_HOSTS = []

# Приложения Django
INSTALLED_APPS = (
    'django.contrib.admin',  # если админку планируете использовать
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mailing',  # ваше приложение для рассылок
)

# Средства промежуточной обработки запросов
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# Настройки Celery
# BROKER_URL = 'redis://localhost:6379/0'
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


ROOT_URLCONF = 'myproject.urls'

WSGI_APPLICATION = 'myproject.wsgi.application'

# Настройка базы данных - используется SQLite для разработки
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Настройки интернационализации
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Статические файлы (CSS, JavaScript, изображения)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
