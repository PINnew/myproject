# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.http import HttpResponseRedirect

urlpatterns = [
    url(r'^$', lambda request: HttpResponseRedirect('/mailing/')),
    url(r'^mailing/', include('mailing.urls')),
]
