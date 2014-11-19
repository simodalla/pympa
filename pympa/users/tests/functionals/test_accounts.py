# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.chrome.webdriver import WebDriver


class AccountsTests(TestCase):

    def setUp(self):
        pass

    def test_home(self):
        response = self.client.get('/', follow=True)
        self.assertRedirects(response,
                             '{}?next=/admin/'.format(reverse('admin:login')),
                             status_code=301)

    def test_login_redirect_to_admin_login(self):
        response = self.client.get('/accounts/login/', follow=True)
        self.assertRedirects(response,
                             '{}?next=/admin/'.format(reverse('admin:login')),
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


