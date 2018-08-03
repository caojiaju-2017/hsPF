#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *


class CustomApi(object):
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
        if command == "Open_Resource".upper():
            return CustomApi.Open_Resource(request)
        elif command == "Query_Res".upper():
            return CustomApi.Query_Res(request)
        elif command == "view_remark".upper():
            return CustomApi.Open_Remark(request)
        elif command == "Get_Orders".upper():
            return CustomApi.Open_OrdersPage(request)
        elif command == "View_Order".upper():
            return CustomApi.ViewOrder(request)
        elif command == "Open_Contact".upper():
            return CustomApi.OpenContact(request)
        elif command == "Send_Suggest".upper():
            return CustomApi.SendSuggest(request)
        elif command == "Release_Suggest".upper():
            return CustomApi.ReleaseSuggest(request)
        elif command == "Release_Remark".upper():
            return CustomApi.ReleaseRemark(request)
        elif command == "Open_ENGame".upper():
            return CustomApi.OpenENGame(request)
        elif command == "View_MyOrganization".upper():
            return CustomApi.ViewMyOrganization(request)
        elif command == "View_Tasks".upper():
            return CustomApi.ViewTasks(request)
        elif command == "View_News".upper():
            return CustomApi.ViewNews(request)
        elif command == "Query_News".upper():
            return CustomApi.QueryNews(request)
        elif command == "WX_PAY_SUCCESS".upper():
            return CustomApi.WxPaySuccess(request)
        # elif command == "WX_PAY_SUCCESS".upper():
        #     return CustomApi.WxPaySuccess(request)
    @staticmethod
    def WxPaySuccess(request):
        postDataList = {}
        postDataList = getPostData(request)

        ordercoce = postDataList["ordercoce"]
        openid = postDataList['openid']

        if ordercoce == 'GAME_PAY':
            csmHandle = HsGameCustom.objects.filter(code = openid).first()
            if not csmHandle:
                csmHandle = HsGameCustom()
                csmHandle.code = openid
                csmHandle.sevstart = time.strftime('%Y-%m-%d', time.localtime(time.time()))

            currentdate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            now = datetime.datetime.now()
            delta = datetime.timedelta(days=30)
            n_days = now + delta
            csmHandle.sevstop = n_days.strftime('%Y-%m-%d')

            commitDataList = []
            commitDataList.append(CommitData(csmHandle, 0))

            # 清空分享次数
            shareHandle = HsCustomGameShareCount.objects.filter(ccode=openid).first()
            if shareHandle:
                shareHandle.sharecount = 0
                commitDataList.append(CommitData(shareHandle, 0))

            # 事务提交
            try:
                result = commitCustomDataByTranslate(commitDataList)

                if not result:
                    loginResut = json.dumps({"ErrorInfo": "数据写入失败", "ErrorId": 99999, "Result": None})
                    return HttpResponse(loginResut)
            except Exception, ex:
                loginResut = json.dumps({"ErrorInfo": "数据写入失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        else:
            orderHandle = HsOrders.objects.filter(code=ordercoce).first()
            if not orderHandle:
                HsWriteLog('Order Data Not found')
                loginResut = json.dumps({"ErrorInfo": "订单数据不存在", "ErrorId": 20001, "Result": None})
                return HttpResponse(loginResut)

            if orderHandle.usercode != openid:
                HsWriteLog('Order open id not same')
                loginResut = json.dumps({"ErrorInfo": "订单购买者数据异常", "ErrorId": 20002, "Result": None})
                return HttpResponse(loginResut)
            orderHandle.state = 6

            try:
                orderHandle.save()
                HsWriteLog('Order save success')
            except Exception,ex:
                HsWriteLog('Order save faild' + ex.message)
                pass

        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def Open_Resource(request):
        if (not HsShareData.IsDebug):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "Images"), "erweima_img.png"))
            return render(request, 'warning_notice.html', {"erweima_img": "/static/Images/erweima_img.png"})

        code = request.GET.get('code')
        openid = request.GET.get('openid')
        HsWriteLog("Resource code =%s" % (code))

        renterDict = {}

        resourceHandle = HsResources.objects.filter(code=code).first()

        if not resourceHandle:
            return render(request, '404.html', {})

        renterDict['Name'] = resourceHandle.restitle
        renterDict['Price'] = resourceHandle.price
        renterDict['Introduce'] = resourceHandle.resinfo
        renterDict['PreviewUrl'] = resourceHandle.previewurl
        renterDict['OrgName'] = resourceHandle.orgname
        renterDict['OrgImage'] = resourceHandle.orgimage
        renterDict['OrgInfo'] = resourceHandle.orginfo

        resourceItems = HsResourceInfo.objects.filter(rescode=code).order_by('index')
        renterDictAarry = []
        for oneItem in resourceItems:
            oneItemDict = {}
            oneItemDict["Index"] = oneItem.index
            oneItemDict["Title"] = oneItem.title
            oneItemDict["Info"] = oneItem.introduce
            renterDictAarry.append(oneItemDict)

        renterDict['Res_Datas'] = renterDictAarry
        renterDict['Res_Code'] = code

        # 检查当前用户是否购买了该资源
        orderHandle = HsOrders.objects.filter(goodscode=code,usercode=openid,state=6).first()

        HsWriteLog("Check Order Info,Resource code =%s,UserCode=%s" % (code,openid))

        if orderHandle:
            renterDict['Res_Priv'] = 1
            renterDict['Priv_Title'] = "查看"
        else:
            renterDict['Res_Priv'] = 0
            renterDict['Priv_Title'] = "购买"

        allRemarks = HsResRemark.objects.filter(rcode = code).order_by("reltime")
        okRemarks = []
        for one in allRemarks:
            if one.type == 0:  #机器人的留言
                okRemarks.append(one)
                continue
            if one.usercode != openid:
                continue
            okRemarks.append(one)

        renterDict['Remark_Txt'] = len(okRemarks)

        return render(request, './home/res/res_detail.html', renterDict)

    @staticmethod
    def Query_Res(request):
        pageIndex = int(request.GET.get('pageindex'))
        pageSize = int(request.GET.get('pagesize'))
        filterS = request.GET.get('filter')
        
        # grade = request.GET.get('grade')  # 学历
        # gclass = request.GET.get('class')  # 班级
        subject = int(request.GET.get('subject'))  # 科目

        # HsWriteLog("pageindex=%d,pageSize=%d,filter=%s,grade=%s,gclass=%s,subject=%s" % (
        #     pageIndex, pageSize, filterS, grade, gclass, subject))

        pageIndex = int(request.GET.get('pageindex'))
        pageSize = int(request.GET.get('pagesize'))

        # gradeid = getNameId(0, grade)
        # gclassid = getNameId(1, gclass)
        # subjectid = getNameId(2, subject)
        ipreques = request.META['REMOTE_ADDR']

        # HsWriteLog("gradeid=%d,gclassid=%d,subjectid=%d,filterS=%s" % (
        #     gradeid, gclassid, subjectid, filterS))

        resArray = []
        resDatas = None

        resDatas = queryResource(subject, filterS)
        HsWriteLog("queryResource ,get record count=%d" % len(resDatas))
        resDatas = resDatas[pageIndex * pageSize:pageIndex * pageSize + pageSize]
        for oneRes in resDatas:
            resDict = {}
            resDict['ResGrade'] = getName(0, oneRes.resgrade)
            resDict['ResLevel'] = getName(1, oneRes.reslevel)
            resDict['ResClass'] = getName(2, oneRes.resclass)
            resDict['ResInfo'] = oneRes.resinfo[:50]
            resDict['ResImage'] = oneRes.resimage
            resDict['Price'] = oneRes.price
            resDict['Name'] = oneRes.name
            resDict['ViewCount'] = oneRes.viewcount
            resDict['BuyCount'] = oneRes.viewcount
            resDict['ResTitle'] = oneRes.restitle
            resDict['OrgName'] = oneRes.orgname
            resDict['Code'] = oneRes.code
            resDict['ResImage'] = oneRes.resimage
            resourceItems = HsResourceInfo.objects.filter(rescode=oneRes.code)
            resDict['ResItemCount'] = len(resourceItems)

            resArray.append(resDict)

        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": resArray})
        return HttpResponse(loginResut)



    @staticmethod
    def OpenENGame(request):
        if (not HsShareData.IsDebug):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "Images"), "erweima_img.png"))
            return render(request, 'warning_notice.html', {"erweima_img": "/static/Images/erweima_img.png"})

        openid = request.GET.get('openid')
        # HsWriteLog('OpenENGame openid=================%s====================' % openid)
        # HsWriteLog('OpenENGame openid=================oQE6Bt6PVtEL9XzfDSI_Xj0Ed0e8====================')
        renterDict={}
        # if openid == "oQE6Bt6PVtEL9XzfDSI_Xj0Ed0e8":
        #     renterDict['game_open'] = 1
        # else:
        #     renterDict['game_open'] = 0
        return render(request, './home/../../templates/game/game_home.html', renterDict)

    @staticmethod
    def Open_Remark(request):
        if (not HsShareData.IsDebug):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "Images"), "erweima_img.png"))
            return render(request, 'warning_notice.html', {"erweima_img": "/static/Images/erweima_img.png"})

        code = request.GET.get('code')
        openid = request.GET.get('openid')

        allRemarks = HsResRemark.objects.filter(rcode = code).order_by("reltime")

        HsWriteLog('allRemarks code=================%s====================' % code)
        HsWriteLog('allRemarks openid=================%s====================' % openid)
        HsWriteLog('allRemarks Result=================%d====================' % len(allRemarks))
        okRemarks = []
        for one in allRemarks:
            if one.type == 0:  #机器人的留言
                if one.usercode == openid:
                    one.username = "我"
                okRemarks.append(one)
                continue
            if one.usercode != openid:
                continue

            one.username = "我"
            okRemarks.append(one)
        renterDict = {}

        resultAarray = []
        for index,oneRemark in enumerate(okRemarks):
            onedict = {}
            onedict["UserName"] = oneRemark.username
            onedict["RemarkTime"] = oneRemark.reltime
            onedict["Index"] = "第%d楼" % (index + 1)
            onedict["Info"] = oneRemark.content
            resultAarray.append(onedict)
            
        renterDict["RemarkInfos"]= resultAarray
        renterDict["RCode"]= code

        return render(request, './home/res/view_remark.html', renterDict)

    @staticmethod
    def Open_OrdersPage(request):
        if (not HsShareData.IsDebug):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "Images"), "erweima_img.png"))
            return render(request, 'warning_notice.html', {"erweima_img": "/static/Images/erweima_img.png"})

        try:
            openId = request.GET.get('openId')
        except:
            openId = None

        # HsWriteLog('WX OpenId=====================================' + openId)
        renterDict = {}
        resultList = []

        orderDatas = HsOrders.objects.filter(usercode=openId, state=6)
        for oneOrder in orderDatas:
            oneRecord = {}
            oneRecord["code"] = oneOrder.code
            oneRecord["goodscode"] = oneOrder.goodscode
            oneRecord["time"] = oneOrder.ordertime

            resHandle = HsResources.objects.filter(code=oneOrder.goodscode).first()
            if not resHandle:
                continue

            oneRecord["title"] = resHandle.restitle
            oneRecord["simpleimage"] = resHandle.resimage
            HsWriteLog('resHandle.resimage=====================================' + resHandle.resimage)
            resultList.append(oneRecord)

        renterDict['My_Orders'] = resultList
        return render(request, './home/usercenter/res_order.html', renterDict)

    @staticmethod
    def ViewOrder(request):
        if (not HsShareData.IsDebug):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "Images"), "erweima_img.png"))
            return render(request, 'warning_notice.html', {"erweima_img": "/static/Images/erweima_img.png"})

        try:
            resCode = request.GET.get('code')
        except:
            resCode = None

        HsWriteLog('orderCode=====================================' + resCode)

        orderHandler = None
        if resCode:
            # 查询订单数据
            orderHandler = HsResourcesSecretInfo.objects.filter(rescode=resCode).first()

        renterDict = {}
        configs = HsSysConfig.objects.all()
        for oneCfg in configs:
            if oneCfg.ckey == "SYS_QQ":
                renterDict["SYS_QQ"] = oneCfg.cvalue
            elif oneCfg.ckey == "SYS_PHONE":
                renterDict["SYS_PHONE"] = oneCfg.cvalue
            elif oneCfg.ckey == "SYS_EWM":
                renterDict["SYS_EWM"] = oneCfg.cvalue

        if orderHandler:
            renterDict['BaiduNetUrl'] = orderHandler.downloadurl
            renterDict['BaiduNetUrlPswd'] = orderHandler.dlpsswd
        else:
            renterDict['BaiduNetUrl'] = "资源链接失效"
            renterDict['BaiduNetUrlPswd'] = '资源失效'
        return render(request, './home/usercenter/order_detail_info.html', renterDict)

    @staticmethod
    def OpenContact(request):
        if (not HsShareData.IsDebug):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "Images"), "erweima_img.png"))
            return render(request, 'warning_notice.html', {"erweima_img": "/static/Images/erweima_img.png"})

        renterDict = {}
        configs = HsSysConfig.objects.all()
        for oneCfg in configs:
            if oneCfg.ckey == "SYS_QQ":
                renterDict["SYS_QQ"] = oneCfg.cvalue
            elif oneCfg.ckey == "SYS_PHONE":
                renterDict["SYS_PHONE"] = oneCfg.cvalue
            elif oneCfg.ckey == "SYS_EWM":
                renterDict["SYS_EWM"] = oneCfg.cvalue

        return render(request, './home/usercenter/cooperation.html', renterDict)

    @staticmethod
    def SendSuggest(request):
        if (not HsShareData.IsDebug):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "Images"), "erweima_img.png"))
            return render(request, 'warning_notice.html', {"erweima_img": "/static/Images/erweima_img.png"})

        renterDict = {}
        return render(request, './home/usercenter/suggest.html', renterDict)

    @staticmethod
    def ViewNews(request):
        if (not HsShareData.IsDebug):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "Images"), "erweima_img.png"))
            return render(request, 'warning_notice.html', {"erweima_img": "/static/Images/erweima_img.png"})
        renterDict = {}

        Code = request.GET.get('Code')

        newsHandle = HsNews.objects.filter(code=Code).first()

        renterDict["NewsTitle"] = newsHandle.title
        renterDict["NewsCode"] = newsHandle.code

        if not newsHandle:
            return render(request, './home/news/view_news.html', renterDict)

        Items = HsNewsInfo.objects.filter(ncode=Code).order_by('tindex')

        arr = []
        for one in Items:
            abc = {}
            abc["Index"] = one.tindex
            abc["StepName"] = "第%d:" % (one.tindex + 1)
            abc["Title"] = one.title[:15] + "..."
            abc["Info"] = one.info.replace("\n","<br/>").replace("<br/><br/>","<br/>")
            abc["Image"] = one.imagename
            arr.append(abc)

        renterDict["TitleInfos"] = arr

        # return render(request, './home/news/' + newsInfo.urlname, renterDict)
        return render(request, './home/news/view_news.html', renterDict)

    @staticmethod
    def QueryNews(request):
        pageIndex = int(request.GET.get('pageindex'))
        pageSize = int(request.GET.get('pagesize'))
        # start = int(request.GET.get('start'))

        ipreques = request.META['REMOTE_ADDR']
        results = HsNews.objects.filter().order_by('-newstime')[pageIndex * pageSize:pageIndex * pageSize + pageSize]

        rtnResult = []
        for index, one in enumerate(results):
            oneNews = {}
            oneNews['Title'] = one.title
            oneNews["Info"] = one.info[0:60]
            oneNews['Date'] = one.newstime
            oneNews['Image'] = one.image
            oneNews['Code'] = one.code
            rtnResult.append(oneNews)

        # print rtnResult
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": rtnResult})
        return HttpResponse(loginResut)

    @staticmethod
    def ReleaseSuggest(request):
        if (not HsShareData.IsDebug):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "Images"), "erweima_img.png"))
            return render(request, 'warning_notice.html', {"erweima_img": "/static/Images/erweima_img.png"})

        postDataList = {}
        postDataList = getPostData(request)

        ucode = postDataList["ucode".lower()].encode('utf-8')
        title = postDataList["title".lower()].encode('utf-8')
        customname = postDataList["customname".lower()].encode('utf-8')
        customphone = postDataList["customphone".lower()].encode('utf-8')
        detail = postDataList["detail".lower()].encode('utf-8')

        # 推送邮件
        try:
            bodyData = "用户%s：通过微店反馈意见 \n他的电话为：%s \n 意见详细描述为：%s" % (customname, customphone, detail)
            # BaseEmail.sendMail(bodyData, title)
            # sendmailThread = threading.Thread(target=BaseEmail.sendMail, args=(bodyData,title,))
            # sendmailThread.setDaemon(True)
            # sendmailThread.start()
        except Exception, ex:
            raise ex
            HsWriteLog('send mail failed!=====================================')

        newSuggest = HsSuggests()
        newSuggest.code = uuid.uuid1().__str__().replace("-", "")
        newSuggest.phone = customphone
        newSuggest.content = detail
        newSuggest.reltime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        newSuggest.title = title
        newSuggest.usercode = ucode
        newSuggest.username = customname

        commitDataList = []
        commitDataList.append(CommitData(newSuggest, 0))

        # 事务提交
        try:
            result = commitCustomDataByTranslate(commitDataList)

            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            print ex
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)

        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)



    @staticmethod
    def ReleaseRemark(request):
        if (not HsShareData.IsDebug):
            url = "http://" + request.META['HTTP_HOST'] + request.META['PATH_INFO'] + request.META['QUERY_STRING']
            img = qrcode.make(url)
            img.save(os.path.join(os.path.join(STATIC_ROOT, "Images"), "erweima_img.png"))
            return render(request, 'warning_notice.html', {"erweima_img": "/static/Images/erweima_img.png"})

        postDataList = {}
        postDataList = getPostData(request)

        openid = postDataList["openid".lower()].encode('utf-8')
        body = postDataList["body".lower()].encode('utf-8')
        rcode = postDataList["rcode".lower()].encode('utf-8')

        HsWriteLog('ReleaseRemark!=====================================' + rcode)

        openIdHandle = HsCustom.objects.filter(wxaccount=openid).first()
        userName = getRadomName(8)

        if openIdHandle:
            userName = openIdHandle.name

        newRemark = HsResRemark()
        newRemark.code = uuid.uuid1().__str__().replace("-", "")
        newRemark.content = body
        newRemark.rcode = rcode
        newRemark.type = 1
        newRemark.username = userName
        newRemark.reltime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        newRemark.usercode = openid

        commitDataList = []
        commitDataList.append(CommitData(newRemark, 0))

        # 事务提交
        try:
            result = commitCustomDataByTranslate(commitDataList)

            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            print ex
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)

        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def everyDayWord(request):
        datecurrent = time.strftime("%Y-%m-%d", time.localtime())

        wordHandle = HsEvyDayWord.objects.filter(evdate=datecurrent).first()

        renterDict = {}
        if not wordHandle:
            renterDict["word"] = 'face'
            renterDict["date"] = datecurrent
            renterDict["orgname"] = '汉森教育2013'
            renterDict["wordcontent"] = '今天我们要学的词组是face。Face是脸，面孔，作为动词，face有面对的意思。比如，学会面对困难--learn to face difficulties. 美国人民在911以后面临如何防范恐怖袭击的巨大挑战，"The American people faced the big challenge of how to prevent terrorist attacks after 911." 还比如美国司法部长冈萨雷斯因司法部解雇八位联邦检察官而在国会受到严厉质询，"Alberto Gonzales faced tough questioning about his role in the controversy." 今天我们学习的词组是face...'
            renterDict["soundlink"] = '/static/everydate/default_word.mp3'
        else:
            renterDict["word"] = wordHandle.word
            renterDict["date"] = datecurrent
            renterDict["orgname"] = '汉森教育2013'
            renterDict["wordcontent"] = wordHandle.content
            renterDict["soundlink"] = '/static/everydate/%s/%s'%(renterDict["date"].replace('-',''),wordHandle.sound)
        return render(request, 'everyday/ed_word.html',renterDict )


    @staticmethod
    def everyDaySentence(request):
        datecurrent = time.strftime("%Y-%m-%d", time.localtime())
        wordHandle = HsEvySentence.objects.filter(evdate=datecurrent).first()
        renterDict = {}

        if not wordHandle:
            renterDict["sentence"] = 'I want to sleep but ... ...'
            renterDict["date"] = datecurrent
            renterDict["orgname"] = '汉森教育2013'
            renterDict["encontent"] = 'I want to sleep but my brain won\'t stop talking to itself. '
            renterDict["cncontent"] = '我想睡觉，但我的脑子在那儿自言自语，无休无止。'
            renterDict["soundlink"] = '/static/everydate/default_sentence.mp3'
        else:
            renterDict["sentence"] = wordHandle.encontent[:15] + " ... ..."
            renterDict["date"] = datecurrent
            renterDict["orgname"] = '汉森教育2013'
            renterDict["encontent"] = wordHandle.encontent
            renterDict["cncontent"] = wordHandle.cncontent
            renterDict["soundlink"] = '/static/everydate/%s/sentence_sound.mp3' % (renterDict["date"].replace('-', ''))
        return render(request, 'everyday/ed_sentence.html',renterDict )


    @staticmethod
    def everyDayRead(request):
        datecurrent = time.strftime("%Y-%m-%d", time.localtime())
        wordHandle = HsEvyRead.objects.filter(evdate=datecurrent).first()
        renterDict = {}

        if not wordHandle:
            renterDict["title"] = "今日文章还未发布"
        else:
            renterDict["title"] = wordHandle.title
            renterDict["date"] = datecurrent
            renterDict["orgname"] = '汉森教育2013'
            renterDict["content"] = wordHandle.content

        return render(request, 'everyday/ed_read.html',renterDict )

