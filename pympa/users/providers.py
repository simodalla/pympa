# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
import ipdb
from django.http import HttpResponse, HttpResponseRedirect
from allauth.exceptions import ImmediateHttpResponse


class PympaSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self,
                      request,
                      sociallogin,
                      data):
        print("start populate_user")
        print(sociallogin, data)
        p = super(PympaSocialAccountAdapter, self).populate_user(
            request, sociallogin, data)
        p.username = data.get('email').split('@')[0]
        print(type(p), p)
        print("end populate_user")
        return p

    def new_user(self, request, sociallogin):
        print("start new_user")
        nu = super(PympaSocialAccountAdapter, self).new_user(request,
                                                             sociallogin)
        print(type(nu), nu)
        print("end new_user")
        return nu

    def save_user(self, request, sociallogin, form=None):
        print("start save_user")
        su = super(PympaSocialAccountAdapter, self).save_user(
            request, sociallogin, form=form)
        print(type(su), su)
        print("end save_user")
        return su
    #
    # def get_connect_redirect_url(self, request, socialaccount):
    #     # import ipdb
    #     # ipdb.set_trace()
    #     result = super(PympaSocialAccountAdapter,
    #                    self).get_connect_redirect_url(request, socialaccount)
    #     return result

    def pre_social_login(self, request, sociallogin):
        # import ipdb
        # ipdb.set_trace()
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            print("************************************")
            print("#####", sociallogin.is_existing)
            if not sociallogin.is_existing:
                sociallogin.account.user = User.objects.get(
                    email=sociallogin.account.user.email)
                sociallogin.save(request)
                import ipdb
                ipdb.set_trace()
        except User.DoesNotExist:
            pass
        # raise ImmediateHttpResponse(HttpResponse('Closed for the day'))
        # raise ImmediateHttpResponse(HttpResponseRedirect('/pippo/'))




class PympaAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        # return False
        return True

    # def new_user(self, request):
    #     print("start PympaAccountAdapter new_user")
    #     n_u = super(PympaAccountAdapter, self).new_user(request)
    #     print(n_u)
    #     print("stop PympaAccountAdapter new_user")
    #     return n_u
    #
    # def save_user(self, request, user, form, commit=True):
    #     print("start PympaAccountAdapter save_user")
    #     s_u = super(PympaAccountAdapter, self).save_user(
    #         request, user, form, commit=commit)
    #     print(s_u)
    #     print("stop PympaAccountAdapter save_user")
    #     return s_u
        