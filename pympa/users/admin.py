# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import (PympaUser, AuthorizedDomain, AuthorizedUser,
                     LogUnauthorizedLogin)
from .forms import PympaUserChangeForm, PympaUserCreationForm


@admin.register(PympaUser)
class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = PympaUserChangeForm
    add_form = PympaUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(AuthorizedDomain)
class AuthorizedDomainAdmin(admin.ModelAdmin):
    list_display = ('domain',)


@admin.register(AuthorizedUser)
class AuthorizedUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_denied', 'is_staff', 'is_superuser',)


@admin.register(LogUnauthorizedLogin)
class LogUnauthorizedLoginAdmin(admin.ModelAdmin):
    list_display = ('username', 'reason', 'created', )

# admin.site.register(PympaUser, CustomUserAdmin)