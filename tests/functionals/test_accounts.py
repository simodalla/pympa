# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase, TestCase
from django.contrib.auth.models import User

from selenium.webdriver.chrome.webdriver import WebDriver


class AccountsTests(TestCase):

    def setUp(self):
        pass

    def test_login_redirect_to_admin_login(self):
        response = self.client.get('/accounts/login/', follow=True)
        self.assertRedirects(response,
                             '{}?next=/admin/'.format(reverse('admin:login')),
                             status_code=301)


# class AccountsLiveTests(LiveServerTestCase):
#
#     def setUp(self):
#         pass
#
#     @classmethod
#     def setUpClass(cls):
#         cls.browser = WebDriver()
#         super(AccountsLiveTests, cls).setUpClass()
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.browser.quit()
#         super(AccountsLiveTests, cls).tearDownClass()
#
#     def test_login_redirect_to_admin_login(self):
#         self.browser.get('/accounts/login/')


