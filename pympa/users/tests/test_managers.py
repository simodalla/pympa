# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import unittest
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import RequestFactory


User = get_user_model()
""":type : users.models.PympaUser"""


class TestSocialPympaUserManager(unittest.TestCase):

    def setUp(self):
        self.url = '/users/1/'
        self.email = 'user@example.org'
        self.mock_user = mock.MagicMock(spec=User, email=self.email)
        # self.mock_user.email = self.email
        self.mock_user.get_absolute_url.return_value = self.url
        self.mock_sociallogin = mock.MagicMock()
        self.mock_sociallogin.account.user = self.mock_user
        self.mock_request = mock.MagicMock()
        self.factory = RequestFactory()
        self.request = self.factory.get(self.url)

    def tearDown(self):
        self.mock_user.reset_mock()
        self.mock_sociallogin.reset_mock()

    @mock.patch('users.managers.mail_admins')
    def test_email_new_sociallogin_send_email(self, mock_mail_admins):
        User.objects.email_new_sociallogin(self.request,
                                           self.mock_sociallogin)
        mock_mail_admins.assert_called_once_with(
            'Nuovo socialaccount di {}'.format(self.email),
            mock.ANY, fail_silently=True, html_message=mock.ANY)
        self.mock_user.get_absolute_url.assert_called_once()
