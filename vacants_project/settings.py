"""
Django settings for vacants_project project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import django_heroku

# Django doesn't serve static files on its own when DEBUG is set to False; that's what
# whitenoise does. (Otherwise we get 500 errors)
import whitenoise

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'h2&$a6itbdb1ik)53jag8x238x+c29jz9%2sq)1%s$og4zlo(b')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Verbose logging - used to investigate 500 errors that creep up after we set DEBUG to False
# Example: "Missing staticfiles manifest entry for '/css/style.css'"
import logging

LOGGING = logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
)

ALLOWED_HOSTS = ['vacants.herokuapp.com',
                 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'okcvacants.apps.OkcvacantsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vacants_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'okcvacants/templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vacants_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'vacants',
        'USER': 'geodjango',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_vacants'
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# serializers
SERIALIZATION_MODULES = {
    "geojson": "django.contrib.gis.serializers.geojson",
    "neighborhood_geojson": "okcvacants.neighborhood_geojson_serializer"
}

GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.getenv('GEOS_LIBRARY_PATH')

if (os.getenv('IS_HEROKU')):
    # staticfiles is set to False: django_heroku sets the STATICFILES_STORAGE variable, which seems to be
    # causing problems (and we've got staticfiles configured already)
    django_heroku.settings(locals(), staticfiles=False)

if DATABASES['default']['ENGINE'] in ('django.db.backends.postgresql', 'django.db.backends.postgresql_psycopg2'):
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'
elif DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.spatialite'
