#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *

appID = "wx6d45e5e461e41f06"
appsecret = "726c202ca673beff13e4bc7dd0d5d01a"

class WxApiHelp(object):
    @staticmethod
    @csrf_exempt
    def CommandDispatch(req):
        # print "api invoke1"
        command = req.GET.get('Command').upper()
        # print "api invoke2"
        # return HttpResponse("ok")
        if  command  == "Bind_Phone".upper():
            return WxApiHelp.Bind_Phone(req)
        elif command  == "Get_Addresses".upper():
            return WxApiHelp.Get_Addresses(req)

    @staticmethod
    @csrf_exempt
    def getWxAuthData(request):
        # 请求微信加密验证码---用于配置后天数据
        return HttpResponse("iJqJ8ZXNRFKMeimo")

    @staticmethod
    @csrf_exempt
    def wxA(request):
        '''
        微信登录
        :param request:
        :return:
        '''
        dict = {}
        try:
            code = request.GET.get('code')
            state = request.GET.get('state')
        except Exception, e:
            # print u"获取code和stat参数错误"
            return render(request, 'wxauth.html', dict)


        dict["code"]=code
        dict["state"] = state

        # 获取token
        try:
            url = u'https://api.weixin.qq.com/sns/oauth2/access_token'
            params = {
                'appid': appID,
                'secret': appsecret,
                'code': code,
                'grant_type': 'authorization_code'
            }
            res = requests.get(url, params=params).json()

            access_token = res["access_token"]  # 只是呈现给大家看,可以删除这行
            openid = res["openid"]  # 只是呈现给大家看,可以删除这行

            dict["access_token"] = access_token
            dict["openid"] = openid
        except Exception, e:
            # print u"获取access_token参数错误"
            return render(request, 'wxauth.html', dict)

        a = 1
        # 4.拉取用户信息
        #  //http：GET（请使用https协议） https://api.weixin.qq.com/sns/userinfo?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
        try:
            user_info_url = u'https://api.weixin.qq.com/sns/userinfo'
            params = {
                'access_token': access_token,
                'openid': openid,
            }
            res = requests.get(user_info_url, params=params).json()
            print res
            nameUser = res['nickname'].encode('iso8859-1').decode('utf-8')

            print nameUser
            """
            注意,这里有个坑,res['nickname']表面上是unicode编码,
            但是里面的串却是str的编码,举个例子,res['nickname']的返回值可能是这种形式
            u'\xe9\x97\xab\xe5\xb0\x8f\xe8\x83\x96',直接存到数据库会是乱码.必须要转成
            unicode的编码,需要使用
            res['nickname'] = res['nickname'].encode('iso8859-1').decode('utf-8')
            这种形式来转换.
            你也可以写个循环来转化.
            for value in res.values():
                value = value.encode('iso8859-1').decode('utf-8')
            """

            # 检查账户信息
            existAccount = HsParents.objects.filter(wxaccount=openid).first()
            if not existAccount:
                newAccount = HsParents()
                newAccount.wxaccount = openid
                newAccount.name = nameUser
                newAccount.wxheadimage = res['headimgurl']
                # newAccount.lastlogintime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                try:
                    newAccount.save()
                except Exception,ex:
                    print 'create account error' + ex.message

            dict["openid"] = openid
            dict["wx_name"] = nameUser
            dict["wx_head_image"] = res['headimgurl']

        except Exception, e:
            # print u"拉取用户信息错误"
            return render(request, 'wxauth.html', dict)

        #
        # return  HttpResponse("MSBMLCCIiHOH519f")

        # 登录成功，直接渲染主页
        return render(request, './?OpenId=%s&WxName=%s&HeadImg=%s'% (openid,nameUser, res['headimgurl']),dict)