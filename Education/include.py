#!/usr/local/bin/python
#-*- coding:utf-8 -*-

import httplib
import urllib
import datetime
import threading
import md5
import random
import os
import inspect
import hashlib
import base64
import pickle
import socket
import sys
import platform
import time
import json
import uuid
import re
import et
import qrcode
import urllib2
import requests
from django.template import Template, Context
from HsPlatform.Sms.HsSmsHelp import *
from HsPlatform.Sms.MobileRecord import *

# DJANGO 引用
from django.shortcuts import render,render_to_response
from django.http import  HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.template import Template, Context
from HsEdu.models import *
from HsEdu.Api.PublicService import *
from HsShareData import *

import logging
import json,uuid,time,base64,re,urllib
from django.shortcuts import render,render_to_response
from django.http import  HttpResponse,HttpResponseRedirect

from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import qrcode,urllib2,requests
from HsShareData import *
from django.db.models import F
from django.db.models import Q
from HsEdu.models import *
import xml.etree.ElementTree as ET

from HsEdu.Api.BaseEmail import *

logger = logging.getLogger('django')
appID = "wx75e53a9db8f89fce"
appsecret = "c45eefc37a8a0889fa4ebe020a9eb696"
api_key="e23458c671bd7d2b5dd9919f7a700a61"

def HsWriteLog(message):
    # return
    global logger
    logger.error(message)
