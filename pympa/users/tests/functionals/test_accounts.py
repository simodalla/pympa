# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.models import SocialAccount

from ...models import AuthorizedUser, AuthorizedDomain


User = get_user_model()
ADMINS = (('admin', 'admin@example.org'),)


class PympaUsersTests(TestCase):

    def setUp(self):
        self.email = 'admin@example.com'
        self.password = 'default'
        User.objects.create_superuser(
            self.email, self.password)

    def test_home(self):
        response = self.client.get('/', follow=True)
        self.assertRedirects(response,
                             '{}?next=/admin/'.format(reverse('admin:login')),
                             status_code=301)

    def test_login_redirect_to_admin_login(self):
        response = self.client.get(reverse('account_login'), follow=True)
        self.assertRedirects(response,
                             '{}?next=/admin/'.format(reverse('admin:login')),
                             status_code=301)

    def test_logout_redirect_to_admin_login(self):
        self.client.login(username=self.email, password=self.password)
        response = self.client.get(reverse('account_logout'), follow=True)
        self.assertRedirects(response,
                             reverse('admin:logout'),
                             status_code=301)

    def test_password_change_redirect_to_admin_password_change(self):
        self.client.login(username=self.email, password=self.password)
        response = self.client.get(reverse('account_change_password'),
                                   follow=True)
        self.assertRedirects(response,
                             reverse('admin:password_change'),
                             status_code=301)


def make_google_login(driver, url, username=None, password=None):
    username = username or settings.TEST_GOOGLE_USER_USERNAME
    password = password or settings.TEST_GOOGLE_USER_PASSWORD
    driver.get(url)
    driver.find_element_by_id('Email').send_keys(username)
    driver.find_element_by_id('Passwd').send_keys(password)
    driver.find_element_by_id('signIn').click()
    element = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.ID, 'submit_approve_access'))
    )
    element.click()


@override_settings(ADMINS=ADMINS)
class PympaUsersLiveTests(StaticLiveServerTestCase):

    def setUp(self):
        google = SocialApp()
        google.name = "Google"
        google.provider = "google"
        google.client_id = settings.TEST_GOOGLE_CLIENT_ID
        google.secret = settings.TEST_GOOGLE_CLIENT_SECRET
        google.save()
        google.sites.add(Site.objects.get(pk=settings.SITE_ID))

        self.email = settings.TEST_GOOGLE_USER_USERNAME
        self.driver = WebDriver()
        self.driver.implicitly_wait(10)
        AuthorizedDomain.objects.create(domain=self.email.split('@')[1])

    def tearDown(self):
        self.driver.quit()

    def test_google_login_create_local_user_if_user_not_exist(self):
        make_google_login(self.driver,
                          '{}/accounts/google/login/?next=/admin/'
                          '&process=login'.format(self.live_server_url))
        social_account = SocialAccount.objects.filter(user__email=self.email)
        self.assertEqual(len(social_account), 1)
        user = social_account[0].user
        self.assertEqual(user.last_name, settings.TEST_GOOGLE_USER_LAST_NAME)
        self.assertEqual(user.first_name, settings.TEST_GOOGLE_USER_FIRST_NAME)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [ADMINS[0][1]])
        self.assertIn(
            'Nuovo socialaccount di {}'.format(
                settings.TEST_GOOGLE_USER_USERNAME),
            mail.outbox[0].subject,)

    def test_google_login_update_local_user_if_user_exist(self):
        user = User.objects.create_user(self.email)
        make_google_login(self.driver,
                          '{}/accounts/google/login/?next=/admin/'
                          '&process=login'.format(self.live_server_url))
        social_account = SocialAccount.objects.filter(
            user__email=user.email)
        self.assertEqual(len(social_account), 1)
        related_user = social_account[0].user
        self.assertEqual(user.pk, related_user.pk)
        self.assertEqual(related_user.last_name,
                         settings.TEST_GOOGLE_USER_LAST_NAME)
        self.assertEqual(related_user.first_name,
                         settings.TEST_GOOGLE_USER_FIRST_NAME)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [ADMINS[0][1]])
        self.assertIn(
            'Collegamento socialaccount di {}'.format(
                settings.TEST_GOOGLE_USER_USERNAME),
            mail.outbox[0].subject)

    def test_google_login_fail_because_user_is_denied(self):
        for model in [User, SocialAccount]:
            self.assertEqual(model.objects.count(), 0)
        AuthorizedUser.objects.create(email=self.email, is_denied=True)
        make_google_login(self.driver,
                          '{}/accounts/google/login/?next=/admin/'
                          '&process=login'.format(self.live_server_url))
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.ID, 'unauthorized_login'))
        )
        self.assertEqual(
            self.driver.current_url.split(self.live_server_url)[1],
            reverse('users:unauthorized_login'))
        for model in [User, SocialAccount]:
            self.assertEqual(model.objects.count(), 0)

    def test_google_login_fail_because_user_is_not_active(self):
        user = User.objects.create_user(self.email)
        user.is_active = False
        user.save()
        make_google_login(self.driver,
                          '{}/accounts/google/login/?next=/admin/'
                          '&process=login'.format(self.live_server_url))
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.ID, 'unauthorized_login'))
        )
        self.assertEqual(
            self.driver.current_url.split(self.live_server_url)[1],
            reverse('users:unauthorized_login'))
        for model in [SocialAccount]:
            self.assertEqual(model.objects.count(), 0)

    def test_google_login_fail_because_domain_not_in_autorized(self):
        AuthorizedDomain.objects.all().delete()
        make_google_login(self.driver,
                          '{}/accounts/google/login/?next=/admin/'
                          '&process=login'.format(self.live_server_url))
        WebDriverWait(self.driver, 10).until(
            ec.element_to_be_clickable((By.ID, 'unauthorized_login'))
        )
        self.assertEqual(
            self.driver.current_url.split(self.live_server_url)[1],
            reverse('users:unauthorized_login'))
        for model in [SocialAccount]:
            self.assertEqual(model.objects.count(), 0)
