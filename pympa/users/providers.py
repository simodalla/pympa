# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


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
        # import ipdb
        # ipdb.set_trace()
        print("end save_user")
        return su