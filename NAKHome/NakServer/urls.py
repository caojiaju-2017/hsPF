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


    url(r'^newsDetail_102645.html', WebCenterApi.openNews102645),
    url(r'^newsDetail_102648.html', WebCenterApi.openNews102648),
    url(r'^newsDetail_102651.html', WebCenterApi.openNews102651),
    url(r'^newsDetail_102653.html', WebCenterApi.openNews102653),
    url(r'^newsDetail_102656.html', WebCenterApi.openNews102656),
    url(r'^newsDetail_102659.html', WebCenterApi.openNews102659),
    url(r'^newsDetail_102662.html', WebCenterApi.openNews102662),


] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)