# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth import get_user_model


from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter

User = get_user_model()
""":type : users.models.PympaUser"""


class PympaSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        try:
            if not sociallogin.is_existing:
                local_user = User.objects.get(
                    email=sociallogin.account.user.email)
                local_user.copy_fields(sociallogin.account.user,
                                       ['last_name', 'first_name'])
                sociallogin.account.user = local_user
                sociallogin.save(request)
        except User.DoesNotExist:
            User.objects.email_new_sociallogin(request, sociallogin)

        # raise ImmediateHttpResponse(HttpResponse('Closed for the day'))
        # raise ImmediateHttpResponse(HttpResponseRedirect('/pippo/'))


class PympaAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        # return False
        return True