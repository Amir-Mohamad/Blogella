from .base import (BASE_DIR, SECRET_KEY, INSTALLED_APPS, MIDDLEWARE,
    TEMPLATES, AUTH_PASSWORD_VALIDATORS, AUTH_USER_MODEL, ROOT_URLCONF,
    WSGI_APPLICATION, LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_L10N, USE_TZ,
    STATIC_URL, STATIC_ROOT, STATICFILES_DIRS, REST_FRAMEWORK, MAX_UPLOAD_ADMIN_SIZE,
    DEFAULT_AUTO_FIELD, SIMPLE_JWT, SITE_ID, CORS_ALLOW_ALL_ORIGINS)
import os
DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': '',
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
