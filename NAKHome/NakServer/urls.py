#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""NakServer URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from Nak.Api.WebCenterApi import *

urlpatterns = [
    # API接口
    url(r'^admin/', admin.site.urls),
    url(r'^$',WebCenterApi.openHome),

    url(r'^about.html', WebCenterApi.openAbout),
    url(r'^contect.html', WebCenterApi.openContect),
    url(r'^hr.html', WebCenterApi.openHr),
    url(r'^index.html', WebCenterApi.openHome),
    url(r'^news.html', WebCenterApi.openNews),
    url(r'^product.html', WebCenterApi.openProduct),
    url(r'^service.html', WebCenterApi.openService),
    url(r'^footer.html', WebCenterApi.openFooter),

    url(r'^newsDetail_102624.html', WebCenterApi.openNews102624),
    url(r'^newsDetail_102627.html', WebCenterApi.openNews102627),
    url(r'^newsDetail_102630.html', WebCenterApi.openNews102630),
    url(r'^newsDetail_102632.html', WebCenterApi.openNews102632),
    url(r'^newsDetail_102635.html', WebCenterApi.openNews102635),
    url(r'^newsDetail_102637.html', WebCenterApi.openNews102637),
    url(r'^newsDetail_102640.html', WebCenterApi.openNews102640),
    url(r'^newsDetail_102643.html', WebCenterApi.openNews102643),
    url(r'^newsDetail_102645.html', WebCenterApi.openNews102645),
    url(r'^newsDetail_102648.html', WebCenterApi.openNews102648),
    url(r'^newsDetail_102651.html', WebCenterApi.openNews102651),
    url(r'^newsDetail_102653.html', WebCenterApi.openNews102653),
    url(r'^newsDetail_102656.html', WebCenterApi.openNews102656),
    url(r'^newsDetail_102659.html', WebCenterApi.openNews102659),
    url(r'^newsDetail_102662.html', WebCenterApi.openNews102662),
    url(r'^newsDetail_102665.html', WebCenterApi.openNews102665),
    url(r'^newsDetail_102672.html', WebCenterApi.openNews102672),
    url(r'^newsDetail_102675.html', WebCenterApi.openNews102675),
    url(r'^newsDetail_102678.html', WebCenterApi.openNews102678),
    url(r'^newsDetail_102682.html', WebCenterApi.openNews102682),
    url(r'^newsDetail_102685.html', WebCenterApi.openNews102685),
    url(r'^newsDetail_102688.html', WebCenterApi.openNews102688),
    url(r'^newsDetail_102690.html', WebCenterApi.openNews102690),
    url(r'^newsDetail_102694.html', WebCenterApi.openNews102694),
    url(r'^newsDetail_103736.html', WebCenterApi.openNews103736),
    url(r'^newsDetail_103740.html', WebCenterApi.openNews103740),
    url(r'^newsDetail_103744.html', WebCenterApi.openNews103744),
    url(r'^newsDetail_103746.html', WebCenterApi.openNews103746),
    url(r'^newsDetail_103750.html', WebCenterApi.openNews103750),
    url(r'^newsDetail_103903.html', WebCenterApi.openNews103903),

] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)