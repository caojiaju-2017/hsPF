#!/usr/bin/env python
# -*- coding: utf-8 -*-
# e065b8c671bd7d2b5dd9913f7a700380
from include import *
#http://blog.csdn.net/vanqingyu/article/details/52156289
appID = "wx75e53a9db8f89fce"
appsecret = "c45eefc37a8a0889fa4ebe020a9eb696"
api_key="e23458c671bd7d2b5dd9919f7a700a61"
access_token = None
ticket = None
mch_id = "1495716512"
nonce_str = "fsdfds"
notify_url="http://www.h-sen.com/paySuccess.html"
class WebCenterApi(object):
    @staticmethod
    @csrf_exempt
    def CommandDispatch(req):
        command = req.GET.get('Command').upper()

    @staticmethod
    @csrf_exempt
    def getWxAuthData(request):
        return HttpResponse("MSBMLCCIiHOH519f")

    @staticmethod
    @csrf_exempt
    def wxA(request):
        #HsWriteLog('Something went wrong!')
        dict = {}
        try:
            code = request.GET.get('code')
            state = request.GET.get('state')
        except Exception, e:
            # print u"获取code和stat参数错误"
            return render(request, 'index.html', dict)


        dict["code"]=code
        dict["state"] = state

        # 获取token
        # https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code
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
            return render(request, 'index.html', dict)

        a = 1
        wxInfo = {}
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
            openid = openid.encode('utf-8')
            nameUser = nameUser.encode('utf-8')
            imgUrl = res['headimgurl'].encode('utf-8')

            wxInfo["OpenId"] = openid
            wxInfo["WxName"] = nameUser
            wxInfo["HeadImg"] = imgUrl

            # 添加到客户表
            existCustomHandle = HsCustom.objects.filter(wxaccount=openid).first()
            if not existCustomHandle:
                newCustom = HsCustom()
                newCustom.wxaccount = openid
                newCustom.name = nameUser
                newCustom.headimage = imgUrl
            else:
                newCustom = existCustomHandle
                newCustom.name = nameUser
                newCustom.headimage = imgUrl

            newCustom.save()
        except Exception, e:
            HsWriteLog('Something went wrong!====================================='+e.message)
            return render(request, 'index.html', dict)

        # 返回一些数据
        resArray = []
        resDatas = HsResources.objects.all().order_by('-code')[:10]
        for oneRes in resDatas:
            resDict = {}
            resDict['ResGrade']=getName(0,oneRes.resgrade)
            resDict['ResLevel'] = getName(1,oneRes.reslevel)
            resDict['ResClass'] = getName(2,oneRes.resclass)
            resDict['ResInfo'] = oneRes.resinfo[:50]
            resDict['ResImage'] = oneRes.resimage
            resDict['Price'] = oneRes.price
            resDict['Name'] = oneRes.name
            resDict['ViewCount'] = oneRes.viewcount
            resDict['BuyCount'] = 14
            resDict['ResTitle'] = oneRes.restitle
            resDict['OrgName'] = oneRes.orgname
            resDict['Code'] = oneRes.code
            resDict['ResImage'] = oneRes.resimage
            resArray.append(resDict)
        # dict['Resource_Datas']= renterDictAarry

        # 查询数据
        homeDictAarry = []
        hsNews = HsNews.objects.filter().order_by('-newstime')[:10]
        for one in hsNews:
            oneNews={}
            oneNews['Title'] = one.title
            oneNews["Info"] = one.info[0:60]
            oneNews['Date'] = one.newstime
            oneNews['Image'] = one.image
            oneNews['Code'] = one.code

            homeDictAarry.append(oneNews)
        dict['NewsDatas'] = homeDictAarry
        dict['wxInfo'] = json.dumps(wxInfo)
        dict['Resource_Datas']=resArray
        # return  HttpResponse("MSBMLCCIiHOH519f")
        return render(request, 'index.html',dict)

    @staticmethod
    def calcSepSeconds(start,stop):
        return  (stop - start).seconds

    @staticmethod
    def getShareData(cmd,cmdcode):
        rtnDict={}
        if cmd == "View_News": # newsInfo
            queryNews = HsNews.objects.all().filter(code=cmdcode).first()
            if queryNews:
                rtnDict["title"] = queryNews.title
                rtnDict["context"] = queryNews.info
                rtnDict["image"] = "newsPic/" + queryNews.image
            else:
                rtnDict["title"] = "新闻分享"
                rtnDict["context"] = "来自于汉森教育的新闻分享，关注官方微信公众号，可免费领取教学视频资源。"
                rtnDict["image"] = "default.jpg"
        elif cmd == "Open_Resource":
            queryResource = HsResources.objects.all().filter(code=cmdcode).first()
            if queryResource:
                rtnDict["title"] = queryResource.restitle
                rtnDict["context"] = queryResource.resinfo
                rtnDict["image"] = "ResImage/" + queryResource.resimage
            else:
                rtnDict["title"] = "资源分享"
                rtnDict["context"] = "来自于汉森教育的资源分享，关注官方微信公众号，可免费领取教学视频资源。"
                rtnDict["image"] = "default.jpg"
        elif cmd == "GAME_WORDS":
            rtnDict["title"] = "中小学单词游戏"
            rtnDict["context"] = "课程功能紧密结合,学生背单词之后，有些单词在测试的时候答错了，系统为你记录，后续可复习，在玩游戏的过程中不知不觉地记住单词。"
            rtnDict["image"] = "game/" + "game.png"
            # url = "http://www.h-sen.com/wait_game.html"
        else:
            rtnDict["title"] = "汉森资源分享"
            rtnDict["context"] = "来自于汉森教育的新闻分享，关注官方微信公众号，可免费领取教学视频资源。"
            rtnDict["image"] = "default.jpg"

        return  rtnDict
    @staticmethod
    @csrf_exempt
    def shareToFriend(request):
        url = request.GET.get('url')

        cmd = None
        cmdCode = None
        try:
            values = url.split('?')[-1]
            for key_value in values.split('&'):
                oneKey = key_value.split('=')
                key = oneKey[0]
                value = oneKey[1]
                if key.lower() == "command":
                    cmd = value
                elif key.lower() == "code":
                    cmdCode = value
        except:
            cmd = "None"
            cmdCode="null"

        if "game_" in url:
            cmd = "GAME_WORDS"

        # HsWriteLog("Command cmd = " + cmd)
        # HsWriteLog("Command cmdCode = " + cmdCode)
        # url = "http://www.h-sen.com/?code=021qjgjm00rgWl18bojm0iyzjm0qjgj7&state=abc"
        rtnDict = {}
        # 检查上一次授权
        timesnamp = int(time.time())
        lastedData = HsWxTicket.objects.filter().first()
        nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        HsWriteLog(nowtime)
        shareDataDict = WebCenterApi.getShareData(cmd,cmdCode)
        # shareDataDict, url = WebCenterApi.getShareData(cmd, cmdCode, url)
        if lastedData:
            HsWriteLog('Not First Ticket=====================================')
            stop = datetime.datetime.now()
            start = datetime.datetime.strptime(lastedData.signtime, '%Y-%m-%d %H:%M:%S')
            HsWriteLog(lastedData.signtime)
            sepSeconds = WebCenterApi.calcSepSeconds(start, stop) #https://www.cnblogs.com/liuq/p/6211005.html
            timeouttimes = 0
            if not lastedData.timeoutsecond:
                timeouttimes = 0
            else:
                timeouttimes = int(lastedData.timeoutsecond)
            HsWriteLog('Time Sep= %d====================================='%(sepSeconds))
            HsWriteLog('Time TimeOut = %d====================================='%(timeouttimes))
            if sepSeconds < timeouttimes:
                HsWriteLog('Not Timeout=====================================')
                rtnDict['timeStamp'] = timesnamp
                rtnDict['nonceStr'] = str(lastedData.noncestr)
                rtnDict['signature'] = WebCenterApi.getOldSignature(url,str(timesnamp),str(lastedData.noncestr),str(lastedData.ticket))
                rtnDict['appId'] = str(lastedData.appid)

                rtnDict['title'] = shareDataDict["title"]
                rtnDict['context'] = shareDataDict["context"]
                rtnDict['image'] = shareDataDict["image"]
                HsWriteLog('share url:' + url)
                rtnDict['url'] = url

                # HsWriteLog("LastData ====>"+str(rtnDict))
                rtnDictGlobal = rtnDict
                loginResut = json.dumps(rtnDictGlobal)
                return HttpResponse(loginResut)
            else:
                HsWriteLog('TimeOut=====================================')
        else:
            HsWriteLog('First get Ticket=====================================')
            lastedData = HsWxTicket()


        print "shareToFriend===>",url

        nonceStr = 'Zfdf09i'
        # nowtime = datetime.datetime.strptime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")



        rtnDict['timeStamp'] = timesnamp
        rtnDict['nonceStr'] = nonceStr

        signResult = WebCenterApi.getSignature(appID, appsecret, url, timesnamp, nonceStr)
        rtnDict['signature'] = signResult[0]
        rtnDict['appId'] = appID

        rtnDict['title'] = shareDataDict["title"]
        rtnDict['context'] = shareDataDict["context"]
        rtnDict['image'] = shareDataDict["image"]

        rtnDict['url'] = url
        rtnDictGlobal = rtnDict

        # 更新数据库
        HsWriteLog('start save=====================================')
        lastedData.ticket =  signResult[2]
        lastedData.signtime = nowtime
        lastedData.timestamp = timesnamp
        lastedData.noncestr = nonceStr
        lastedData.signature =  rtnDict['signature']
        lastedData.appid = appID
        lastedData.timeoutsecond = signResult[1]

        try:
            lastedData.save()
        except:
            HsWriteLog('start save failed=====================================')
            pass

        HsWriteLog("NewData ====>"+ str(rtnDictGlobal))
        loginResut = json.dumps(rtnDictGlobal)
        return HttpResponse(loginResut)
    @staticmethod
    def getSignature(appid,appscret,url,timesnamp,noncestr):
        accessToken = WebCenterApi.getAccessToken(appid, appscret)
        jsapi_ticket,timeoutseconds = WebCenterApi.getJsapiTicket(accessToken)
        signValue = "jsapi_ticket=" + jsapi_ticket + "&noncestr=" + noncestr + "&timestamp=" + str(timesnamp) + "&url=" + url
        HsWriteLog("jsapi_ticket:" + jsapi_ticket)
        import hashlib
        signature = hashlib.sha1(signValue).hexdigest()
        return signature,timeoutseconds,jsapi_ticket

    @staticmethod
    def getOldSignature(url,timesnamp,noncestr,jsapi_ticket):
        signValue = "jsapi_ticket=" + jsapi_ticket + "&noncestr=" + noncestr + "&timestamp=" + str(timesnamp) + "&url=" + url

        HsWriteLog("Resing String:" + signValue)
        import hashlib
        signature = hashlib.sha1(signValue).hexdigest()
        return signature
    @staticmethod
    def getAccessToken(appid,appsecret):
        global access_token
        # WEIXIN_JSAPI_TICKET_URL = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=ACCESS_TOKEN&type=jsapi";
        # access_token = mapToken.get("accessToken")
        if access_token == None:
            url = "https://api.weixin.qq.com" + "/cgi-bin/token?grant_type=client_credential&appid="+appid+"&secret="+appsecret;

            # menuJsonStr = HttpUtil.get(url);
            # 定义字典
            try:
                req = urllib2.Request(url)
                res = urllib2.urlopen(req)
                res = res.read()

                print '===getAccessToken===>',res
                resDict = json.loads(res)
                access_token = resDict['access_token']
            except :
                access_token = None

        return access_token
    @staticmethod
    def getJsapiTicket(accessToken):
        global ticket
        expires_in = None
        if ticket == None:
            print "===>",access_token
            url = None
            try:
                url = "https://api.weixin.qq.com" + "/cgi-bin/ticket/getticket?access_token="+accessToken+"&type=jsapi"
            except:
                return None
            # menuJsonStr = HttpUtil.get(url);
            # type = new TypeToken < Map < String, Object >> () {}.getType();
            #  Map < Object, Object > ticketInfo = new Gson().fromJson(menuJsonStr, type);
            try:
                req = urllib2.Request(url)
                res = urllib2.urlopen(req)
                res = res.read()

                print '===getJsapiTicket===>', res

                resJson = json.loads(res)
                ticket = resJson['ticket']
                expires_in = resJson['expires_in']
            except:
                ticket = None

        print 'tickes====',ticket
        return ticket,expires_in

    @staticmethod
    @csrf_exempt
    def upload_res_file(request):
        HsWriteLog('upload_res_file')
        if request.method == "POST":  # 请求方法为POST时，进行处理
            myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
            if not myFile:
                return HttpResponse("no files for upload!")

            destination  = os.path.join(STATIC_ROOT,"Images")
            destination  = os.path.join(destination,"ResImage")
            destination = open(os.path.join(destination, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

            return HttpResponse(myFile.name)

    @staticmethod
    @csrf_exempt
    def upload_news_file(request):
        HsWriteLog('upload_res_file')
        if request.method == "POST":  # 请求方法为POST时，进行处理
            myFile = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
            if not myFile:
                return HttpResponse("no files for upload!")

            destination  = os.path.join(STATIC_ROOT,"Images")
            destination  = os.path.join(destination,"newsPic")
            destination = open(os.path.join(destination, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

            return HttpResponse(myFile.name) 


    @staticmethod
    @csrf_exempt
    def UploadRes(request):
        renterDict={}
        return render(request, 'uploadres.html',renterDict )         

    @staticmethod
    @csrf_exempt
    def UploadNews(request):
        renterDict={}
        return render(request, 'uploadnews.html',renterDict )       
        
    @staticmethod
    def getOrderNo():
        return "%s%04d"%(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())), random.randint(1, 9999))
    @staticmethod
    def payCall(request):
        HsWriteLog('wx pay invoke')
        # 用户Code
        openid = request.GET.get('openid')
        code = request.GET.get('code')
        rescode = request.GET.get('rescode')

        HsWriteLog("rescode =%s" % rescode)
        HsWriteLog("code =%s" % code)

        fee = 0
        rejectDirectUrl = 'wxpaying.html'
        payDict = {}
        if rescode == "GAME_PAY":
            shareHandle = HsCustomGameShareCount.objects.filter(ccode=openid).first()

            shareCount = 0
            if not shareHandle:

                shareCount = 0
            else:
                shareCount = shareHandle.sharecount
            HsWriteLog("openid =%s" % openid)
            HsWriteLog("shareCount =%d" % shareCount)

            if shareCount >= 10:
                shareCount = 10

            fee = HsShareData.RENT_FEE*100 - shareCount*100;
            rejectDirectUrl = "game/game_wxpaying.html"
            payDict['OrderPrice'] = HsShareData.RENT_FEE - shareCount
            if shareCount == 0:
                payDict['ResTitle'] = "月租"
            else:
                payDict['ResTitle'] = "月租-分享朋友圈为您节省%d元"%shareCount
        else:
            # 查询资源数据
            resHandle = HsResources.objects.filter(code=rescode).first()

            if not resHandle:
                return render(request, '404.html', {})
            fee = resHandle.price * 100
            payDict['OrderPrice'] = resHandle.price
            payDict['ResTitle'] = resHandle.restitle

        # 获取用户OPENID
        fetchUrl= "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%(appID,appsecret,code)
        fp = urllib2.urlopen(fetchUrl)
        token = fp.read().decode('utf-8')
        tokenjson = json.loads(token)
        openid = tokenjson['openid']
        ip = request.META['REMOTE_ADDR']

        HsWriteLog("payCall function get id=%s" %openid)

        out_trade_no = WebCenterApi.getOrderNo()


        # 签名
        bodyString = "HS Source"
        # 首先获取签名paysign,通过下面代码：
        stringA = "appid=%s&body=%s&mch_id=%s&nonce_str=%s&" \
                  "notify_url=%s&openid=%s&out_trade_no=%s&" \
                  "spbill_create_ip=%s&total_fee=%d&trade_type=JSAPI"%(appID,bodyString,mch_id,nonce_str,notify_url,openid,out_trade_no,ip,fee)
        stringSignTemp = stringA + "&key=%s"%api_key
        paysign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest().upper()

        # HsWriteLog("paysign String =%s" % stringSignTemp)

        # # 获取paysign后，获取prepay_id
        pay_xml ="<xml>\
   <appid>%s</appid>\
   <body>%s</body>\
   <mch_id>%s</mch_id>\
   <nonce_str>%s</nonce_str>\
   <notify_url>%s</notify_url>\
   <openid>%s</openid>\
   <out_trade_no>%s</out_trade_no>\
   <spbill_create_ip>%s</spbill_create_ip>\
   <total_fee>%d</total_fee>\
   <trade_type>JSAPI</trade_type>\
   <sign>%s</sign>\
</xml>"%(appID,bodyString,mch_id,nonce_str,notify_url,openid,out_trade_no,ip,fee,paysign)
        # HsWriteLog("pay_xml String =%s" % pay_xml)

        # 然后传给统一支付API，返回一个xml：
        req = urllib2.Request("https://api.mch.weixin.qq.com/pay/unifiedorder")
        req.add_header('User-Agent',
                       'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
        unifiedorderXML = urllib2.urlopen(req, data=pay_xml.encode('utf-8'))

        # 获取prepay_id,并设置好前端要用的package参数:
        tree = ET.parse(unifiedorderXML)
        root = tree.getroot()
        psign = root.find('sign').text
        prepay_id = root.find("prepay_id").text
        package = "prepay_id=" + prepay_id
        return_code = root.find("return_code").text

        # HsWriteLog("payCall function get return_code=%s" % return_code)
        # HsWriteLog("payCall function get psign=%s" % psign)
        HsWriteLog("payCall function get prepay_id=%s" % prepay_id)
        # HsWriteLog("payCall function get package=%s" % package)

        # 再次签名，准备调用支付
        timesnamp = int(time.time())
        stringB="appId=%s&nonceStr=%s&package=%s&signType=MD5&timeStamp=%s"%(appID,nonce_str,package,timesnamp)
        stringBSignTemp=stringB+"&key=%s"%  api_key
        paysign=hashlib.md5(stringBSignTemp.encode('utf-8')).hexdigest().upper()


        payDict["appid"] = appID
        payDict["timestamp"] = timesnamp
        payDict["nonceStr"] = nonce_str
        payDict["package"] = package
        payDict["paysign"] = paysign
        payDict["rescode"] = rescode

        payDict['OrderNo'] = out_trade_no
        payDict['ResCode'] = rescode

        # 生成订单
        newOrder = HsOrders()
        newOrder.code = out_trade_no
        newOrder.usercode = openid
        newOrder.ordertime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        newOrder.goodscode = rescode
        newOrder.price = fee
        newOrder.state = 0
        newOrder.count = 1
        newOrder.downloadinfo = None

        try:
            newOrder.save()
        except:
            return render(request, '404.html', {})

        return render(request, rejectDirectUrl ,payDict) #HttpResponse(paysign)

    @staticmethod
    @csrf_exempt
    def payWait(request):
        renterDict = {}


    @staticmethod
    @csrf_exempt
    def paySuccess(request):
        HsWriteLog('wx paySuccess invoke1111')
        print request.GET
        return HttpResponseRedirect('wxpaysuccess.html')

    @staticmethod
    @csrf_exempt
    def goHome(request):
        if (not HsShareData.IsDebug)  and not checkMobile(request):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT,"Images"),"erweima_img.png"))
            return render(request, 'warning_notice.html',{"erweima_img":"/static/Images/erweima_img.png"})

        # 提取访问参数
        HsWriteLog('goHome!=====================================')
        try:
            OpenId = request.GET.get('OpenId')
            WxName = request.GET.get('WxName')
            HeadImg = request.GET.get('HeadImg')
        except Exception, e:
            # print u"获取code和stat参数错误"
            # return render(request, 'wxauth.html', dict)
            pass

        renterDict = {}

        renterDictAarry = []
        for index in range (10):
            renterDictAarry.append(index)
        # renterDict['Resource_Datas']= renterDictAarry

        # 查询数据
        homeDictAarry = []
        hsNews = HsNews.objects.filter().order_by('-newstime')[:10]
        for one in hsNews:
            oneNews={}
            oneNews['Title'] = one.title
            oneNews["Info"] = one.info
            oneNews['Date'] = one.newstime
            oneNews['Image'] = one.image
            oneNews['Code'] = one.code

            homeDictAarry.append(oneNews)
        renterDict['NewsDatas'] = homeDictAarry

        return render(request, 'index.html',renterDict )


    @staticmethod
    @csrf_exempt
    def GameSwitch(request):
        HsWriteLog('GameSwitch=========================================!')
        dict = {}
        try:
            code = request.GET.get('code')
            state = request.GET.get('state')
        except Exception, e:
            # print u"获取code和stat参数错误"
            return render(request, 'wait_game.html', dict)


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
            return render(request, 'wait_game.html', dict)

        wxInfo = {}
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
            openid = openid.encode('utf-8')
            nameUser = nameUser.encode('utf-8')
            imgUrl = res['headimgurl'].encode('utf-8')

            wxInfo["OpenId"] = openid
            wxInfo["WxName"] = nameUser
            wxInfo["HeadImg"] = imgUrl

        except Exception, e:
            HsWriteLog('Something went wrong!====================================='+e.message)
            return render(request, 'wait_game.html', dict)

        dict['wxInfo'] = wxInfo
        dict['setting'] = WebCenterApi.loginGame(openid)
        return render(request, 'game/game_home.html',dict)

    @staticmethod
    def getSetting(code):
        HsWriteLog('============>>WebCenterApi.getSetting!')
        # 查询错题记录
        mysetting = HsCustomGameSetting.objects.filter(ccode=code).first()

        if not mysetting:
            loginResut = json.dumps({"ErrorInfo": "未查到配置数据", "ErrorId": 20001, "Result": None})
            return HttpResponse(loginResut)

        rtnDictGlobal = {}
        rtnDictGlobal["kbcode"] = mysetting.kbcode
        rtnDictGlobal["lcode"] = mysetting.lcode
        rtnDictGlobal["gcode"] = mysetting.gcode
        rtnDictGlobal["ccode"] = mysetting.ccode

        return  rtnDictGlobal

    @staticmethod
    def loginGame(code):
        '''
        存储用户的 设置数据
        :param request:
        :return:
        '''
        # code = request.GET.get('code')
        HsWriteLog('============>>WebCenterApi.loginGame!')
        rtnDict = {}
        setting = WebCenterApi.getSetting(code)
        rtnDict["setting"] = setting

        overdate = 0
        currentdate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # 判断账户是否需要重置
        customInfo = HsGameCustom.objects.filter(code=code).first()
        if not customInfo:
            customInfo = HsGameCustom()
            customInfo.code = code
            customInfo.sevstart = currentdate
            now = datetime.datetime.now()
            delta = datetime.timedelta(days=15)
            n_days = now + delta
            customInfo.sevstop = n_days.strftime('%Y-%m-%d')
            try:
                customInfo.save()
            except:
                pass

            pass
        else:
            startdate = customInfo.sevstart
            sevstop = customInfo.sevstop
            if sevstop < currentdate:
                overdate = 1

        rtnDict["overdate"] = overdate

        # 设置月租费用---暂时固定未10元
        rtnDict["renter"] = HsShareData.RENT_FEE
        return rtnDict

    @staticmethod
    @csrf_exempt
    def openWaitPage(request):
        if (not HsShareData.IsDebug)  and not checkMobile(request):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT,"Images"),"erweima_img.png"))
            return render(request, 'warning_notice.html',{"erweima_img":"/static/Images/erweima_img.png"})

        hidden = 0
        try:
            hidden = int(request.GET.get('hidden'))
        except:
            hidden = 0
        renterDict = {}
        renterDict["hidden"] = hidden
        return render(request, 'wait.html',renterDict )

    @staticmethod
    @csrf_exempt
    def openGameWaitPage(request):
        renterDict = {}
        return render(request, 'wait_game.html',renterDict )

    @staticmethod
    @csrf_exempt
    def goHomeEx(request):
        renterDict = {}
        return render(request, 'home_ex.html',renterDict )

    @staticmethod
    @csrf_exempt
    def goFooter(request):
        renterDict = {}
        return render(request, 'footer.html',renterDict )


