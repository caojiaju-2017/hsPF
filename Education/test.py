#!/usr/bin/env python
# -*- coding: utf-8 -*-

# E:\GitWorkSpace\NewEducation\微信数据\每日一句

import datetime,os

now = datetime.datetime.now()
delta = datetime.timedelta(days=1)
n_days = now + delta
n_days.strftime('%Y-%m-%d')

for index in range(365):
    if index == 0:
        continue
    delta = datetime.timedelta(days=index)
    n_days = now + delta
    willDate = n_days.strftime('%Y-%m-%d')
    path = u"E:\\GitWorkSpace\\NewEducation\\微信数据\\每日一文\\%s"%willDate

    try:
        os.makedirs(path)
    except:
        pass