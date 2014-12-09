# -*- coding: utf-8 -*-
"""
Django settings for pympa project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os.path import join, dirname

from configurations import Configuration, values


BASE_DIR = dirname(dirname(__file__))


class Common(Configuration):

    SITE_PREFIX = 'pympa'

    # APP CONFIGURATION
    DJANGO_APPS = (
        # Default Django apps:
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Useful template tags:
        # 'django.contrib.humanize',
    )
    ADMIN_APPS = (
        # Admin
        'autocomplete_light',
        'grappelli',
        'django.contrib.admin',
    )
    THIRD_PARTY_APPS = (
        # 'crispy_forms',  # Form layouts
        # 'avatar',  # for user avatars
        'allauth',  # registration
        'allauth.account',  # registration
        'allauth.socialaccount',  # registration
        'allauth.socialaccount.providers.google',
    )

    # Apps specific for this project go here.
    LOCAL_APPS = (
        'users',  # custom users app
        # Your stuff: custom apps go here
        'pympa_core',
        'pympa_affarigenerali',
        'pympa_registrum',
        'openhelpdesk',
        'mezzanine.conf',
        'mezzanine.core'
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
    INSTALLED_APPS = DJANGO_APPS + ADMIN_APPS + THIRD_PARTY_APPS + LOCAL_APPS
    # END APP CONFIGURATION

    # MIDDLEWARE CONFIGURATION
    MIDDLEWARE_CLASSES = (
        # Make sure djangosecure.middleware.SecurityMiddleware is listed first
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
    # END MIDDLEWARE CONFIGURATION

    # MIGRATIONS CONFIGURATION
    MIGRATION_MODULES = {
        'sites': 'contrib.sites.migrations'
    }
    # END MIGRATIONS CONFIGURATION

    # DEBUG
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.BooleanValue(False)

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    # SECRET CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    # Note: This key only used for development and testing.
    #       In production, this is changed to a values.SecretValue() setting
    SECRET_KEY = "1234567890!=*"
    # END SECRET CONFIGURATION

    # FIXTURE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
    # FIXTURE_DIRS = (
    #     join(BASE_DIR, 'fixtures'),
    # )
    # END FIXTURE CONFIGURATION

    # EMAIL CONFIGURATION
    # EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    # END EMAIL CONFIGURATION

    # MANAGER CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
    ADMINS = (
        ("""Simone Dalla""", 'simodalla@gmail.com'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
    MANAGERS = ADMINS
    # END MANAGER CONFIGURATION

    # DATABASE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = values.DatabaseURLValue('postgres://localhost/pympa7',
                                        alias='default')
    # END DATABASE CONFIGURATION

    # CACHING
    # Do this here because thanks to django-pylibmc-sasl and pylibmc
    # memcacheify (used on heroku) is painful to install on windows.
    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #         'LOCATION': ''
    #     }
    # }
    # END CACHING

    # GENERAL CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
    TIME_ZONE = 'Europe/Rome'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
    LANGUAGE_CODE = 'it-it'
    # LANGUAGE_CODE = 'en'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
    SITE_ID = 1

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
    USE_I18N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
    USE_L10N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
    USE_TZ = True
    # END GENERAL CONFIGURATION

    # TEMPLATE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        # Your stuff: custom template context processers go here
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",
        'pympa_core.context_processors.admin_interface'
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_DIRS = (
        join(BASE_DIR, 'templates'),
    )

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    # See: http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    # END TEMPLATE CONFIGURATION

    # STATIC FILE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = '/{}/static/'.format(SITE_PREFIX)

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    STATICFILES_DIRS = (
        join(BASE_DIR, 'assets'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    # END STATIC FILE CONFIGURATION

    # MEDIA CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = join(BASE_DIR, 'media')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = '/{}/media/'.format(SITE_PREFIX)
    # END MEDIA CONFIGURATION

    # URL Configuration
    ROOT_URLCONF = 'urls'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
    WSGI_APPLICATION = 'wsgi.application'
    # End URL Configuration

    # SLUGLIFIER
    # AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"
    # END SLUGLIFIER

    # LOGGING CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d'
                          ' %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }
    # more details on how to customize your logging configuration.
    # END LOGGING CONFIGURATION

    # Your common stuff: Below this line define 3rd party library settings

    # ADMIN SITE CONFIGURATION
    ADMIN_SITE_HEADER = 'PymPA'
    ADMIN_SITE_TITLE = 'PymPA'
    ADMIN_INDEX_TITLE = 'Gestisci i tuoi moduli di PymPA'

    # GRAPELLI CONFIGURATION
    GRAPPELLI_ADMIN_TITLE = ADMIN_SITE_HEADER

    # AUTHENTICATION CONFIGURATION
    AUTH_USER_MODEL = 'users.PympaUser'
    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",
    )
    # Some really nice defaults
    ACCOUNT_AUTHENTICATION_METHOD = "email"
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'

    #  Custom user app defaults
    LOGIN_REDIRECT_URL = '/'
    LOGIN_URL = '/{}/admin/'.format(SITE_PREFIX)
    # END Custom user app defaults

    # ACCOUNT_ADAPTER = "users.providers.PympaAccountAdapter"
    SOCIALACCOUNT_ADAPTER = "users.providers.PympaSocialAccountAdapter"
    SOCIALACCOUNT_QUERY_EMAIL = True
    SOCIALACCOUNT_PROVIDERS = {
        'google': {
            'SCOPE': ['profile', 'email'],
            'AUTH_PARAMS': {'access_type': 'online'}}
    }
    # END AUTHENTICATION CONFIGURATION