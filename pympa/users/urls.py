# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^login/$',  views.LoginRedirectView.as_view()),
    url(r'^logout/$', views.LogoutRedirectView.as_view()),
)
