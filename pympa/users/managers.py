# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import BaseUserManager
from django.core.mail import mail_admins
from django.template import loader, Context
from django.utils import timezone
from django.utils.html import strip_tags


class PympaUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

    def _email_for_sociallogin(self, subject, template, context=None):
        context = context or {}
        message = loader.get_template(template).render(Context(context))
        mail_admins(subject,
                    strip_tags(message).lstrip('\n'),
                    fail_silently=True,
                    html_message=message)

    def email_new_sociallogin(self, request, sociallogin):
        user = sociallogin.account.user
        """:type : users.models.PympaUser"""
        context = {'email': user.email,
                   'user_url': request.build_absolute_uri(
                       user.get_absolute_url())}
        subject = 'Nuovo socialaccount di {}'.format(user.email)
        return self._email_for_sociallogin(
            subject, "users/email/new_sociallogin.html", context)

    def email_link_sociallogin(self, request, sociallogin):
        user = sociallogin.account.user
        """:type : users.models.PympaUser"""
        context = {'email': user.email,
                   'user_url': request.build_absolute_uri(
                       user.get_absolute_url())}
        subject = 'Collegamento socialaccount di {}'.format(user.email)
        return self._email_for_sociallogin(
            subject, "users/email/link_sociallogin.html", context)
