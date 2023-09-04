from pathlib import Path
import os
from environ import Env
from coreApp.keys import *

env = Env()
env.read_env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = 'KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = []
# ALLOWED_HOSTS = [
#     'todo.thehive-services.com',
#     'dev-todo.thehive-services.com'
# ]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',
    'https://todo.thehive-services.com',
    'https://dev-todo.thehive-services.com',
    'http://todo.thehive-services.com',
    'http://dev-todo.thehive-services.com',
]

CORS_ALLOWED_ALL_ORIGINS: True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'coreApp.apps.CoreappConfig',
    'apiApp.apps.ApiappConfig',
    'userApp.apps.UserappConfig',
    'corsheaders',
    'rest_framework',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'todo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'todo.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR,'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'mysql.connector.django',
#         # 'ENGINE':'django.db.backends.mysql',
#         'NAME': 'thehives_todo',
#         'USER': 'root',
#         # 'USER': 'thehives_todo',
#         'PASSWORD': 'HoneyBee#4',
#         # 'PASSWORD': 'LilyBee',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         # 'OPTIONS': {'charset': 'utf8mb4'},
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'beedev.services@gmail.com'
# EMAIL_HOST_USER = 'kowabungahooker@gmail.com'
EMAIL_HOST_PASSWORD = 'HOST_PASSWORD'
EMAIL_HOST_ALT_USER = 'melissa@beedev-services.com'
