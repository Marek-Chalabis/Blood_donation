import os
from . import super_secret_informations

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = super_secret_informations.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1'] + super_secret_informations.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'info',
    'crispy_forms',
    'django_filters',
    'bootstrapform',
    'django_cleanup.apps.CleanupConfig',
    'localflavor',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',


    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'blood_dontaion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'blood_dontaion.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# login/logout routine
LOGIN_REDIRECT_URL = 'main'
LOGOUT_REDIRECT_URL = 'main'
LOGIN_URL = 'login'

# email info
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = super_secret_informations.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = super_secret_informations.EMAIL_HOST_PASSWORD
EMAIL_PORT = 587

# caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',   # saves caches in DB
        'LOCATION': 'cache_table'  # DB table for caches
    }
}

# ADDS FOR APPS
# bootstrap - updated visuals
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# IP for debug_toolbar (only for local right now)
INTERNAL_IPS = [
    '127.0.0.1',
]

# # AMAZON S3 (keep static files there uncomment if you want)
# # COMMENT SAVE METHOD IN USERS -> MODELS PROFILE -> SAVE()
# AWS_ACCESS_KEY_ID = super_secret_informations.AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY = super_secret_informations.AWS_SECRET_ACCESS_KEY
# AWS_STORAGE_BUCKET_NAME = super_secret_informations.AWS_STORAGE_BUCKET_NAME
#
# # boto and django-storages settings
# INSTALLED_APPS += ['storages']
# # this 2 options can be necessary to uncomment depends on your AWS settings
# # AWS_S3_REGION_NAME = "eu-west-2"
# # AWS_S3_ADDRESSING_STYLE = "virtual"
# AWS_S3_FILE_OVERWRITE = False  # do not allows to overwrite files
# AWS_DEFAULT_ACL = None
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
