# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .managers import PympaUserManager


@python_2_unicode_compatible
class PympaUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = PympaUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        url = reverse('admin:users_pympauser_change', args=(self.pk,))
        if not self.pk and self.email:
            url = '{}?email={}'.format(
                reverse('admin:users_pympauser_changelist'), self.email)
        return url

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = self.email
        if self.first_name and self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def copy_fields(self, source_user, fields=None):
        """
        Update fields from list param 'fields' of current User from User
        'source_user'.
        """
        fields = fields or []
        update = False
        for field in fields:
            social_field = getattr(source_user, field)
            if not (getattr(self, field) == social_field):
                setattr(self, field, social_field)
                update = True
        if update:
            self.save()
        return update

    def set_fields_from_authorized(self, authorized_user, fields=None):
        fields = fields or ['is_staff', 'is_superuser']
        for field in fields:
            setattr(self, field, getattr(authorized_user, field, False))

    @property
    def authorized_user(self):
        try:
            return AuthorizedUser.objects.get(email=self.email)
        except AuthorizedUser.DoesNotExist:
            return None

    def is_in_authorized_domain(self):
        if not self.email or '@' not in self.email:
            return False
        domain = self.email.split('@')[1]
        try:
            AuthorizedDomain.objects.get(domain=domain)
            return True
        except AuthorizedDomain.DoesNotExist:
            return False


class AuthorizedDomain(models.Model):
    domain = models.CharField(_('domain'), max_length=254, unique=True)

    class Meta:
        verbose_name = _('authorized domain')
        verbose_name_plural = _('authorized domains')


class AuthorizedUser(models.Model):
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_superuser = models.BooleanField(
        _('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))
    is_denied = models.BooleanField(
        _('deny status'), default=False,
        help_text=_('Designates that this user is denied to login.'))

    class Meta:
        verbose_name = _('authorized user')
        verbose_name_plural = _('authorized users')


UNAUTHORIZED_REASONS = (
    ('domain', _('Domain Unauthorized')),
    ('notactive', _('User Not Active')),
    ('deny', _('User Denied')),
)


class LogUnauthorizedLogin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=254)
    reason = models.CharField(max_length=254, choices=UNAUTHORIZED_REASONS,
                              null=True)

    class Meta:
        verbose_name = _('log unauthorized login')
        verbose_name_plural = _('log unauthorized logins')