# -*- coding: utf-8 -*-

from django.views.generic import RedirectView, TemplateView
from django.core.urlresolvers import reverse


class AccountsLoginRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('admin:index')


class AccountsLogoutRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('admin:logout')


class AccountsPasswordChangeView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('admin:password_change')


class AccountsInactiveRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('admin:index')


class AdminPasswordResetRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('account_reset_password')


class UnauthorizedLogin(TemplateView):

    template_name = 'users/unauthorized_login.html'