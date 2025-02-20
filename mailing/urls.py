# -*- coding: utf-8 -*-
from django.conf.urls import url  # Используем url вместо path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  # Ваши другие пути...
    url(r'^create_newsletter/$', views.create_newsletter, name='create_newsletter'),
    url(r'^email_opened/(?P<newsletter_id>\d+)/(?P<subscriber_id>\d+)/$', views.email_opened, name='email_opened'),
    url(r'^track/open/(?P<newsletter_id>\d+)/(?P<subscriber_id>\d+)/$', views.track_open, name='track_open'),
    url(r'^track/click/(?P<newsletter_id>\d+)/(?P<subscriber_id>\d+)/$', views.track_click, name='track_click'),
]