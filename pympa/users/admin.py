# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
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
        (_('Migration data'), {'fields': ('old_pympa_id',
                                          'old_pympa_username')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )
    add_form = PympaUserCreationForm
    form = PympaUserChangeForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff',
                    'is_active', 'ld_groups')
    # list_editable = ('first_name', 'last_name', 'is_staff', 'is_active')
    list_per_page = 25
    list_select_related = True
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    def ld_groups(self, obj):
        return '<br>'.join(
            ['<a href="{}?id={}">{}</a>'.format(
                reverse(admin_urlname(group._meta, 'changelist')),
                group.pk,
                group.name)
             for group in obj.groups.order_by('name')])
    ld_groups.allow_tags = True
    ld_groups.short_description = _('groups')


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