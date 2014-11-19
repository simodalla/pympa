# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.chrome.webdriver import WebDriver


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


class AccountsLiveTests(StaticLiveServerTestCase):

    def setUp(self):
        pass

    @classmethod
    def setUpClass(cls):
        cls.browser = WebDriver()
        super(AccountsLiveTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(AccountsLiveTests, cls).tearDownClass()

    def test_signup(self):
        self.browser.get(self.live_server_url + '/accounts/signup/')


