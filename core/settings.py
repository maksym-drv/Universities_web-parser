"""
Django settings for core project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from datetime import datetime
from selenium.webdriver import FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',') if \
    os.environ.get('ALLOWED_HOSTS') else ['localhost']

CSRF_TRUSTED_ORIGINS = os.environ['CSRF_TRUSTED_ORIGINS'].split(',') if \
    os.environ.get('CSRF_TRUSTED_ORIGINS') else ['http://localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'webparser.data',
    'webparser.options',
    'webparser.templates',
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates')), ],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'), 
        'USER': os.environ.get('DB_USER'), 
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'), 
        'PORT': os.environ.get('DB_PORT'),
    }
}

AUTH_USER_MODEL = 'accounts.CustomUser'
LOGIN_REDIRECT_URL = '/templates'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery
CELERY_BROKER_URL       = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND   = os.environ.get('CELERY_RESULT_BACKEND')
CELERY_RESULT_EXTENDED  = os.environ.get('CELERY_RESULT_EXTENDED')
CELERY_TASK_TRACK_STARTED = os.environ.get('CELERY_TASK_TRACK_STARTED')

# Parser

TARGET_URL = lambda year = datetime.now().year: \
    'https://vstup2022.edbo.gov.ua/offers/' if \
    year == datetime.now().year else f'https://vstup{year}.edbo.gov.ua/offers/' 

REGIONS_URL = 'https://registry.edbo.gov.ua/files/regions.xlsx'
SPECIALITIES_URL = 'https://registry.edbo.gov.ua/files/specialities.xlsx'
UNIVERSITIES_URL = 'https://registry.edbo.gov.ua/api/universities/'

DEFAULT_PARAMS = {
    'ut': 1,
    'exp': 'json'
}

OPTIONS_ROOT = os.path.join(BASE_DIR, 'webparser/options/')

if os.environ.get('AM_I_IN_DOCKER'):

    FIREFOX_OPTIONS = FirefoxOptions()
    FIREFOX_OPTIONS.add_argument('--headless')
    FIREFOX_OPTIONS.add_argument('--mute-audio')
    FIREFOX_OPTIONS.add_argument('--no-sandbox')
    FIREFOX_OPTIONS.add_argument('--disable-dev-shm-usage')

    EXECUTABLE_PATH = GeckoDriverManager().install()