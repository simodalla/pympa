# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from django.test import TestCase

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.models import SocialAccount

User = get_user_model()


class AccountsTests(TestCase):

    def setUp(self):
        self.username = 'admin@example.com'
        self.password = 'default'
        User.objects.create_superuser(
            self.username, self.username, self.password)

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
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('account_logout'), follow=True)
        self.assertRedirects(response,
                             reverse('admin:logout'),
                             status_code=301)

    def test_password_change_redirect_to_admin_password_change(self):
        self.client.login(username=self.username, password=self.password)
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


class AccountsLiveTests(StaticLiveServerTestCase):

    def setUp(self):
        google = SocialApp()
        google.name = "Google"
        google.provider = "google"
        google.client_id = settings.TEST_GOOGLE_CLIENT_ID
        google.secret = settings.TEST_GOOGLE_CLIENT_SECRET
        google.save()
        google.sites.add(Site.objects.get(pk=settings.SITE_ID))

    @classmethod
    def setUpClass(cls):
        cls.driver = WebDriver()
        cls.driver.implicitly_wait(10)
        super(AccountsLiveTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(AccountsLiveTests, cls).tearDownClass()

    # def test_signup(self):
    #     self.driver.get(self.live_server_url + '/accounts/signup/')

    def test_google_login_create_local_user_if_user_not_exist(self):
        make_google_login(self.driver,
                          '{}/accounts/google/login/?next=/admin/'
                          '&process=login'.format(self.live_server_url))
        social_account = SocialAccount.objects.filter(
            user__email=settings.TEST_GOOGLE_USER_USERNAME)
        self.assertEqual(len(social_account), 1)
        user = social_account[0].user
        self.assertEqual(user.last_name, settings.TEST_GOOGLE_USER_LAST_NAME)
        self.assertEqual(user.first_name, settings.TEST_GOOGLE_USER_FIRST_NAME)

    def test_google_login_update_local_user_if_user_exist(self):
        user = User.objects.create_user(settings.TEST_GOOGLE_USER_USERNAME)
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