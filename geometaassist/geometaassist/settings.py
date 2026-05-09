"""
Django settings for geometaassist project.
"""

import os
from pathlib import Path

from django.contrib.messages import constants as message_constants
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env')


SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-0)x_bla)qx&lq#u*y%9o3o!s3^1ohe4)@%53n^x994dixo1z35',
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes')

ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    'https://infs3202-414ae30f.uqcloud.net'
]

# Tells Django that the UQCloud load balancer handles SSL termination.
# Requests arrive at Gunicorn as plain HTTP internally, but this header
# tells Django to treat them as HTTPS so secure cookies and redirects work correctly.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Ensures session and CSRF cookies are only sent over HTTPS in production.
# Set to False locally (when DEBUG=True) so plain HTTP dev server still works.
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Prevents JavaScript from reading the session cookie, mitigating session
# theft via XSS attacks.
SESSION_COOKIE_HTTPONLY = True

# Prevents the app from being embedded in an iframe on other sites,
# mitigating clickjacking attacks.
X_FRAME_OPTIONS = 'DENY'

# Prevents browsers from guessing (sniffing) the content type of responses,
# which can prevent certain XSS attacks via uploaded files.
SECURE_CONTENT_TYPE_NOSNIFF = True


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'accounts',
    'projects',
    'billing',
    'metadata',
    'mockup',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'geometaassist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'geometaassist.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'geometaassist'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'mockpassword'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}


AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = os.environ.get('DJANGO_STATIC_URL', '/geometaassist_static/')
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = '/var/www/htdocs/geometaassist_static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MESSAGE_TAGS = {
    message_constants.DEBUG:   'secondary',
    message_constants.INFO:    'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR:   'danger',
}


OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
CHROMA_PERSIST_DIR = os.environ.get(
    'CHROMA_PERSIST_DIR',
    str(BASE_DIR / 'rag' / 'chroma_store'),
)
