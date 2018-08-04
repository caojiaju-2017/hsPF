#!/usr/bin/env python
# -*- coding: utf-8 -*-
from include import *
from UtilHelper import *
class ResourceApi(object):

    @staticmethod
    @csrf_exempt
    def CommandDispatch(req):
        command = req.GET.get('command').upper()
        if command == "RESOURCE_LIST".upper():
            return ResourceApi.ResourceList(req,command)
        elif command == "ADD_RESOURCE".upper():
            return ResourceApi.AddResource(req,command)
        elif command == "EDIT_RESOURCE".upper():
            return ResourceApi.EditResource(req,command)
        elif command == "DELE_RESOURCE".upper():
            return ResourceApi.DeleResource(req,command)



    @staticmethod
    def ResourceList(request,cmd):
        # 提取参数
        getParams = UtilHelper.getGetParams(request)
        postParams = UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())


        resources = HsResources.objects.filter(state=1)


        stype = int(allParams["stype"])
        if stype != 0:
            resources = resources.filter(resclass=stype)

        limit = int(allParams["limit"])
        pageIndex = int(allParams["page"])
        fliterStr = None

        try:
            fliterStr = allParams["fliterstring"]

            if not fliterStr or len(fliterStr) <= 0:
                fliterStr = None
        except:
            pass

        # 对每个广告检查终端数据授权状态
        afterFliters = []
        for oneRes in resources:
            if fliterStr :
                if fliterStr in oneRes.restitle:
                    afterFliters.append(oneRes)
                elif fliterStr in oneRes.resinfo:
                    afterFliters.append(oneRes)
            else:
                afterFliters.append(oneRes)

        returnList = []
        oneProg = None
        for index,oneRes in enumerate(afterFliters):
            if index < limit * (pageIndex - 1) or index >= limit * pageIndex:
                continue

            oneOrgDict = {}
            oneOrgDict['id'] = oneRes.id
            oneOrgDict['code'] = oneRes.code
            oneOrgDict['reslevel'] = oneRes.reslevel
            oneOrgDict['resclass'] = oneRes.resclass
            oneOrgDict['price'] = oneRes.price
            oneOrgDict['title'] = oneRes.restitle


            preUrl = None
            if not oneRes.previewurl or len(oneRes.previewurl) <= 0:
                preUrl = "未设置"
            else:
                preUrl = '<a href="%s" target="__blank">查看</a>'%oneRes.previewurl.encode('utf-8')
            oneOrgDict['previewurl'] = preUrl
            returnList.append(oneOrgDict)

        dictRtn = {}
        dictRtn["code"] = 0
        dictRtn["msg"] = "success"
        dictRtn["count"] = len(afterFliters)
        dictRtn["data"] = returnList

        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)

    @staticmethod
    def AddResource(request,cmd):
        '''
        查询日程列表
        :param request:
        :return:
        '''
        LoggerHandle.writeLogDevelope("日程添加指令%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)


        # 验证参数完整性
        paramCompleteness,info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)

        if paramCompleteness:
            LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        else:
            LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
            loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 参数验签
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)

        # 检查logioncode是否为权力机构
        acntHandle = ByAdAccount.objects.filter(account = allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        orgHandel = ByAdOrganization.objects.filter(code=allParams["orgsign"]).first()
        if not orgHandel:
            LoggerHandle.writeLogDevelope("当前单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前单位数据异常", "ErrorId": 20008, "Result": {}})
            return HttpResponse(loginResut)


        # 判断当前是否存在重名日程
        schList = BySchedules.objects.filter(orgcode=orgHandel,state=1)

        for oneSch in schList:
            if oneSch.name == allParams["name"]:
                LoggerHandle.writeLogDevelope("日程名重复", request)
                loginResut = json.dumps({"ErrorInfo": "日程名重复", "ErrorId": 20007, "Result": {}})
                return HttpResponse(loginResut)

        # 提取参数
        type = int(allParams["type"])
        name = allParams["name"]
        schInfo = allParams["scheduleinfo"]

        newSch = BySchedules()
        newSch.code = UtilHelper.UtilHelper.newUuid()
        newSch.type = type
        newSch.name = name
        newSch.orgcode =orgHandel
        newSch.state = 1
        newSch.regtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        commitDataList = []
        commitDataList.append(CommitData(newSch, 0))
        # try:
        #     newSch.save()
        # except Exception,ex:
        #     loginResut = json.dumps({"ErrorInfo": "日程数据存储失败", "ErrorId": 20007, "Result": {}})
        #     return HttpResponse(loginResut)


        schInfoList = schInfo.split("&")
        newDict = {}
        for oneSch in schInfoList:
            if not oneSch or len(oneSch) <= 0:
                continue
            splitInfo = oneSch.split("|")

            if len(splitInfo) != 2:
                continue

            keyValue = splitInfo[0]
            timeValues = splitInfo[1]

            # 分拆开始时间   结束时间
            timeSplit = timeValues.split("-")
            if len(timeSplit) != 2:
                continue

            # 构造写入指令--ByScheduleDetailPre--- 循环关键明细 日期或周序号或日期序号
            detailPro = None
            # if type == 0:
            #     detailPro = ByScheduleDetailPre.objects.filter(scode = newSch,date=keyValue).first()
            # elif type == 1:
            #     detailPro = ByScheduleDetailPre.objects.filter(scode=newSch, week=keyValue).first()
            # elif type == 2:
            #     detailPro = ByScheduleDetailPre.objects.filter(scode=newSch, nomon =keyValue).first()


            # 创建
            detailProCode = None
            if not newDict.has_key(keyValue):
                detailPro = ByScheduleDetailPre()
                detailPro.code = UtilHelper.UtilHelper.newUuid()
                detailPro.week = -1
                detailPro.nomon = -1
                if type == 0:
                    detailPro.date = keyValue
                elif type == 1:
                    detailPro.week = keyValue
                elif type == 2:
                    detailPro.nomon = keyValue

                # detailPro.scode = BySchedules.objects.filter(code= newSch.code).first()
                detailPro.scode_id = newSch.code
                commitDataList.append(CommitData(detailPro, 0))

                newDict[keyValue] = detailPro.code
                detailProCode = detailPro.code
                # try:
                #     detailPro.save()
                # except Exception,ex:
                #     loginResut = json.dumps({"ErrorInfo": "日程数据存储失败", "ErrorId": 20007, "Result": {}})
                #     return HttpResponse(loginResut)
            else:
                detailProCode = newDict[keyValue]
            # 创建日程明细---- ByScheduleDetail
            schDetail = ByScheduleDetail()
            schDetail.code = UtilHelper.UtilHelper.newUuid()
            schDetail.scode_id = detailProCode
            schDetail.starttime = timeSplit[0]
            schDetail.stoptime = timeSplit[1]
            commitDataList.append(CommitData(schDetail, 0))

            pass


        # 事务提交
        try:
            result = DBHelper.commitCustomDataByTranslate(commitDataList)

            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)


        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    def DeleResource(request,cmd):
        getParams = UtilHelper.getGetParams(request)
        postParams = UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())

        commitDataList = []

        delResource = HsResources.objects.filter(code=allParams["code"]).first()

        if not delResource:
            loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
            return HttpResponse(loginResut)

        delResource.state = 0
        commitDataList.append(CommitData(delResource, 0))

        # 事务提交
        try:
            result = commitCustomDataByTranslate(commitDataList)

            if not result:
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)


        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)


    @staticmethod
    def EditResource(request,cmd):
        '''
        终端编辑
        :param request:
        :return:
        '''

        LoggerHandle.writeLogDevelope("收到终端编辑指令%s"%cmd.encode('utf-8'), request)
        LoggerHandle.writeLog("%s" % cmd.encode('utf-8'), request)

        # 提取参数
        getParams = UtilHelper.UtilHelper.getGetParams(request)
        postParams = UtilHelper.UtilHelper.getPostParams(request)

        allParams = dict(getParams.items()+postParams.items())
        LoggerHandle.writeLogDevelope("指令GET参数" + str(getParams), request)
        LoggerHandle.writeLogDevelope("指令POST参数" + str(postParams), request)

        # 验证参数完整性
        paramCompleteness,info = ParamCheckHelper.ParamCheckHelper.getParamModule(cmd).checkParamComplete(allParams)

        if paramCompleteness:
            LoggerHandle.writeLogDevelope("参数完整,符合要求", request)
        else:
            LoggerHandle.writeLogDevelope("参数不完整，缺少：" + info, request)
            loginResut = json.dumps({"ErrorInfo": "参数不足，缺少：" + info, "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 参数验签
        verifyResult = VerifyHelper.VerifyHelper.verifyParam(allParams)
        if verifyResult:
            LoggerHandle.writeLogDevelope("参数验签成功", request)
        else:
            LoggerHandle.writeLogDevelope("参数验签失败", request)
            loginResut = json.dumps({"ErrorInfo": "参数验签失败", "ErrorId": 20002, "Result": {}})
            return HttpResponse(loginResut)


        # 检查logioncode是否为权力机构
        acntHandle = ByAdAccount.objects.filter(account = allParams["logincode"]).first()

        # 检查当前账号是否具有当前权限
        if not acntHandle:
            LoggerHandle.writeLogDevelope("当前账号数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "当前账号数据异常", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        resultPrivilegeSign = PrivilegeHelper.PrivilegeHelper.funcPrivCheck(cmd, acntHandle)
        if not resultPrivilegeSign:
            LoggerHandle.writeLogDevelope("权限受限", request)
            loginResut = json.dumps({"ErrorInfo": "权限受限", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        # 检查当前账户是否具有权限
        ownerOrgHandel = ByAdOrganization.objects.filter(code = allParams["orgcode"]).first()
        if not ownerOrgHandel:
            LoggerHandle.writeLogDevelope("归属单位数据异常", request)
            loginResut = json.dumps({"ErrorInfo": "归属单位数据异常", "ErrorId": 20006, "Result": {}})
            return HttpResponse(loginResut)

        currentAllOrgs = OrgTree.getOrgTreeObjects(ownerOrgHandel)
        # 检查该MAC地址是否已经被注册
        currentAllOrgs.append(ownerOrgHandel)

        playerList = None
        for oneOrg in currentAllOrgs:
            if not playerList :
                playerList = ByAdPlayers.objects.filter(orgcode=oneOrg,state=1).order_by("-id")
            else:
                playerList = playerList | ByAdPlayers.objects.filter(orgcode=oneOrg,state=1).order_by("-id")

        # 当前单位下检查名字唯一性
        for onePlay in playerList:
            if onePlay.type == 0:  #led设备，
                continue
            if onePlay.name == allParams["name"]:
                LoggerHandle.writeLogDevelope("终端名重复", request)
                loginResut = json.dumps({"ErrorInfo": "终端名重复", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)


        # 全网机构内检查ip和mac的合法性
        orgRootTemp = ByAdOrganization.objects.filter(code = allParams["orgsign"]).first()
        currentAllOrgsTemps = OrgTree.getOrgTreeObjects(orgRootTemp)
        # 检查该MAC地址是否已经被注册
        currentAllOrgsTemps.append(orgRootTemp)
        playerListTempsContainMe = None
        for oneOrg in currentAllOrgsTemps:
            if not playerListTempsContainMe :
                playerListTempsContainMe = ByAdPlayers.objects.filter(orgcode=oneOrg,state=1).order_by("-id")
            else:
                playerListTempsContainMe = playerListTempsContainMe | ByAdPlayers.objects.filter(orgcode=oneOrg,state=1).order_by("-id")

        # 自我排除
        playerListTemps = playerListTempsContainMe.filter(~Q(code = allParams["code"]))
        for onePlay in playerListTemps:
            if onePlay.type == 0:  #led设备，
                continue

            if onePlay.code == allParams["code"]:
                continue

            if onePlay.mac == allParams["mac"]:
                LoggerHandle.writeLogDevelope("MAC地址已被注册", request)
                loginResut = json.dumps({"ErrorInfo": "MAC地址已被注册", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)
            if onePlay.ipaddress == allParams["ipaddress"]:
                LoggerHandle.writeLogDevelope("IP地址冲突", request)
                loginResut = json.dumps({"ErrorInfo": "IP地址冲突", "ErrorId": 20006, "Result": {}})
                return HttpResponse(loginResut)

        regPlayer = playerListTempsContainMe.filter(code = allParams["code"]).first()
        # 如果已经注册--- 直接返回成功
        # regPlayer = ByAdPlayers()
        # regPlayer.code = UtilHelper.UtilHelper.newUuid()
        regPlayer.orgcode = ownerOrgHandel
        # regPlayer.orgcode_id = allParams["orgsign"]
        regPlayer.name = allParams["name"]
        # regPlayer.gcode = None  # 新终端未分组
        regPlayer.ipaddress = allParams["ipaddress"]
        regPlayer.mac = allParams["mac"]
        # regPlayer.lastcmd = None
        # regPlayer.lastcmdresult = None
        # regPlayer.lastlogintime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # regPlayer.online = 1
        # regPlayer.pcode = None
        # regPlayer.terminalsign = regPlayer.code
        # regPlayer.type = 0
        # regPlayer.state = 1
        regPlayer.port = allParams["port"]
        # regPlayer.ledtype = allParams["ledtype"]

        try:
            regPlayer.save()
        except Exception, ex:
            LoggerHandle.writeLogDevelope("注册失败", request)
            loginResut = json.dumps({"ErrorInfo": "注册失败", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        # 返回登录结果
        loginResut = json.dumps({"ErrorInfo": "终端登记成功，请联系管理员授权", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)






    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    @staticmethod
    @csrf_exempt
    def LoginAdmin(request):
        renterDict = {}
        return render(request, 'login_admin.html',renterDict )

    @staticmethod
    @csrf_exempt
    def OpenSchoolPCHome(request):
        renterDict = {}
        return render(request, 'resource.html',renterDict )

    @staticmethod
    @csrf_exempt
    def OpenManageResource(request):
        renterDict = {}
        return render(request, 'resource_add.html',renterDict )
