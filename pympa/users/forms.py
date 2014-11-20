# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import PympaUser


class PympaUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(PympaUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = PympaUser
        fields = ("email",)


class PympaUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(PympaUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = PympaUser
        fields = '__all__'