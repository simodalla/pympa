# -*- coding: utf-8 -*-
'''
Local Configurations

- Runs in Debug mode
- Uses console backend for emails
- Use Django Debug Toolbar
'''
from configurations import values

from .common import Common


class Local(Common):

    # DEBUG
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG
    # END DEBUG

    # INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    # END INSTALLED_APPS

    # Mail settings
    EMAIL_HOST = "smtp-relay.gmail.com"
    EMAIL_PORT = 465
    EMAIL_BACKEND = values.Value(
        'django.core.mail.backends.console.EmailBackend')
    # End mail settings

    # django-debug-toolbar
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + (
        'debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    # end django-debug-toolbar

    # Your local stuff: Below this line define 3rd party libary settings

    TEST_GOOGLE_USER_USERNAME = values.SecretValue()
    TEST_GOOGLE_USER_PASSWORD = values.SecretValue()
    TEST_GOOGLE_USER_LAST_NAME = 'demo_djangogoogleapps'
    TEST_GOOGLE_USER_FIRST_NAME = 'demo_djangogoogleapps'
    TEST_GOOGLE_CLIENT_ID = values.SecretValue()
    TEST_GOOGLE_CLIENT_SECRET = values.SecretValue()

    ##### openheldesk #####
    PACKAGE_NAME_FILEBROWSER = 'filebrowser_safe'
    GRAPPELLI_INSTALLED = True
    TESTING = None