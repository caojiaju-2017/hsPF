#!/usr/local/bin/python
#-*- coding:utf-8 -*-

from include import *

class SmsData(object):
    def __init__(self):
        self.Storage = "HsSmsHistory"
        self.Account = 'C84396637'
        self.Host = '106.ihuyi.com'
        self.Url = '/webservice/sms.php?method=Submit'
        self.AppSecret = '6c72523f9bb138ac1231e006274db8aa'
        self.TimeOutSeconds = 60
        self.initConfig()

    def initConfig(self):
        # 数据查询

        # 判定结果

        # 初始化对象

        pass


    # 0 表示成功   1001表示未超时
    def sendMessage(self,content,mobile):
        # 检查是否符合时间约定要求
        # 查询记录
        mobileRecord = MobileRecord.getMobileRecord(mobile)

        # 短信超时标识
        toFlag = True

        # 首次发送短信
        if not mobileRecord:
            mobileRecord = MobileRecord()
            mobileRecord.Mobile = mobile
            pass
        else: # 非首次，验证超时时间
            toFlag = mobileRecord.checkTimeOut(self.TimeOutSeconds)

        # 未超时，则返回失败原因
        if not toFlag:
            return 1001

        # 已超时，则重新生成短信验证码
        newSmsCode = self.__newSmsCode()

        # 正常发送
        sendResult = self.__sendSms(content, mobile)

        # 更新手机发送记录数据
        mobileRecord.SmsCode = newSmsCode
        mobileRecord.SendTime = datetime.datetime.now()
        return  0


    # 非公开短信发送函数
    def __sendSms(self,text, mobile):
        params = urllib.urlencode({'account': self.Account, 'password' : self.AppSecret, 'content': text, 'mobile':mobile,'format':'json' })
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection(self.Host, port=80, timeout=30)
        conn.request("POST", self.Url, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()


        return response_str

    def __newSmsCode(self):
        rd = random.randint(1000, 9999)