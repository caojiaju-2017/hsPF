#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""HsEduServer URL Configuration

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

from HsEdu.Api.WebCenterApi import *
from HsEdu.Api.ThirePart.WxApiHelp import *
from HsEdu.Api.Custom.CustomApi import *
# from HsEdu.Api.Chat.ChatApi import *
from HsEdu.Api.Admin.AdminApi import *
from HsEdu.Api.Game.GameApi import *

from HsEdu.Api.Game.WordInit import *
from HsEdu.Api.ThreeApi.Api import *

from HsEdu.Api.MySchool.MySchoolApi import *
from HsEdu.Api.ResourceApi import *
urlpatterns = [
    # API接口
    url(r'^admin/', admin.site.urls),
    # url(r'^$',WebCenterApi.wxA),

    url(r'^$',WebCenterApi.goHomeEx),
    url(r'^footer.html',WebCenterApi.goFooter),

    # 启动时微信登录---等待页面
    url(r'^wait.html',WebCenterApi.openWaitPage),
    # url(r'^index.html',WebCenterApi.goHome),
    url(r'^index.html',WebCenterApi.goHomeEx),

    # 微信授权
    url(r'^MP_verify_MSBMLCCIiHOH519f.txt', WebCenterApi.getWxAuthData),
    url(r'^shareToFriend',WebCenterApi.shareToFriend),


    url(r'^payCall.html',WebCenterApi.payCall),
    url(r'^paySuccess.html',WebCenterApi.paySuccess),


    # 客户api
    url(r'^api/ctm/$',CustomApi.CommandDispatch),



    # 消息页面
    url(r'^res_detail.html',CustomApi.CommandDispatch),
    url(r'^view_remark.html',CustomApi.CommandDispatch),
    # 用户dns
    url(r'^res_order.html',CustomApi.CommandDispatch),
    url(r'^order_detail_info.html', CustomApi.CommandDispatch),
    url(r'^cooperation.html', CustomApi.CommandDispatch),
    url(r'^suggest.html', CustomApi.CommandDispatch),
    url(r'^view_news.html', CustomApi.CommandDispatch),

    url(r'^uploadResFile/$', WebCenterApi.upload_res_file),
    url(r'^uploadNewsFile/$', WebCenterApi.upload_news_file),
    
    url(r'^uploadres.html', WebCenterApi.UploadRes),
    url(r'^uploadnews.html', WebCenterApi.UploadNews),
    
    # 管理页面cd
    url(r'^admin.html',AdminApi.CommandDispatch),
    url(r'^gettestData/$',AdminApi.getTestData),

    # 游戏相关-单词游戏
    url(r'^wait_game.html', WebCenterApi.openGameWaitPage),
    url(r'^wx_game_login.html', WebCenterApi.GameSwitch),
    url(r'^game_home.html', GameApi.openGameHome),
    url(r'^game_setting.html', GameApi.settingGame),
    url(r'^game_error_book.html', GameApi.openErrorBook),
    url(r'^game_map.html', GameApi.openGameMap),
    url(r'^gamming.html', GameApi.startGame),
    url(r'^game_view_word.html', GameApi.viewErrorWord),
    url(r'^api/game/$',GameApi.CommandDispatch),
    url(r'^game_result.html', GameApi.Get_Result),
    url(r'^initOne.html', WordInit.initProunce),

    # 每日
    url(r'^everydaword.html', CustomApi.everyDayWord),
    url(r'^everydaysentense.html', CustomApi.everyDaySentence),
    url(r'^everydayread.html', CustomApi.everyDayRead),

    # three test
    url(r'^three.html', Api.openHome),


    # 我的学校---移动
    url(r'^api/school/$',MySchoolApi.CommandDispatch),

    url(r'^mb_wait.html', MySchoolApi.openSchoolWaitPage),
    url(r'^introduce.html', MySchoolApi.StartIntroduce),  #移动端
    url(r'^step1.html', MySchoolApi.StartStep1),  #移动端
    url(r'^step2.html', MySchoolApi.StartStep2),  #移动端
    url(r'^mbmyschool.html', MySchoolApi.OpenSchoolHome),  #移动端
    url(r'^reg_direct_myschool.html', MySchoolApi.RegDirectLogin),  #移动端
    url(r'^mb_home.html', MySchoolApi.openHome),
    url(r'^mb_find.html', MySchoolApi.openFind),
    url(r'^mb_my.html', MySchoolApi.openMy),

    # 我的学校--电脑
    url(r'^login.html', MySchoolApi.LoginSchool),  #登陆主页
    url(r'^myschool.html', MySchoolApi.OpenSchoolPCHome),  #登陆主页

    url(r'^login_admin.html', ResourceApi.LoginAdmin),  # 登陆管理界面
    url(r'^resource.html', ResourceApi.OpenSchoolPCHome),  # 资源主页

] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)