#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *
class AdminApi(object):
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

        command = request.GET.get('Command')
        if command:
            command = command.upper()

        if  command  == None:
            return AdminApi.OpenAdmin(request)

    @staticmethod
    def OpenAdmin(request):
        renterDict = {}
        return render(request, './admin/admin.html',renterDict )

    @staticmethod
    def getTestData(request):

        rtnDiction = {}

        dataList = []
        for index in range(100):
            oneRecord = {}
            oneRecord['id'] = 'aaaaa'
            oneRecord['username'] = 'aaaaa'
            oneRecord['sex'] = 'aaaaa'
            oneRecord['city'] = 'aaaaa'
            oneRecord['sign'] = 'aaaaa'
            oneRecord['experience'] = 'aaaaa'
            oneRecord['score'] = 'aaaaa'
            oneRecord['classify'] = 'aaaaa'
            oneRecord['wealth'] = 'aaaaa'
            oneRecord['fixed'] = 'aaaaa'
            dataList.append(oneRecord)

        rtnDiction['code'] = 0
        rtnDiction['msg'] = "Success"
        rtnDiction['data'] = dataList
        rtnDiction['count'] = len(dataList)


        loginResut = json.dumps(rtnDiction)
        return HttpResponse(loginResut)