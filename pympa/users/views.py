# -*- coding: utf-8 -*-

from django.views.generic import RedirectView
from django.core.urlresolvers import reverse


class LoginRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('admin:index')


class LogoutRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('admin:logout')