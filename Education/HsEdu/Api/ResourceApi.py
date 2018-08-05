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
        elif command == "DELE_RESOURCE".upper():
            return ResourceApi.DeleResource(req,command)
        elif command == "RESOURCE_ITEMS".upper():
            return ResourceApi.ResourceItems(req, command)
        elif command == "RESOURCE_CHANGE_STATE".upper():
            return ResourceApi.ChangeState(req, command)
        elif command == "RESOURCE_ADD_ITEM".upper():
            return ResourceApi.ResourceAddItem(req, command)
        elif command == "RESOURCE_DELE_ITEM".upper():
            return ResourceApi.ResourceDeleItem(req, command)

    @staticmethod
    def ResourceDeleItem(request,cmd):
        getParams = UtilHelper.getGetParams(request)
        postParams = UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())

        commitDataList = []

        delResourceItem = HsResourceInfo.objects.filter(code=allParams["code"]).first()

        if not delResourceItem:
            loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
            return HttpResponse(loginResut)

        commitDataList.append(CommitData(delResourceItem, 1))

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
    def ResourceAddItem(request,cmd):
        # 提取参数
        getParams = UtilHelper.getGetParams(request)
        postParams = UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())


        # 查询当前数据是否存在
        resHandle = HsResources.objects.filter(code=allParams["code"],state=1).first()
        if not resHandle:
            loginResut = json.dumps({"ErrorInfo": "主资源不存在", "ErrorId": 20001, "Result": None})
            return HttpResponse(loginResut)

        resItem = HsResourceInfo.objects.filter(code=allParams["itemcode"]).first()

        if not resItem:
            resItem = HsResourceInfo()

        resItem.code = UtilHelper.newUuid()
        resItem.rescode = allParams["code"]
        resItem.index = int(allParams["itemindex"])
        resItem.title = allParams["itemtitle"]
        resItem.introduce = allParams["iteminfo"]
        resItem.restype = 0

        commitDataList = []
        commitDataList.append(CommitData(resItem, 0))

        # 事务提交
        try:
            result = commitCustomDataByTranslate(commitDataList)

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
    def ChangeState(request,cmd):
        getParams = UtilHelper.getGetParams(request)
        postParams = UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())

        commitDataList = []

        changeResource = HsResources.objects.filter(code=allParams["code"]).first()

        if not changeResource:
            loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
            return HttpResponse(loginResut)

        if changeResource.state == 1:
            changeResource.state = 2
        else:
            changeResource.state = 1

        commitDataList.append(CommitData(changeResource, 0))

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
    def ResourceItems(request,cmd):
        # 提取参数
        getParams = UtilHelper.getGetParams(request)
        postParams = UtilHelper.getPostParams(request)
        allParams = dict(getParams.items() + postParams.items())

        resItems = HsResourceInfo.objects.filter(rescode=allParams["code"]).order_by("index")

        limit = int(allParams["limit"])
        pageIndex = int(allParams["page"])

        returnList = []
        oneProg = None
        for index,oneRes in enumerate(resItems):
            if index < limit * (pageIndex - 1) or index >= limit * pageIndex:
                continue

            oneOrgDict = {}
            oneOrgDict['id'] = index + 1
            oneOrgDict['code'] = oneRes.code
            oneOrgDict['index'] = oneRes.index
            oneOrgDict['title'] = oneRes.title
            oneOrgDict['introduce'] = oneRes.introduce
            returnList.append(oneOrgDict)

        dictRtn = {}
        dictRtn["code"] = 0
        dictRtn["msg"] = "success"
        dictRtn["count"] = len(resItems)
        dictRtn["data"] = returnList

        # 返回登录结果
        lResut = json.dumps(dictRtn)
        return HttpResponse(lResut)

    @staticmethod
    def ResourceList(request,cmd):
        # 提取参数
        getParams = UtilHelper.getGetParams(request)
        postParams = UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())


        resources = HsResources.objects.filter(~Q(state=0))


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
            oneOrgDict['id'] = index + 1
            oneOrgDict['code'] = oneRes.code
            oneOrgDict['resname'] = oneRes.restitle
            oneOrgDict['resgrade'] = oneRes.resgrade
            oneOrgDict['resclass'] = oneRes.resclass
            oneOrgDict['resprice'] = oneRes.price
            oneOrgDict['respeople'] = oneRes.name
            oneOrgDict['resviewcount'] = oneRes.viewcount
            oneOrgDict['resorgname'] = oneRes.orgname
            oneOrgDict['resinfo'] = oneRes.resinfo
            oneOrgDict['orginfo'] = oneRes.orginfo

            if oneRes.state == 1:
                oneOrgDict['statename'] = "启用"
            elif oneRes.state == 2:
                oneOrgDict['statename'] = "未启用"

            oneOrgDict['resimage'] =  '<a href="/static/Images/ResImage/%s.jpg" target="__blank">查看</a>' % oneRes.code.encode('utf-8')


            preUrl = None
            if not oneRes.previewurl or len(oneRes.previewurl) <= 0:
                preUrl = "未设置"
            else:
                preUrl = '<a href="%s" target="__blank">查看</a>'%oneRes.previewurl.encode('utf-8')
            oneOrgDict['previewurl'] = preUrl
            oneOrgDict['previewurlabsolute'] = oneRes.previewurl

            resSecret = HsResourcesSecretInfo.objects.filter(rescode=oneRes.code).first()
            if not resSecret:
                pass
            else:
                downloadUrl = None
                if not resSecret.downloadurl or len(resSecret.downloadurl) <= 0:
                    downloadUrl = "未设置"
                else:
                    downloadUrl = '<a href="%s" target="__blank">查看</a>' % resSecret.downloadurl.encode('utf-8')

                oneOrgDict['resdownloadurl'] = downloadUrl
                oneOrgDict['resdownloadurlabsolute'] = resSecret.downloadurl
                oneOrgDict['respassword'] = resSecret.dlpsswd

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
        # 提取参数
        getParams = UtilHelper.getGetParams(request)
        postParams = UtilHelper.getPostParams(request)

        allParams = dict(getParams.items() + postParams.items())


        # 查询当前数据是否存在
        resHandle = HsResources.objects.filter(code=allParams["code"],state=1).first()

        if not resHandle:
            resHandle = HsResources()

        resHandle.code = allParams["code"]
        resHandle.resgrade = allParams["resgrade"]
        resHandle.resclass = allParams["resclass"]
        resHandle.reslevel = 2
        resHandle.restitle = allParams["resname"]
        resHandle.resinfo = allParams["resinfo"]
        resHandle.resimage = allParams["code"] + ".jpg"
        resHandle.price = allParams["resprice"]

        resHandle.name = allParams["respeople"]
        resHandle.viewcount = allParams["resviewcount"]
        resHandle.orgname = allParams["resorgname"]
        resHandle.orgimage = allParams["code"]+ "_org.jpg"
        resHandle.orginfo = allParams["orginfo"]
        resHandle.previewurl = allParams["respreviewurl"]
        resHandle.state = 1


        resdownloadurl = allParams["resdownloadurl"]
        respassword = allParams["respassword"]


        commitDataList = []
        commitDataList.append(CommitData(resHandle, 0))

        commitDataList.append(CommitData(HsResourcesSecretInfo.objects.filter(rescode=allParams["code"]),1))

        newSecretInfo = HsResourcesSecretInfo()
        newSecretInfo.rescode = allParams["code"]
        newSecretInfo.downloadurl = resdownloadurl
        newSecretInfo.dlpsswd = respassword
        commitDataList.append(CommitData(newSecretInfo, 0))

        # 事务提交
        try:
            result = commitCustomDataByTranslate(commitDataList)

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
    @csrf_exempt
    def uploadFile(request):
        code = None
        # 提取参数
        getParams = UtilHelper.getGetParams(request)

        if not getParams.has_key("code") or not getParams.has_key("type"):
            loginResut = json.dumps({"ErrorInfo": "参数错误", "ErrorId": 2999, "Result": {}})
            return HttpResponse(loginResut)

        destination = os.path.join(STATIC_ROOT, "Images")
        destination = os.path.join(destination, "ResImage")

        fName = None
        code = getParams["code"]
        type = int(getParams["type"])

        if type == 0:
            fName = code + "_org.jpg"
        elif type == 1:
            fName = code + ".jpg"

        destination = open(os.path.join(destination, fName), 'wb+')  # 打开特定的文件进行二进制的写操作
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        dict={}
        dict["code"] = 0

        lResut = json.dumps(dict)
        return HttpResponse(lResut)

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

    @staticmethod
    @csrf_exempt
    def OpenResourceItems(request):
        renterDict = {}
        return render(request, 'resource_items.html',renterDict )
