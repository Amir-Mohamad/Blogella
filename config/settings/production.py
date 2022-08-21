import sys
sys.path.append('/usr/src/app/config/settings')
import dj_database_url
from base import (BASE_DIR, SECRET_KEY, INSTALLED_APPS, MIDDLEWARE,
    TEMPLATES, AUTH_PASSWORD_VALIDATORS, AUTH_USER_MODEL, ROOT_URLCONF,
    WSGI_APPLICATION, LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_L10N, USE_TZ,
    STATIC_URL, STATIC_ROOT, STATICFILES_DIRS, REST_FRAMEWORK, MAX_UPLOAD_ADMIN_SIZE,
    DEFAULT_AUTO_FIELD, SIMPLE_JWT, SITE_ID, CORS_ALLOW_ALL_ORIGINS)

import os
DEBUG = False
# NOTE: domain is not avalaible
ALLOWED_HOSTS = ['blogella.ir', ]

# print(os.environ.get('NAME'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('NAME'), 
        'USER':  os.environ.get('USER'), 
        'PASSWORD':  os.environ.get('PASSWORD'),
        'HOST':  os.environ.get('HOST'), 
        'PORT':  os.environ.get('PORT'),
    }
}

# print(os.environ.get('LIARA_SECRET_KEY'))
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_S3_ENDPOINT_URL = 'http://blogella.storage.iran.liara.space'
# AWS_STORAGE_BUCKET_NAME = 'blogella'
# AWS_ACCESS_KEY_ID = 'gm6dml2c51d6'
# AWS_SECRET_ACCESS_KEY = '8cfa2279-140d-4ed1-85ec-1f2f93192c58'
# AWS_S3_OBJECT_PARAMETERS = {
#   'CacheControl': 'max-age=86400',
# }

# AWS_LOCATION = 'static'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
