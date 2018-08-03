#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *
# globalWords = HsGameSystemWords.objects.all()

from WordInit import *

class GameApi(object):
    @staticmethod
    @csrf_exempt
    def openGameHome(request):
        HsWriteLog('=====================================>> openGameHome')
        renterDict = GameApi.loginGame('aaaa')
        return render(request, 'game/game_home.html', renterDict)

    @staticmethod
    @csrf_exempt
    def settingGame(request):
        renterDict = {}

        # 返回课标
        kbList = HsGameKBiao.objects.filter(state=1).order_by('code')
        kbArray = []
        for one in kbList:
            oneKb = {}
            oneKb['code'] = int(one.code)
            oneKb['name'] = one.name
            kbArray.append(oneKb)

        renterDict['KBDatas'] = kbArray

        # 返回学历数据
        xlList = HsGameLevel.objects.filter(state=1)
        xlArray = []
        for one in xlList:
            oneXl = {}
            oneXl['code'] = one.code
            oneXl['name'] = one.name
            xlArray.append(oneXl)
        renterDict['XLDatas'] = xlArray

        # 返回年级
        xnList = HsGameGrade.objects.filter(state=1).order_by('code')
        xnArray = []
        for one in xnList:
            oneXn = {}
            oneXn['code'] = one.code
            oneXn['name'] = one.name
            xnArray.append(oneXn)
        renterDict['XNDatas'] = xnArray

        return render(request, 'game/game_setting.html', renterDict)

    @staticmethod
    @csrf_exempt
    def openErrorBook(request):
        renterDict = {}
        return render(request, 'game/game_error_book.html', renterDict)

    @staticmethod
    @csrf_exempt
    def openGameMap(request):
        renterDict = {}
        try:
            openid = request.GET.get("openid")
        except Exception, e:
            renterDict['units'] = []
            renterDict['havecfg'] = 0
            return render(request, 'game/game_map.html', renterDict)

        # 查询客户配置
        customConfig = HsCustomGameSetting.objects.filter(ccode=openid).first()
        if not customConfig:
            renterDict['units'] = []
            renterDict['havecfg'] = 0
            return render(request, 'game/game_map.html', renterDict)

        kbcode = customConfig.kbcode
        lcode = customConfig.lcode
        gcode = customConfig.gcode
        state= customConfig.state
        # 查询单元列表
        unitLists = HsGameUnit.objects.filter(kbcode=kbcode,lcode=lcode,gcode=gcode,state=state).order_by('index')

        unitRtnList=[]
        for oneUnit in unitLists:
            renterDict={}

            if len(oneUnit.name) < 8:
                renterDict['name'] = oneUnit.name
            else:
                renterDict['name'] = oneUnit.name[:30] + " ... ..."
            renterDict['code'] = oneUnit.code
            unitRtnList.append(renterDict)
            # unitRtnList.append(renterDict)

        renterDict['units'] = unitRtnList
        renterDict['havecfg'] = 1
        return render(request, 'game/game_map.html', renterDict)

    @staticmethod
    @csrf_exempt
    def startGame(request):
        renterDict = {}
        try:
            unitcode = request.GET.get("unitcode")
        except Exception, e:
            loginResut = json.dumps({"ErrorInfo": "参数错误", "ErrorId": 20001, "Result": {}})
            return HttpResponse(loginResut)

        renterDict['unitcode'] = unitcode
        return render(request, 'game/gamming.html', renterDict)

    @staticmethod
    @csrf_exempt
    def viewErrorWord(request):
        try:
            wcode = request.GET.get("wcode")
            openid = request.GET.get("openid")
        except Exception, e:
            return HttpResponse("参数错误")

        renterDict = GameApi.getWordInfo(wcode, openid)
        return render(request, 'game/game_view_word.html', renterDict)

    @staticmethod
    @csrf_exempt
    def gameResult(request):
        try:
            unitcode = request.GET.get("unitcode")
            openid = request.GET.get("openid")
        except Exception, e:
            return HttpResponse("参数错误")

        # 查询单元单词列表
        unitWords = HsGameUnitWords.objects.filter(code=unitcode)

        # 查询错误列表
        wcodeList = []
        for oneWord in unitWords:
            wcodeList.append(oneWord.wcode)

        conditionOrFilter = GameApi.buildQueryErrorCondition(wcodeList)
        systemWords = None
        if conditionOrFilter:
            dynamicBuildString = "HsGameErrorBook.objects.filter(%s,code=openid)" % conditionOrFilter
            systemWords = eval(dynamicBuildString)

        # 计算正确数量
        finishDict = []
        rightDict = []
        for oneWord in unitWords:
            errorKey = None
            if oneWord.wcode in finishDict:
                continue
            for oneErr in systemWords:
                if oneWord.wcode == oneErr.wcode:
                    errorKey = oneErr.wcode
                    break
            if not errorKey:
                oneRecord = {}
                oneRecord['word'] = oneWord.wcode
                oneRecord['mykey'] = oneWord.wcode
                rightDict.append(oneRecord)
                finishDict.append(oneWord.wcode)

        # 计算未作答数量
        noKeyDict = []
        for oneWord in unitWords:
            errorKey = None
            if oneWord.wcode in finishDict:
                continue
            for oneErr in systemWords:
                if (oneWord.wcode == oneErr.wcode) and (not oneErr.mykey or len(oneErr.mykey) == 0):
                    errorKey = oneErr.wcode
                    break
            if errorKey:
                oneRecord = {}
                oneRecord['word'] = oneWord.wcode
                oneRecord['mykey'] = ""
                noKeyDict.append(oneRecord)
                finishDict.append(oneWord.wcode)

        # 计算错误数量
        errorKeyDict = []
        for oneWord in unitWords:
            errorKey = None
            if oneWord.wcode in finishDict:
                continue
            for oneErr in systemWords:
                if (oneWord.wcode == oneErr.wcode) and (oneErr.mykey and len(oneErr.mykey) > 0):
                    errorKey = oneErr.mykey
                    break
            if errorKey:
                oneRecord = {}
                oneRecord['word'] = oneWord.wcode
                oneRecord['mykey'] = errorKey
                errorKeyDict.append(oneRecord)
                finishDict.append(oneWord.wcode)

        resultDict= {}
        resultDict["right"] = rightDict
        resultDict["noanswer"] = noKeyDict
        resultDict["error"] = errorKeyDict

        loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": resultDict})
        return HttpResponse(loginResut)



    @staticmethod
    @csrf_exempt
    def updateRecord(request):
        '''
        更新游戏记录
        :param request:
        :return:
        '''
        postDataList = {}
        postDataList = getPostData(request)

        ccode = postDataList["ccode"]
        unitcode = postDataList['unitcode']
        scores = int(postDataList['score'])

        # 非单元监测，则直接返回，不做数据更新
        if not unitcode or len(unitcode) == 0:
            loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": None})
            return HttpResponse(loginResut)

        existHandle = HsGameResult.objects.filter(ccode=ccode,ucode=unitcode).first()
        if not existHandle:
            loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": None})
            return HttpResponse(loginResut)

        existHandle.score = scores

        existHandle.gametime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        try:
            existHandle.save()
        except Exception ,ex:
            pass


        rtnDictGlobal = {}
        loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    @csrf_exempt
    def newGameRecord(request):
        '''
        新建游戏记录
        :param request:
        :return:
        '''
        postDataList = {}
        postDataList = getPostData(request)

        ccode = postDataList["ccode"]
        unitcode = postDataList['unitcode']
        scores = int(postDataList['score'])

        # 非单元监测，则直接返回，不做数据更新
        existHandle = HsGameResult.objects.filter(ccode=ccode,ucode=unitcode).first()
        if not existHandle:
            existHandle = HsGameResult()

        existHandle.ccode = ccode
        existHandle.ucode = unitcode
        existHandle.score = scores
        existHandle.gametime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        try:
            existHandle.save()
        except Exception ,ex:
            pass

        rtnDictGlobal = {}
        loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)


    @staticmethod
    @csrf_exempt
    def Write_Error_Book(request):
        '''
        刷新错题本
        :param request:
        :return:
        '''
        postDataList = {}
        postDataList = getPostData(request)
        mykey = postDataList['error']
        wcode = postDataList['right']
        code = postDataList['openid']

        # 查询错题记录
        errorhandle = HsGameErrorBook.objects.filter(code=code,wcode=wcode).first()

        if mykey == wcode:
            if errorhandle:
                try:
                    errorhandle.delete()
                except:
                    pass
            else:
                pass

        else:
            if not errorhandle:
                errorhandle = HsGameErrorBook()

            errorhandle.mykey = mykey
            errorhandle.wcode = wcode
            errorhandle.code = code

            try:
                errorhandle.save()
            except:
                pass


        rtnDictGlobal = {}
        loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    @csrf_exempt
    def deleteErrorBookWord(request):
        '''
        刷新错题本
        :param request:
        :return:
        '''
        wcode = request.GET.get('wcode')
        code = request.GET.get('code')

        # 查询错题记录
        errorhandle = HsGameErrorBook.objects.filter(code=code,wcode=wcode).first()

        if not errorhandle:
            loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": None})
            return HttpResponse(loginResut)

        try:
            errorhandle.delete()
        except:
            pass


        rtnDictGlobal = {}
        loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    @csrf_exempt
    def queryErrorBook(request):
        '''
        查询错题本
        :param request:
        :return:
        '''
        code = request.GET.get('code')
        pageIndex = int(request.GET.get('pageindex'))
        pageSize = int(request.GET.get('pagesize'))

        # 查询错题记录
        errorWords = HsGameErrorBook.objects.all().order_by('wcode')

        rtnDictGlobal = {}
        datas = []
        for index,oneWord in enumerate(errorWords):
            if index < pageIndex*pageSize:
                continue

            if index >= (pageIndex + 1)* pageSize:
                break

            oneRecord ={}

            oneRecord["mykey"] = oneWord.mykey
            oneRecord["wcode"] = oneWord.wcode
            datas.append(oneRecord)

        rtnDictGlobal["Datas"] = datas

        loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": rtnDictGlobal})
        return HttpResponse(loginResut)

    @staticmethod
    @csrf_exempt
    def updateCustomSetting(request):
        '''
        存储用户的 设置数据
        :param request:
        :return:
        '''
        code = request.GET.get('code')
        kbcode = request.GET.get('kbcode')
        lcode = request.GET.get('lcode')
        gcode = request.GET.get('gcode')
        state = request.GET.get('state')

        # 查询错题记录
        mysetting = HsCustomGameSetting.objects.filter(ccode = code)

        if not mysetting:
            mysetting = HsCustomGameSetting()

        mysetting.ccode = code
        mysetting.kbcode = kbcode
        mysetting.lcode = lcode
        mysetting.gcode = gcode

        mysetting.state = state
        try:
            mysetting.save()
        except Exception ,ex:
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 20001, "Result": None})
            return HttpResponse(loginResut)


        rtnDictGlobal = {}
        loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)

    @staticmethod
    @csrf_exempt
    def loadCustomSetting(request):
        '''
        加载用户的 设置数据
        :param request:
        :return:
        '''
        code = request.GET.get('code')

        rtnDictGlobal = GameApi.getSetting(code)


        loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": rtnDictGlobal})
        return HttpResponse(loginResut)

    @staticmethod
    def getSetting(code):
        # 查询错题记录
        mysetting = HsCustomGameSetting.objects.filter(ccode=code)

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
    @csrf_exempt
    def loginGame(code):
        '''
        存储用户的 设置数据
        :param request:
        :return:
        '''
        # code = request.GET.get('code')
        HsWriteLog('============>>loginGame!')
        rtnDict={}
        setting = GameApi.getSetting(code)
        rtnDict["setting"] = setting

        overdate = 0
        currentdate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        # 判断账户是否需要重置
        customInfo = HsGameCustom.objects.filter(code = code).first()
        if not customInfo:
            customInfo = HsGameCustom()
            customInfo.code = code
            customInfo.sevstart = currentdate
            now = datetime.datetime.now()
            delta = datetime.timedelta(days=3)
            n_days = now + delta
            customInfo.sevstop =n_days.strftime('%Y-%m-%d')
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
        return  rtnDict
        # loginResut = json.dumps({"ErrorInfo": "Success", "ErrorId": 200, "Result": rtnDict})
        # return HttpResponse(loginResut)


    # =======================api invoke
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
        if command == "Save_Setting".upper():
            return GameApi.Save_Setting(request)
        elif command == "Open_Error_Book".upper():
            return GameApi.Open_Error_Book(request)
        elif command == "Get_Word_Info".upper():
            return GameApi.Get_Word_Info(request)
        elif command == "Get_Unit_Code".upper():
            return GameApi.Get_Unit_Code(request)
        elif command == "Write_Error_Book".upper():
            return  GameApi.Write_Error_Book(request)
        elif command == "Get_Result".upper():
            return  GameApi.gameResult(request)
        elif command == "Share_Success".upper():
            return  GameApi.Share_Success(request)

    @staticmethod
    def Get_Result(request):
        try:
            unitcode = request.GET.get("unitcode")
            # openid = request.GET.get("openid")
        except Exception, e:
            return HttpResponse("参数错误")

        rtnDict ={}
        rtnDict['unitcode'] = unitcode

        return render(request, 'game/game_result.html', rtnDict)
    @staticmethod
    def getWordInfo(wcode,openid,offset=0):
        # global globalWords
        errorWords = HsGameErrorBook.objects.filter(code=openid).order_by('wcode')

        wcodeList = []
        for one in errorWords:
            wcodeList.append(one.wcode)
        systemWordList = GameApi.getSystemWords(wcodeList)
        oneWordDict ={}
        for index,oneWord in enumerate(errorWords):
            if oneWord.wcode != wcode:
                continue

            rtnWord = None
            selIndex = -1
            if offset == 0:
                rtnWord = oneWord
                selIndex = index
            elif offset == 1 and len(errorWords) > index + 1:
                rtnWord = errorWords[index + 1]
                selIndex = index + 1
            elif offset == -1 and index > 0:
                rtnWord = errorWords[index - 1]
                selIndex = index - 1

            if rtnWord:
                oneWordDict['wcode'] = rtnWord.wcode
                systemWords = None
                for one in systemWordList:
                    if one.words == rtnWord.wcode:
                        systemWords = one
                        break

                if not systemWords:
                    checkNetMeaning = WordInit.initProunceNet(oneWord.wcode)
                    if not checkNetMeaning:
                        oneWordDict['meaning'] = '未知单词'
                        oneWordDict['sentence'] = ""
                        oneWordDict['pron'] = ""
                    else:
                        oneWordDict['meaning'] = checkNetMeaning.meaning
                        oneWordDict['sentence'] = checkNetMeaning.lx.replace("/r/n", "<br>")
                        oneWordDict['pron'] = checkNetMeaning.pron
                else:
                    oneWordDict['meaning'] = systemWords.meaning
                    oneWordDict['sentence'] = systemWords.lx.replace("/r/n", "<br>")
                    oneWordDict['pron'] = systemWords.pron

                oneWordDict['mykey'] = rtnWord.mykey

                oneWordDict['haveNext'] = len(errorWords) - selIndex - 2
                oneWordDict['havePre'] = selIndex - 1

            break

        return  oneWordDict

    # http://fanyi.youdao.com/openapi.do?keyfrom=android&key=group&type=data&doctype=json&version=1.2&q=group
    # http://dict-co.iciba.com/api/dictionary.php?w=group&key=key
    @staticmethod
    def Get_Word_Info(request):
        try:
            wcode = request.GET.get("wcode")
            openid = request.GET.get("openid")
            offset = int(request.GET.get("offset"))
        except Exception, e:
            # print u"获取code和stat参数错误"
            return HttpResponse("参数错误")

        oneWordDict = GameApi.getWordInfo(wcode,openid,offset)

        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": oneWordDict})
        return HttpResponse(loginResut)

    @staticmethod
    def Open_Error_Book(request):
        # global globalWords
        try:
            openid = request.GET.get("openid")
            HsWriteLog('openid=========================================!' + openid)
            pageindex = int(request.GET.get("pageindex"))
            pagesize = int(request.GET.get("pagesize"))
        except Exception, e:
            # print u"获取code和stat参数错误"
            return HttpResponse("参数错误")

        gameSetting = HsGameErrorBook.objects.filter(code=openid).order_by('wcode')

        wcodeList = []
        for one in gameSetting:
            wcodeList.append(one.wcode)
        systemWordList = GameApi.getSystemWords(wcodeList)

        HsWriteLog(" systemWordList type is = %s" % type(systemWordList))

        rtnList = []
        for index,oneWord in enumerate(gameSetting):
            if index < pageindex*pagesize:
                continue
            if index >= (pageindex + 1) * pagesize:
                break

            oneWordDict = {}
            oneWordDict['wcode'] = oneWord.wcode
            systemWords = None
            for one in systemWordList:
                if one.words == oneWord.wcode:
                    systemWords = one
                    break

            if not systemWords:
                checkNetMeaning = WordInit.initProunceNet(oneWord.wcode)
                if not checkNetMeaning:
                    oneWordDict['meaning'] = '未知单词'
                else:
                    srcmeaning = checkNetMeaning.meaning
                    srcmeaning = srcmeaning.replace('<br>', "&nbsp")
                    srcmeaning = srcmeaning.replace('<br />', "&nbsp")

                    oneWordDict['meaning'] = srcmeaning[:10] + "..."
            else:
                srcmeaning = systemWords.meaning
                srcmeaning = srcmeaning.replace('<br>' ,"&nbsp")
                srcmeaning = srcmeaning.replace('<br />', "&nbsp")
                oneWordDict['meaning'] = srcmeaning[:10] + "..."

            oneWordDict['mykey'] = oneWord.mykey
            rtnList.append(oneWordDict)

        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": rtnList})
        return HttpResponse(loginResut)


    @staticmethod
    def Save_Setting(request):
        postDataList = {}
        postDataList = getPostData(request)

        openid = postDataList["openid".lower()]
        kbindex = int(postDataList["kbindex".lower()])
        xlindex = int(postDataList["xlindex".lower()])
        xnindex = int(postDataList["xnindex".lower()])
        xqindex = int(postDataList["xqindex".lower()])

        HsWriteLog('openid=========================================!%s'%openid)
        HsWriteLog('kbindex=========================================!%d' % kbindex)
        HsWriteLog('xlindex=========================================!%d' % xlindex)
        HsWriteLog('xnindex=========================================!%d' % xnindex)
        HsWriteLog('xqindex=========================================!%d' % xqindex)


        gameSetting = HsCustomGameSetting.objects.filter(ccode=openid).first()
        if not gameSetting:
            gameSetting = HsCustomGameSetting()

        gameSetting.ccode = openid
        gameSetting.kbcode = kbindex
        gameSetting.lcode = xlindex
        gameSetting.gcode = xnindex
        gameSetting.state = xqindex


        commitDataList = []
        commitDataList.append(CommitData(gameSetting, 0))

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
    def Get_Unit_Code(request):
        HsWriteLog('Get_Unit_Code1=========================================!')
        try:
            unitcode = request.GET.get("unitcode")
            HsWriteLog('unitcode=========================================!%s'%unitcode)
            openid = request.GET.get("openid")
        except Exception, e:
            HsWriteLog('Get_Unit_Code2=========================================!%s'%e.message.decode('utf-8'))
            return HttpResponse("参数错误")
        HsWriteLog('Get_Unit_Code3=========================================!')

        if unitcode == "9999":
            unitWords = HsGameErrorBook.objects.filter(code=openid)
        else:
            unitWords = HsGameUnitWords.objects.filter(code=unitcode)

        wordArray = []
        for oneWord in unitWords:
            wordArray.append(oneWord.wcode)

        HsWriteLog('wordArray.size=========================================!%d'%len(wordArray))
        rtndict = GameApi.getWordDetailInfo(wordArray)
        HsWriteLog('rtndict.value=========================================!%s' % str(rtndict))

        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": rtndict})
        return HttpResponse(loginResut)

    @staticmethod
    def buildQueryErrorCondition(wcodelist):
        rntCondition = None
        for oneWord in wcodelist:
            if rntCondition:
                rntCondition =rntCondition +  "|Q(wcode='%s')"%oneWord
            else:
                rntCondition = "Q(wcode='%s')"%oneWord

        return  rntCondition

    @staticmethod
    def buildOrCondition(wcodelist):
        rntCondition = None
        for oneWord in wcodelist:
            if rntCondition:
                rntCondition =rntCondition +  "|Q(words='%s')"%oneWord
            else:
                rntCondition = "Q(words='%s')"%oneWord

        return  rntCondition

    @staticmethod
    def getSystemWords(wcodeList):
        conditionOrFilter = GameApi.buildOrCondition(wcodeList)

        HsWriteLog(conditionOrFilter)
        if not conditionOrFilter:
            return  []
        dynamicBuildString = "HsGameSystemWords.objects.filter(%s)" % conditionOrFilter
        # eval(dynamicBuildString)
        systemWords = eval(dynamicBuildString)
        return systemWords

    @staticmethod
    def getWordDetailInfo(wcodeList):
        rtnWordDict = {}
        rtnList = []
        conditionOrFilter = GameApi.buildOrCondition(wcodeList)

        if not conditionOrFilter:
            return  rtnWordDict
        dynamicBuildString = "HsGameSystemWords.objects.filter(%s)" % conditionOrFilter
        # eval(dynamicBuildString)
        systemWords = eval(dynamicBuildString)

        for oneword in wcodeList:
            haveRecord = False
            oneWordDict = {}
            oneWordDict['wcode'] = oneword
            for wordHandle in systemWords:
                if wordHandle.words != oneword:
                    continue

                if wordHandle:
                    haveRecord = True
                    if not systemWords:
                        checkNetMeaning = WordInit.initProunceNet(oneword)
                        if not checkNetMeaning:
                            oneWordDict['meaning'] = '未知单词'
                            oneWordDict['sentence'] = ""
                            oneWordDict['pron'] = ""
                        else:
                            oneWordDict['meaning'] = checkNetMeaning.meaning
                            oneWordDict['sentence'] = checkNetMeaning.lx.replace("/r/n", "<br>")
                            oneWordDict['pron'] = checkNetMeaning.pron
                    else:
                        oneWordDict['meaning'] = wordHandle.meaning
                        oneWordDict['sentence'] = wordHandle.lx.replace("/r/n", "<br>")
                        oneWordDict['pron'] = wordHandle.pron

                    break
            if not haveRecord:
                oneWordDict['meaning'] = '未知单词'
                oneWordDict['sentence'] = ""
                oneWordDict['pron'] = ""

            rtnList.append(oneWordDict)
        rtnWordDict['unitwords'] = rtnList

        return  rtnWordDict

    @staticmethod
    def Share_Success(request):
        # HsWriteLog('Share_Success!')
        postDataList = {}
        postDataList = getPostData(request)
        # HsWriteLog('Share_Success1!')
        openid = postDataList["openid".lower()]
        # HsWriteLog('Share_Success2!')
        gameSetting = HsCustomGameShareCount.objects.filter(ccode=openid).first()
        # HsWriteLog('Share_Success3!')
        if not gameSetting:
            # HsWriteLog('Share_Successa!')
            gameSetting = HsCustomGameShareCount()
            gameSetting.sharecount = 0

        else:#判断当前分享日期是否已经分享过
            if gameSetting.sharedate == time.strftime('%Y-%m-%d',time.localtime(time.time())):
                loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
                return HttpResponse(loginResut)
            else:
                pass


            # HsWriteLog('Share_Successb!')
        # HsWriteLog('Share_Success4!')
        gameSetting.ccode = openid
        gameSetting.sharecount = gameSetting.sharecount + 1
        gameSetting.sharedate = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        commitDataList = []
        commitDataList.append(CommitData(gameSetting, 0))
        # HsWriteLog('Share_Success5!')
        # 事务提交
        try:
            result = commitCustomDataByTranslate(commitDataList)

            if not result:
                HsWriteLog('Share_Success6!')
                loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
                return HttpResponse(loginResut)
        except Exception, ex:
            print ex
            HsWriteLog('Share_Success7!')
            loginResut = json.dumps({"ErrorInfo": "数据库操作失败", "ErrorId": 99999, "Result": None})
            return HttpResponse(loginResut)
        HsWriteLog('save_sccueess!')
        loginResut = json.dumps({"ErrorInfo": "操作成功", "ErrorId": 200, "Result": None})
        return HttpResponse(loginResut)