def getPostData(request):
    postDataList = {}
    if request.method == 'POST':
        for key in request.POST:
            try:
                postDataList[key] = request.POST.getlist(key)[0]
            except:
                pass

    import json
    if not postDataList or len(postDataList) == 0:
        try:
            bodyTxt = request.body
            postDataList = json.loads(bodyTxt)
        except Exception,ex:
            pass

    return  postDataList

def commitCustomDataByTranslate(objHandles):
    with transaction.atomic():
        for oneObject in objHandles:
            if not oneObject.dbHandle:
                continue

            try:
                if oneObject.operatorType == 0:
                    oneObject.dbHandle.save()
                elif oneObject.operatorType == 1:
                    oneObject.dbHandle.delete()
            except Exception,ex:
                return  False

    return True


#判断网站来自mobile还是pc
def checkMobile(request):
    """
    demo :
        @app.route('/m')
        def is_from_mobile():
            if checkMobile(request):
                return 'mobile'
            else:
                return 'pc'
    :param request:
    :return:
    """
    userAgent = request.META.get('HTTP_USER_AGENT', None)
    # userAgent = request.headers['User-Agent']
    # userAgent = env.get('HTTP_USER_AGENT')

    _long_matches = r'googlebot-mobile|android|avantgo|blackberry|blazer|elaine|hiptop|ip(hone|od)|kindle|midp|mmp|mobile|o2|opera mini|palm( os)?|pda|plucker|pocket|psp|smartphone|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce; (iemobile|ppc)|xiino|maemo|fennec'
    _long_matches = re.compile(_long_matches, re.IGNORECASE)
    _short_matches = r'1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|e\-|e\/|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(di|rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|xda(\-|2|g)|yas\-|your|zeto|zte\-'
    _short_matches = re.compile(_short_matches, re.IGNORECASE)

    if _long_matches.search(userAgent) != None:
        return True
    user_agent = userAgent[0:4]
    if _short_matches.search(user_agent) != None:
        return True
    return False
