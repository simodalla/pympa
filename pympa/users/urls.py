# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = patterns(
    '',
    url(r'^login/$', RedirectView.as_view(url='/admin/'), name='login'),
)
