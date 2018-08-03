#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import *
from email.header import Header
# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
import mimetypes ,os.path

import smtplib
import email.MIMEMultipart# import MIMEMultipart
import email.MIMEText# import MIMEText
import email.MIMEBase# import MIMEBase
import os.path
import mimetypes
import socket

SEND_ADDRESS = "gj00001@qq.com"
MAIL_PASSWORD="caojj_123"
SMTP_SERVER="smtp.qq.com"
SMTP_PORT = 587

class BaseEmail(object):
    def __init__(self):
        pass

    @staticmethod
    def sendMail(bodyDatas,title):
        to_addr = "609853524@qq.com"
        socket.setdefaulttimeout(20)
        subject = '竞标提示：人脸识别'
        # msg = MIMEText('你好', 'text', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
        # msg['Subject'] = Header(subject, 'utf-8')

        msg = MIMEMultipart()
        msg['From'] = SEND_ADDRESS
        msg['To'] = to_addr
        # msg['Cc'] = ccaddr
        msg['Subject'] = "来自汉森微店留言提醒===>>" + title

        body = "提示：请关注以下留言信息"
        # for one in bodyDatas:
        body = "%s \n    %s"%(body, bodyDatas)

        # body = body.encode("utf-8")
        msg.attach(MIMEText(body, 'plain'))

        smtp = smtplib.SMTP()
        smtp.connect(SMTP_SERVER)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.set_debuglevel(0)

        try:
            smtp.login(SEND_ADDRESS, MAIL_PASSWORD)
            smtp.sendmail(SEND_ADDRESS, to_addr, msg.as_string())
            smtp.quit()
        except Exception,ex:
            print ex
            HsWriteLog('send mail failed！=====================================' + ex.message)
            pass

        # @staticmethod
    # def _format_addr(s):
    #     name, addr = parseaddr(s)
    #     return formataddr(( \
    #         Header(name, 'utf-8').encode(), \
    #         addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    @staticmethod
    def sendMailHasAttach(bodyDatas,title,file_name):
        to_addr = "609853524@qq.com"

        subject = '测试邮件：XXXX'
        # msg = MIMEText('你好', 'text', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
        # msg['Subject'] = Header(subject, 'utf-8')

        msg = MIMEMultipart()
        msg['From'] = SEND_ADDRESS
        msg['To'] = to_addr
        # msg['Cc'] = ccaddr
        msg['Subject'] = "测试邮件===>>" + title

        body = "邮件主题信息："
        body = "%s \n    %s"%(body, bodyDatas)

        #body = body.encode("utf-8")
        msg.attach(MIMEText(body, 'plain'))



        ## 读入文件内容并格式化 [方式1]－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
        data = open(file_name, 'rb')
        ctype, encoding = mimetypes.guess_type(file_name)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
        file_msg.set_payload(data.read())
        data.close()
        email.Encoders.encode_base64(file_msg)  # 把附件编码
        ''''' 
         测试识别文件类型：mimetypes.guess_type(file_name) 
         rar 文件             ctype,encoding值：None None（ini文件、csv文件、apk文件） 
         txt text/plain None 
         py  text/x-python None 
         gif image/gif None 
         png image/x-png None 
         jpg image/pjpeg None 
         pdf application/pdf None 
         doc application/msword None 
         zip application/x-zip-compressed None 

        encoding值在什么情况下不是None呢？以后有结果补充。 
        '''
        # －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－

        ## 设置附件头
        basename = os.path.basename(file_name)
        file_msg.add_header('Content-Disposition', 'attachment', filename=basename)  # 修改邮件头
        msg.attach(file_msg)


        smtp = smtplib.SMTP()
        smtp.connect(SMTP_SERVER)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.set_debuglevel(0)
        smtp.login(SEND_ADDRESS, MAIL_PASSWORD)
        smtp.sendmail(SEND_ADDRESS, to_addr, msg.as_string())
        smtp.quit()

if __name__ == "__main__":
    BaseEmail.sendMail("这款电视真的很大，而且很薄，自带的接口也很齐全，底座也很结实，观影效果清晰，确实是我想要的东西，我想如果是再买大一点的话，我的电视柜就要搁不下了。一般可以看各种视频，嗯她，连接无线网也可以连接网线，也可以，刚来的时候时候以为没有网线都不能用，结果并不是，它可以连接wifi，这点很给力说明书很简单，基本上都不用看我的电视并没有挂起来，只是放在底座上了，我怕我的墙承受不住。送货人员帮我送上楼来，一直安装好调试好，这点给个赞再说一下配置，CPU反应确实很快！打开应用，基本都是秒开，个人认为只是个电视而已，不想让他下载更多的东西，所以说内存方面的话，个人感觉够用，最关键的一点，他可以投屏，把手机上显示的东西投到屏幕上，昨天晚上试了一下游戏，你能想到有多爽？真的太棒了！刚开始可能调不明白，但是你一定要耐心的调，其实很简单！","测试标题！")
    #BaseEmail.sendMailHasAttach("这款电视真的很大，而且很薄，自带的接口也很齐全，底座也很结实，观影效果清晰，确实是我想要的东西，我想如果是再买大一点的话，我的电视柜就要搁不下了。一般可以看各种视频，嗯她，连接无线网也可以连接网线，也可以，刚来的时候时候以为没有网线都不能用，结果并不是，它可以连接wifi，这点很给力说明书很简单，基本上都不用看我的电视并没有挂起来，只是放在底座上了，我怕我的墙承受不住。送货人员帮我送上楼来，一直安装好调试好，这点给个赞再说一下配置，CPU反应确实很快！打开应用，基本都是秒开，个人认为只是个电视而已，不想让他下载更多的东西，所以说内存方面的话，个人感觉够用，最关键的一点，他可以投屏，把手机上显示的东西投到屏幕上，昨天晚上试了一下游戏，你能想到有多爽？真的太棒了！刚开始可能调不明白，但是你一定要耐心的调，其实很简单！","测试标题！","D:\\timg.jpg")