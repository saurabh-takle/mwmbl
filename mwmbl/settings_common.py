"""
Django settings for mwmbl project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from urllib.parse import urlparse

import sentry_sdk

from mwmbl.auth import require_email_confirmation

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'mwmbl',
    'django_htmx',
    'django_vite',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'ninja_extra',
    'debug_toolbar',
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "django_htmx.middleware.HtmxMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'mwmbl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mwmbl.wsgi.application'


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

DJANGO_VITE_DEV_MODE = False


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]


AUTH_USER_MODEL = "mwmbl.MwmblUser"


ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

DEFAULT_FROM_EMAIL = "admin@mwmbl.org"

LOGIN_REDIRECT_URL = "/"

FOOTER_LINKS = [
    {
        "name": "Donate",
        "icon": "ph-currency-dollar-bold",
        "href": "https://opencollective.com/mwmbl",
    },
    {
        "name": "Matrix",
        "icon": "ph-chat-circle-text-bold",
        "href": "https://matrix.to/#/#mwmbl:matrix.org",
    },
    {
        "name": "Book",
        "icon": "ph-book-bold",
        "href": "https://book.mwmbl.org",
    },
    {
        "name": "Blog",
        "icon": "ph-browser-bold",
        "href": "https://blog.mwmbl.org",
    },
    {
        "name": "GitHub",
        "icon": "ph-github-logo-bold",
        "href": "https://github.com/mwmbl/mwmbl",
    },
    {
        "name": "YouTube",
        "icon": "ph-youtube-logo-bold",
        "href": "https://www.youtube.com/@mwmbl",
    },
    {
        "name": "Discord",
        "icon": "ph-discord-logo-bold",
        "href": "https://discord.gg/2BGSUYFdkD",
    },


]

BATCH_DIR_NAME = 'batches'

DATA_UPLOAD_MAX_NUMBER_FIELDS = None


SETUP_DATABASE = True


SENTRY_DSN = os.environ.get("SENTRY_DSN")

if SENTRY_DSN is not None:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for tracing.
        traces_sample_rate=0.1,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=0.1,
        send_default_pii=False,
        before_send=lambda event, hint: strip_query_string(event),
    )
else:
    print("No SENTRY_DSN set, skipping Sentry initialization")


def strip_query_string(event):
    request = event.get("request")
    if request and "url" in request:
        parsed = urlparse(request["url"])
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        event["request"]["url"] = clean_url
        if "query_string" in request:
            del event["request"]["query_string"]
    return event

# Django ninja-jwt settings - custom auth rule
USER_AUTHENTICATION_RULE = require_email_confirmation

# Redis configuration
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")

INTERNAL_IPS = [
    "127.0.0.1",
]
