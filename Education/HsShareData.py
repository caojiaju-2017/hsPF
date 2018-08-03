#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading,datetime,md5,os
from HsEduServer.settings import *
from HsEdu.models import *

import logging
logger = logging.getLogger('django')
class HsShareData:
    dataLock = threading.Lock()
    Version = 'Act_V1.0'
    KeyCode = {}


    SigCode = 'af?Fzio2u'

    IsDebug = True
    GuestAccessDict = {}
    GuestMaxAccessCount = 50

    Factorys = []
    Votes = []
    VoteRecords = []
    Config = None

    lockFactorys = threading.Lock()
    lockVoteRecords = threading.Lock()
    lockVotes = threading.Lock()

    RENT_FEE = 2
    MAX_SHARE_COUNT = 10
    SmsListData = []


class CommitData(object):
    def __init__(self,dbhandle,type):
        self.dbHandle = dbhandle
        self.operatorType = type  # save  delete
