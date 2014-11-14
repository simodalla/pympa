# # # -*- coding: utf-8 -*-
# from django.contrib import admin
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
# # import copy
# # from .models import PympaUser
# # from .forms import PympaUserCreationForm
# # # from django.utils.translation import ugettext_lazy as _
# # #
# # # #
# # # #
# # # class EmailUserAdmin(AuthUserAdmin):
# # #     ordering = ('email',)
# # #     fieldsets = (
# # #             (None, {'fields': ('email', 'password')}),
# # #             (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
# # #             (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
# # #                                            'groups', 'user_permissions')}),
# # #             (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
# # #         )
# # #     add_fieldsets = (
# # #         (None, {
# # #             'classes': ('wide',),
# # #             'fields': ('email', 'password1', 'password2'),
# # #         }),
# # #     )
# # #     list_display = ('email', 'first_name', 'last_name', 'is_staff')
# # #     list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
# # #     search_fields = ('first_name', 'last_name', 'email')
# # #
# #
# #
# # class PympaUserAdmin(AuthUserAdmin):
# #     fieldsets = (list(copy.deepcopy(AuthUserAdmin.fieldsets)) +
# #                  [('Pympa altri...', {'fields': ('old_pympa_id',)})])
# #     add_form = PympaUserCreationForm
# #
# #
# # admin.site.register(PympaUser, PympaUserAdmin)
#
# from django import forms
# from django.contrib.auth import get_user_model
# User = get_user_model()
#
# from django.core.validators import validate_email
#
# class PympaUserCreationForm(UserCreationForm):
#
#     def __init__(self, *args, **kwargs):
#         super(PympaUserCreationForm, self).__init__(*args, **kwargs)
#         print(self.fields)
#         self.fields['username'].validators.append(validate_email)
#         for f in self.fields:
#             print(f, self.fields[f].validators)
#
#
# class PympaUserChangeForm(UserChangeForm):
#
#     def __init__(self, *args, **kwargs):
#         super(PympaUserChangeForm, self).__init__(*args, **kwargs)
#         print(self.fields)
#         self.fields['username'].validators.append(validate_email)
#         self.fields['username'].label = 'Email'
#         for f in self.fields:
#             print(f, self.fields[f].validators)
#
#     # def clean_username(self):
#     #     # Since User.username is unique, this check is redundant,
#     #     # but it sets a nicer error message than the ORM. See #13147.
#     #     username = self.cleaned_data["username"]
#     #     try:
#     #         User._default_manager.get(username=username)
#     #     except User.DoesNotExist:
#     #         return username
#     #     raise forms.ValidationError(
#     #         self.error_messages['duplicate_username'],
#     #         code='duplicate_username',
#     #     )
#     #
#     # def save(self, commit=True):
#     #     user = super(UserCreationForm, self).save(commit=False)
#     #     user.set_password(self.cleaned_data["password1"])
#     #     if commit:
#     #         user.
#     #     return user
#
#
# class PympaUserAdmin(AuthUserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
#     add_form = PympaUserCreationForm
#     form = PympaUserChangeForm
#
#
# admin.site.unregister(User)
# admin.site.register(User, PympaUserAdmin)