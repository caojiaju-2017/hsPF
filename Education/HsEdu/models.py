#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TEMPLATE_DIRS ['E:\\GitWorkSpace\\NewEducation\\4.Code\\Education\\HsEdu\\templates']
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class HsOrders(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    usercode = models.CharField(db_column='UserCode', max_length=32, blank=True,null=True)  # Field name made lowercase.
    ordertime = models.DateTimeField(db_column='OrderTime', blank=True, null=True)  # Field name made lowercase.
    goodscode = models.CharField(db_column='GoodsCode', max_length=32, blank=True,null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    count = models.IntegerField(db_column='Count', blank=True, null=True)  # Field name made lowercase.
    downloadinfo = models.CharField(db_column='DownLoadInfo', max_length=1024, blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_orders'


class HsRelaxReply(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    relaxcode = models.CharField(db_column='RelaxCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    sendcode = models.CharField(db_column='SendCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    info = models.TextField(db_column='Info', blank=True, null=True)  # Field name made lowercase.
    replytime = models.DateTimeField(db_column='ReplyTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_relax_reply'


class HsResources(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True, null=True)  # Field name made lowercase.
    resgrade = models.CharField(db_column='ResGrade', max_length=32, blank=True, null=True)  # Field name made lowercase.
    resclass = models.CharField(db_column='ResClass', max_length=32, blank=True,  null=True)  # Field name made lowercase.
    reslevel = models.CharField(db_column='ResLevel', max_length=32, blank=True,null=True)  # Field name made lowercase.

    restitle = models.CharField(db_column='ResTitle', max_length=64, blank=True, null=True)  # Field name made lowercase.
    resinfo = models.CharField(db_column='ResInfo', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    resimage = models.CharField(db_column='ResImage', max_length=32, blank=True, null=True)  # Field name made lowercase.

    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=32, blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='ViewCount', blank=True, null=True)  # Field name made lowercase.
    orgname = models.CharField(db_column='OrgName', max_length=64, blank=True, null=True)  # Field name made lowercase.
    orgimage = models.CharField(db_column='OrgImage', max_length=64, blank=True, null=True)  # Field name made lowercase.
    orginfo = models.CharField(db_column='OrgInfo', max_length=640, blank=True, null=True)  # Field name made lowercase.
    previewurl = models.CharField(db_column='PreviewUrl', max_length=480, blank=True,null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'hs_resources'


class HsResourceInfo(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    rescode = models.CharField(db_column='ResCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    index = models.IntegerField(db_column='Index', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=64, blank=True, null=True)  # Field name made lowercase.
    introduce = models.CharField(db_column='Introduce', max_length=2000, blank=True,null=True)  # Field name made lowercase.
    restype = models.IntegerField(db_column='ResType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_resource_info'


class HsResourcesSecretInfo(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    rescode = models.CharField(db_column='ResCode', max_length=64, blank=True, null=True)  # Field name made lowercase.
    downloadurl = models.CharField(db_column='DownloadUrl', max_length=2000, blank=True,null=True)  # Field name made lowercase.
    dlpsswd = models.CharField(db_column='DLPsswd', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_resource_secret'


class HsCustom(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    wxaccount = models.CharField(db_column='WxAccount', max_length=64, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    headimage = models.CharField(db_column='HeadImage', max_length=2000, blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_custom'


class HsNews(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    urlname = models.CharField(db_column='UrlName', max_length=32, blank=True, null=True)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=32, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=32, blank=True, null=True)  # Field name made lowercase.
    newstime = models.CharField(db_column='NewsTime', max_length=20, blank=True,null=True)  # Field name made lowercase.
    info = models.CharField(db_column='Info', max_length=256, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_news'


class HsSuggests(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=64, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    usercode = models.CharField(db_column='UserCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    reltime = models.DateTimeField(db_column='RelTime', blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_suggests'

class HsResRemark(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    rcode = models.CharField(db_column='RCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    usercode = models.CharField(db_column='UserCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=64, blank=True,null=True)  # Field name made lowercase.
    reltime = models.CharField(db_column='RelTime', max_length=20, blank=True,null=True)  # Field name made lowercase.
    
    type = models.IntegerField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'hs_res_remark'


class HsSysConfig(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True, null=True)  # Field name made lowercase.
    orgcode = models.CharField(db_column='OrgCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    ckey = models.CharField(db_column='CKey', max_length=32, blank=True, null=True)  # Field name made lowercase.
    cvalue = models.CharField(db_column='CValue', max_length=128, blank=True, null=True)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=4, blank=True, null=True)  # Field name made lowercase.
    ctype = models.IntegerField(db_column='CType', blank=True, null=True)  # Field name made lowercase.
    cexpress = models.CharField(db_column='CExpress', max_length=1024, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_sys_config'


class HsWxTicket(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    ticket = models.CharField(db_column='Ticket', unique=True, max_length=64, blank=True,null=True)  # Field name made lowercase.
    signtime = models.CharField(db_column='SignTime', max_length=32, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.CharField(db_column='TimeStamp', max_length=32, blank=True,null=True)  # Field name made lowercase.
    noncestr = models.CharField(db_column='NonceStr', max_length=20, blank=True,null=True)  # Field name made lowercase.
    signature = models.CharField(db_column='Signature', max_length=64, blank=True, null=True)  # Field name made lowercase.
    appid = models.CharField(db_column='AppId', max_length=64, blank=True, null=True)  # Field name made lowercase.
    timeoutsecond = models.IntegerField(db_column='TimeOutSecond', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_wx_ticket'


class HsNewsInfo(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    ncode = models.CharField(db_column='NCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    tindex = models.IntegerField(db_column='TIndex', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=64, blank=True, null=True)  # Field name made lowercase.
    info = models.CharField(db_column='Info', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    imagename = models.CharField(db_column='ImageName', max_length=64, blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_newsinfo'


class HsWXConfig(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    appid = models.CharField(db_column='AppId', unique=True, max_length=200, blank=True,null=True)  # Field name made lowercase.
    appsecret = models.CharField(db_column='AppSecret', unique=True, max_length=200, blank=True,null=True)  # Field name made lowercase.
    apikey = models.CharField(db_column='ApiKey', max_length=200, blank=True, null=True)  # Field name made lowercase.
    mchid = models.CharField(db_column='MchId', max_length=200, blank=True, null=True)  # Field name made lowercase.
    nonestr = models.CharField(db_column='NoneStr', max_length=200, blank=True, null=True)  # Field name made lowercase.
    notifyurl = models.CharField(db_column='NotiryUrl', max_length=200, blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_newsinfo'              


#----------------For Game
class HsGameKBiao(models.Model):  #
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name',  max_length=64, blank=True,null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=1, blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_game_ke_biao'

class HsGameLevel(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=64, blank=True,null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=1, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'hs_game_level'      

class HsGameGrade(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=64, blank=True,null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=1, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'hs_game_grade'   
            
class HsGameUnit(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=64, blank=True,null=True)  # Field name made lowercase.
    kbcode = models.CharField(db_column='KBCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    lcode = models.CharField(db_column='LCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    gcode = models.CharField(db_column='GCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', unique=True, max_length=32, blank=True,
                             null=True)  # Field name made lowercase.
    index = models.IntegerField(db_column='Index', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'hs_game_unit'     
        
class HsGameCustom(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    sevstart = models.CharField(db_column='SevStart', unique=True, max_length=10, blank=True,null=True)  # Field name made lowercase.
    sevstop = models.CharField(db_column='SevStop', unique=True, max_length=10, blank=True,null=True)  # Field name made lowercase.
    invitecode= models.CharField(db_column='InviteCode', unique=True, max_length=10, blank=True,null=True)  #
    class Meta:
        managed = False
        db_table = 'hs_game_custom'

class HsGameSystemWords(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    words = models.CharField(db_column='words', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    meaning = models.CharField(db_column='meaning', unique=True, max_length=128, blank=True,null=True)  # Field name made lowercase.
    lx = models.CharField(db_column='lx', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    pron = models.CharField(db_column='pron', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_game_system_words' 
        
class HsGameUnitWords(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    wcode = models.CharField(db_column='WCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_game_unit_words'
        
class HsGameSaleCompany(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=64, blank=True,null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', unique=True, max_length=10, blank=True,null=True)  # Field name made lowercase.
    invitecode= models.CharField(db_column='InviteCode', unique=True, max_length=10, blank=True,null=True)  # ������ʦ�Ĵ���
    class Meta:
        managed = False
        db_table = 'hs_game_sale_company'

class HsGameErrorBook(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    wcode = models.CharField(db_column='WCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    mykey = models.CharField(db_column='MYKey', unique=True, max_length=64, blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_game_error_book'        

class HsGameRoom(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    roomkey = models.CharField(db_column='RoomKey', unique=True, max_length=8, blank=True,null=True)  # Field name made lowercase.
    ccode = models.CharField(db_column='CCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=1, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'hs_game_room'






class HsGameResult(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    ccode = models.CharField(db_column='CCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    ucode = models.CharField(db_column='UCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    score = models.IntegerField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    gametime = models.CharField(db_column='GameTime', max_length=20, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'hs_game_result'

class HsCustomGameSetting(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    ccode = models.CharField(db_column='CCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.

    kbcode = models.CharField(db_column='KBCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    lcode = models.CharField(db_column='LCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    gcode = models.CharField(db_column='GCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=1, blank=True, null=True)  # 上学期  下学期.
    class Meta:
        managed = False
        db_table = 'hs_game_custom_setting'

class HsTempT(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    words = models.CharField(db_column='words', unique=True, max_length=64, blank=True,null=True)  # Field name made lowercase.
    prouces = models.CharField(db_column='prouces', max_length=2000, blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'temp_t'

class HsGameSystemWordsCopy(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    words = models.CharField(db_column='words', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    meaning = models.CharField(db_column='meaning', unique=True, max_length=128, blank=True,null=True)  # Field name made lowercase.
    lx = models.CharField(db_column='lx', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    pron = models.CharField(db_column='pron', max_length=200, blank=True, null=True)  # Field name made lowercase.
    uspron = models.CharField(db_column='uspron', max_length=200, blank=True, null=True)  # Field name made lowercase.
    ukpron = models.CharField(db_column='ukpron', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_game_system_words_copy'

class HsCustomGameShareCount(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    ccode = models.CharField(db_column='CCode', unique=True, max_length=32, blank=True,null=True)  # Field name made lowercase.
    sharecount =  models.IntegerField(db_column='ShareCount', blank=True, null=True)  # Field name made lowercase.
    sharedate = models.CharField(db_column='ShareDate', unique=True, max_length=10, blank=True,
                             null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'hs_game_custom_share'

class HsEnwords(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    words = models.CharField(db_column='words',  max_length=32, blank=True,null=True)  # Field name made lowercase.
    explain = models.CharField(db_column='explain', max_length=1000, blank=True,
                             null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'EnWords'


class HsEvyDayWord(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    evdate = models.CharField(db_column='EVDate', max_length=10, blank=True,
                             null=True)  # Field name made lowercase.
    word = models.CharField(db_column='Word',  max_length=32, blank=True,null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True,
                             null=True)  # Field name made lowercase.
    sound = models.CharField(db_column='Sound',  max_length=32, blank=True,null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'hs_evyday_word'

class HsEvySentence(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    evdate = models.CharField(db_column='EVDate', max_length=10, blank=True,
                             null=True)  # Field name made lowercase.
    encontent = models.TextField(db_column='EnContent',   blank=True,null=True)  # Field name made lowercase.
    cncontent = models.TextField(db_column='CnContent', blank=True,
                             null=True)  # Field name made lowercase.
    sound = models.CharField(db_column='Sound',  max_length=32, blank=True,null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'hs_evyday_sentence'

class HsEvyRead(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    evdate = models.CharField(db_column='EVDate', max_length=10, blank=True,
                             null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=64, blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content',  blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_evyday_read'

# =================school
class HsSchoolCustom(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    wxaccount = models.CharField(db_column='WxAccount', max_length=64, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    headimage = models.CharField(db_column='HeadImage', max_length=2000, blank=True,null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    alias = models.CharField(db_column='Alias', max_length=32, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=32, blank=True, null=True)  # Field name made lowercase.
    school = models.CharField(db_column='School', max_length=64, blank=True, null=True)  # Field name made lowercase.
    regdate = models.DateField(db_column='RegDate')  # Field name made lowercase.
    email = models.CharField(db_column='EMail', max_length=64, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'hs_school_custom'

class HsSchoolMessage(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32, blank=True, null=True)  # Field name made lowercase.
    wxaccount = models.CharField(db_column='WxAccount', max_length=64, blank=True, null=True)  # Field name made lowercase.
    msgcontent = models.CharField(db_column='MsgContent', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    msgtime = models.DateTimeField(db_column='MsgTime')  # Field name made lowercase.
    flag = models.IntegerField(db_column='Flag', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_school_message'

class HsSchoolApply(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32, blank=True, null=True)  # Field name made lowercase.
    wxaccount = models.CharField(db_column='WxAccount', max_length=64, blank=True, null=True)  # Field name made lowercase.
    attachfilename = models.CharField(db_column='AttachFileName', max_length=64, blank=True, null=True)  # Field name made lowercase.
    applydate = models.DateField(db_column='ApplyDate')  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_school_apply'
class HsSchoolArticle(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=32, blank=True, null=True)  # Field name made lowercase.
    wxaccount = models.CharField(db_column='WxAccount', max_length=64, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=64, blank=True, null=True)  # Field name made lowercase.
    htmlcontent = models.CharField(db_column='HtmlContent', max_length=4000, blank=True, null=True)  # Field name made lowercase.
    applydate = models.DateField(db_column='ApplyDate')  # Field name made lowercase.
    state = models.IntegerField(db_column='State', blank=True, null=True)  # Field name made lowercase.
    viewcount = models.IntegerField(db_column='ViewCount', blank=True, null=True)  # Field name made lowercase.
    simplecontent = models.CharField(db_column='SimpleContent', max_length=200, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'hs_school_article'

class HsSchoolFav(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    articlecode = models.CharField(db_column='ArticleCode', max_length=32, blank=True, null=True)  # Field name made lowercase.
    wxaccount = models.CharField(db_column='WxAccount', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hs_school_fav'