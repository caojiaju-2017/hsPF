#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *



class MySchoolApi(object):
    @staticmethod
    @csrf_exempt
    def CommandDispatch(request):
        # 检验签名信息
        if checkSign(request):
            loginResut = json.dumps({"ErrorInfo": "Sign Invalid", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)

        # 检查是否登陆
        if not isLogin(request):
            renterDict = {}
            return render(request, 'wait.html', renterDict)

        command = request.GET.get('Command').upper()
        if command == "Release_Article".upper():
            return MySchoolApi.Release_Article(request)
        elif command == "Audit_Article".upper():
            return MySchoolApi.Audit_Article(request)
        elif command == "List_Article".upper():
            return MySchoolApi.List_Article(request)
        elif command == "Delete_Article".upper():
            return MySchoolApi.Delete_Article(request)
        elif command == "Open_Article".upper():
            return MySchoolApi.Open_Article(request)
        elif command == "List_Message".upper():
            return MySchoolApi.List_Message(request)
        elif command == "Release_Message".upper():
            return MySchoolApi.Release_Message(request)
        elif command == "Register_User".upper():
            return MySchoolApi.Register_User(request)
    # ========================== Mobile skd==============================
    @staticmethod
    def openSchoolWaitPage(request):
        renterDict = {}
        return render(request, 'myschool/mb_wait.html',renterDict )

    @staticmethod
    def StartIntroduce(request):
        renterDict = {}
        return render(request, 'myschool/introduce.html',renterDict )

    @staticmethod
    def StartStep1(request):
        renterDict = {}
        return render(request, 'myschool/step1.html',renterDict )

    @staticmethod
    def StartStep2(request):
        renterDict = {}
        username = request.GET.get('username')
        phone = request.GET.get('phone')
        email = request.GET.get('email')
        province = request.GET.get('province')
        city = request.GET.get('city')
        zone = request.GET.get('zone')

        renterDict["username"] = username
        renterDict["phone"] = phone
        renterDict["email"] = email
        renterDict["province"] = province
        renterDict["city"] = city
        renterDict["zone"] = zone

        return render(request, 'myschool/step2.html',renterDict )

    @staticmethod
    def RegDirectLogin(request):
        return render(request, 'myschool/mb_myschool.html', {})

    @staticmethod
    def openHome(request):
        return render(request,'myschool/mb_home.html',{})

    @staticmethod
    def openFind(request):
        return render(request,'myschool/mb_find.html',{})

    @staticmethod
    def openMy(request):
        return render(request,'myschool/mb_my.html',{})

    @staticmethod
    def OpenSchoolHome(request):
        HsWriteLog('OpenSchoolHome=========================================!')
        dict = {}
        try:
            code = request.GET.get('code')
            state = request.GET.get('state')
        except Exception, e:
            # print u"获取code和stat参数错误"
            return render(request, 'myschool/mb_wait.html', dict)


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
            return render(request, 'myschool/mb_wait.html', dict)

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
            return render(request, 'myschool/mb_wait.html', dict)

        dict['wxInfo'] = wxInfo
        HsWriteLog('OpenId=====!' + wxInfo["OpenId"])
        HsWriteLog('WxName=====!' + wxInfo["WxName"])
        HsWriteLog('HeadImg====!' + wxInfo["HeadImg"])
        # dict['setting'] = WebCenterApi.loginGame(openid)

        # 查询账户信息
        customHandle = HsSchoolCustom.objects.filter(wxaccount=wxInfo["OpenId"]).first()

        # 已经注册了账户
        if customHandle:
            HsWriteLog('Have Account')
            return render(request, 'myschool/mb_myschool.html',wxInfo)
        # elif customHandle:
        #     HsWriteLog('New Account====!')
        #
        #     newCustom = HsSchoolCustom()
        #     newCustom.wxaccount = wxInfo["OpenId"]
        #     newCustom.name = wxInfo["WxName"]
        #     newCustom.headimage = wxInfo["HeadImg"]
        #     try:
        #         newCustom.save()
        #     except:
        #         pass

        # 新账户
        return render(request, 'myschool/introduce.html', wxInfo)

    # ================== PC sdk ==========================#
    @staticmethod
    def LoginSchool(request):
        renterDict = {}
        return render(request, 'myschool/login.html',renterDict )

    @staticmethod
    def OpenSchoolPCHome(request):
        renterDict = {}
        return render(request, 'myschool/myschool.html',renterDict )

    #==========================SDK====================================
    @staticmethod
    def Release_Article(request):
        pass
    @staticmethod
    def Audit_Article(request):
        pass
    @staticmethod
    def List_Article(request):
        pageIndex = int(request.GET.get('pageindex'))
        pageSize = int(request.GET.get('pagesize'))
        filterS = request.GET.get('filter')

        ipreques = request.META['REMOTE_ADDR']

        allDatas = HsSchoolArticle.objects.filter(state = 1).order_by("applydate")

        resArray = []
        resDatas = allDatas[pageIndex * pageSize:pageIndex * pageSize + pageSize]

        # 获取vip列表
        customCodes = []
        condition = None
        for oneArticle in resDatas:
            if condition:
                condition = condition + "|Q(wxaccount='%s')"%oneArticle.wxaccount
            else:
                condition = "Q(wxaccount='%s')"%oneArticle.wxaccount

        # 集中查询客户表，获取客户信息
        customHandles = None
        # eval("customHandles=HsSchoolCustom.objects.filter(%s)"%condition)
        customHandles = HsSchoolCustom.objects.filter(Q(wxaccount='oQE6Bt6PVtEL9XzfDSI_Xj0Ed0e8') | Q(wxaccount='oQE6Bt6PVtEL9XzfDSI_Xj0Ed0e8') | Q(wxaccount='oQE6Bt6PVtEL9XzfDSI_Xj0Ed0e8'))
        logger.error("query result ===== > %d g ,%d g"%(len(customHandles), len(resDatas)))

        for oneRes in resDatas:
            resDict = {}
            customInfo = MySchoolApi.getCustom(oneRes.wxaccount,customHandles)

            if customInfo:
                resDict['headimage'] =customInfo.headimage
                resDict['school'] = customInfo.school
            else:
                resDict['headimage'] = "/static/Images/default.png"
                resDict['school'] = ""

            resDict['title'] = oneRes.title
            resDict['time'] = oneRes.applydate.__str__()

            resDict['favvalue'] = 0
            resDict['favimage'] = "/static/Images/3.jpg"
            resDict['simplecontent'] = oneRes.simplecontent
            resDict['articleimage'] =  "/static/myschool/ArticleImage/%s.jpg"%oneRes.code
            resDict['readcount'] = oneRes.viewcount

            results = HsSchoolFav.objects.filter(articlecode=oneRes.code)
            resDict['favcount'] = len(results)


            resArray.append(resDict)
        logger.error("Return result ===== > %d g" % (len(resArray)))
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": resArray})
        return HttpResponse(loginResut)

    @staticmethod
    def getCustom(wxact,dataList):
        if not dataList:
            return  None

        for one in dataList:
            if one.wxaccount == wxact:
                return  one

        return  None
    @staticmethod
    def Delete_Article(request):
        pass
    @staticmethod
    def Open_Article(request):
        pass

    @staticmethod
    def List_Message(request):
        pass

    @staticmethod
    def Release_Message(request):
        pass

    @staticmethod
    def Register_User(request):
        HsWriteLog('Register_User=====================================')
        # openid:openid,wxname:name,imgurl:imagepath,username: username, phone: phone, email: email, province: province, city: city, zone: zone
        postDataList = {}
        postDataList = getPostData(request)

        for key in postDataList:
            HsWriteLog(key + ':' + postDataList[key])

        HsWriteLog('Register_User P====================================================')

        wxHandle = HsSchoolCustom.objects.filter(wxaccount=postDataList['openid']).first()

        if not wxHandle:
            wxHandle = HsSchoolCustom()
            wxHandle.wxaccount = postDataList["openid"]
        wxHandle.name = postDataList["wxname"]
        wxHandle.headimage = postDataList["imgurl"]

        HsWriteLog('postDataList["imgurl"]===================================================' + postDataList["imgurl"])

        wxHandle.alias = postDataList["username"]
        wxHandle.city = "%s-%s-%s"%(postDataList["province"],postDataList["city"],postDataList["zone"])
        wxHandle.email = postDataList['email']
        wxHandle.phone = postDataList["phone"]
        wxHandle.regdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        wxHandle.school = postDataList["school"]

        try:
            wxHandle.save()
        except:
            loginResut = json.dumps({"ErrorInfo": "注册失败", "ErrorId": 2001, "Result": None})
            return HttpResponse(loginResut)

        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)