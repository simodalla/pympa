# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

from users import views

url_home = '%s/' % settings.SITE_PREFIX
url_admin = '%s/admin/' % settings.SITE_PREFIX

urlpatterns = patterns(
    '',
    url(r'^$',  # noqa
        RedirectView.as_view(url='/%s' % url_home), name='root'),
    url(r'^{}$'.format(url_home),  # noqa
        RedirectView.as_view(url='/%s' % url_admin), name='home'),
    url(r'^{}/password_reset/$'.format(settings.SITE_PREFIX),
        views.AdminPasswordResetRedirectView.as_view(),
        name='admin_password_reset'),

    # admin
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^{}/grappelli/'.format(settings.SITE_PREFIX),
        include('grappelli.urls')),  # grappelli URLS
    url(r'^{}'.format(url_admin), include(admin.site.urls)),

    # User management
    url(r'^{}/accounts/'.format(settings.SITE_PREFIX),
        include('users.urls', namespace='users')),
    url(r'^{}/accounts/'.format(settings.SITE_PREFIX),
        include('allauth.urls')),

    # Uncomment the next line to enable avatars
    # url(r'^avatar/', include('avatar.urls')),

    # Your stuff: custom urls go here

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE