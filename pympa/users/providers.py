# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse

from .models import LogUnauthorizedLogin


User = get_user_model()
""":type : users.models.PympaUser"""


class PympaSocialAccountAdapter(DefaultSocialAccountAdapter):

    def _response_user_is_denied_or_inactive(self, sociallogin, reason=None):
        try:
            LogUnauthorizedLogin.objects.create(
                username=sociallogin.account.user.email, reason=reason)
        except Exception:
            pass
        return ImmediateHttpResponse(redirect(
            reverse('users:unauthorized_login')))

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.user.email
        authorized_user = sociallogin.account.user.authorized_user
        if authorized_user:
            if authorized_user.is_denied:
                # login of user denied
                raise self._response_user_is_denied_or_inactive(sociallogin,
                                                                'deny')
        else:
            # login of domain not authorized
            if not sociallogin.account.user.is_in_authorized_domain():
                raise self._response_user_is_denied_or_inactive(sociallogin,
                                                                'domain')
        try:
            local_user = User.objects.get(email=email)
            if not local_user.is_active:
                # login of user not active
                raise self._response_user_is_denied_or_inactive(sociallogin,
                                                                'notactive')
            if not sociallogin.is_existing:  # sociallogin not exist
                local_user.set_fields_from_authorized(authorized_user)
                local_user.copy_fields(sociallogin.account.user,
                                       ['last_name', 'first_name'])
                sociallogin.account.user = local_user
                sociallogin.save(request)
                User.objects.email_link_sociallogin(request, sociallogin)
        except User.DoesNotExist:
            sociallogin.account.user.set_fields_from_authorized(
                authorized_user)
            User.objects.email_new_sociallogin(request, sociallogin)


class PympaAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        # return False
        return True