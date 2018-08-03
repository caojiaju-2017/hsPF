#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import urlretrieve
import chardet
url = "http://online2.tingclass.net/lesson/shi0529/0009/9857/%d.mp3"

# for index in range(582):
#     try:
#         urlretrieve(url % index, 'E:\GitWorkSpace\NewEducation\word\%d.mp3'%index)
#     except:
#         pass

s = '我'.decode('utf-8')
print chardet.detect(s)