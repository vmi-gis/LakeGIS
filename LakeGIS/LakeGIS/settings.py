# coding: utf8
"""
Django settings for LakeGIS project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
fillPath = lambda x: os.path.join(os.path.dirname(__file__), x)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mn5&^mivsi+h8m!+cwjuy$*yru1#ea5$sso=lg3_)6sv+hmyv-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

TEMPLATE_DIRS = (
    fillPath('templates'),
)
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'rest_framework',
    'lakegis_app'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'LakeGIS.urls'

WSGI_APPLICATION = 'LakeGIS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'lakegis',
        'USER': 'lakegis'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'django.assets.finders.AssetsFinder',
)

# API-ключ для викимапии должен быть в local_settings.py
WIKIMAPIA_API_KEY = ''

WIKIMAPIA_SEARCH_SETTINGS = {
    'query_string' : 'база+отдыха+санаторий+ГЛЦ',
    'allowed_categories' : [
        58568, # база отдыха
        31250, # дом отдыха
        16969, # санаторий/профилакторий
        44710, # пансионат
        50,    # гостиница
        44740, # летний оздоровительный/трудовой лагерь
        3220,  # лыжный спорт
        32193, # горнолыжный курорт
        623,   # кемпинг
    ],
    'forbidden_categories' : [
        45716, # нежилое здание
        194,   # парк
        557,   # развалины, руины
        2390,  # заброшенный, неиспользуемый объект
    ]
}

try:
    from local_settings import *
except ImportError:
    pass

