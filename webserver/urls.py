#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""webserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from webserver.serverapp import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', views.please_login),
    url(r'^login/(?P<username>[a-zA-Z0-9_.-]+)/(?P<password>[a-zA-Z0-9_.-]+)/$', views.login_view),
    url(r'^logout/', views.logout_view),
    url(r'^transactions/', views.get_all_transactions),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^valid_card/(?P<number>[0-9]+)/$', views.valid_card),
    url(r'^valid_transaction/(?P<number>[0-9]+)/(?P<code>[0-9]+)/(?P<amount>[-w]+)/(?P<trader>[0-9]+)/$', views.valid_transaction)
]