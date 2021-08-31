"""
Django settings for myfirstapp project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
#from myfirstapp.apps import reddit
import os, sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# the actual path: /Users/nikitaizmailov/Desktop/web_app/django_app/myfirstapp
BASE_DIR = Path(__file__).resolve().parent.parent

# the actual path: /Users/nikitaizmailov/Desktop/web_app/django_app/myfirstapp/myfirstapp
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$n)i%87m@nh4zdf@3yrdqpouq(*ut4@=p86f$$ns5y)76fz23w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['https://wsb-nikitaizm.herokuapp.com', 'wsb-nikitaizm.herokuapp.com', 'wsb-nikitaizm.herokuapp.com/', '127.0.0.1']
ALLOWED_HOSTS = ['wsb-nikitaizm.herokuapp.com', 'https://wsb-nikitaizm.herokuapp.com', '127.0.0.1']


# Application definition
INSTALLED_APPS = [
    # my apps that I have created and installed
    'reddit.apps.RedditConfig',
    'stocks.apps.StocksConfig',

    # this is the main app that will be used.
    'wsb.apps.WsbConfig',

    
    'grappelli',
    'crispy_forms',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # below app should be installed to see static css and js files
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    #'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',


    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',



    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myfirstapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates')
        ],
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

WSGI_APPLICATION = 'myfirstapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# mysql-client==0.0.1

# Connected to my MySQL database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'USER': 'test_admin',
        'PASSWORD': 'test_admin',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Add static file directory. This basically tells django where to look for css,js
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Selecting a Bootstrap4 template pack for Django Crispy Forms.
CRISPY_TEMPLATE_PACK = 'bootstrap4'
