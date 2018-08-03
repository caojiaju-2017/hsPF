#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2,urllib
from bs4 import  BeautifulSoup
import time,random
from multiprocessing import Pool

from include import *
accounts=[]
accounts.append(['60638690',  'youdao111'])
accounts.append(['969918857',  'neverland'])
accounts.append(['993123434',  'pdblog'])
accounts.append(['702271149',  'HTTP-TESTdddaa'])
accounts.append(['1661829537',  'youdianbao'])
accounts.append(['1207861310',  'abc1243'])
accounts.append(['1068666577',  'dsfesdfesdff'])
accounts.append(['1612199890',  'morninglight'])
accounts.append(['1490852988',  'xujiangtao'])
accounts.append(['1102266192',  'OSMeteor'])

ip = []
attr1 = 'body > div:nth-of-type(3) > span:nth-of-type(2)'  # 发音
attr2 = 'body > div:nth-of-type(4)'  # 释义
attr3 = '#listtrans > ul'  # 举例
urlTmp = 'http://dict.youdao.com/m/search?keyfrom=dict.mindex&q=%s'

def f(x):
    time.sleep(10)
    return x*x

def testAttribute(absoluteUrl,tagAttrs):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    send_headers = {
        # 'Host': 'http://www.youdao.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'X-Forwarded-For': ip[random.randint(0, 9998)]
    }

    req = urllib2.Request(absoluteUrl, data=None, headers=send_headers, origin_req_host=None, unverifiable=True)

    try:
        html_doc = urllib2.urlopen(req, timeout=60).read()
    except Exception, ex:
        print 'url failed!'
        return  None

    # print html_doc

    soup = BeautifulSoup(html_doc, 'lxml')

    resultList = []
    for oneTag in tagAttrs:
        # print "=======================%s======================="%oneTag
        try:
            datas = soup.select(oneTag)
            values = str(datas[0])
            values = values.replace("<span>","")
            values = values.replace("</span>", "")
            values = values.replace('<div class="content">','')
            values = values.replace('</div>', '')
            values = values.replace('\n', '')

            if oneTag == "#listtrans > ul":
                values = values.replace('  ', ' ')
            else:
                values = values.replace(' ', '')
            values = values.replace('\t', ' ')
            values = values.replace('<ul><li>', '')
            values = values.replace('</li><li>', '<br/>')
            values = values.replace('</li></ul>', '')
            # print values
            resultList.append(values)
        except Exception,ex:
            resultList.append("")
            pass

    return resultList
        # print "=======================%s--end=======================" % oneTag
# http://dict.youdao.com/m/search?keyfrom=dict.mindex&q=word
# "http://fanyi.youdao.com/openapi.do?keyfrom=youdao111&key=60638690&type=data&doctype=xml&version=1.1&q="+ word);
class WordInit(object):
    @staticmethod
    def initProunceNet(word):
        print len(word)
        for index in range(10000):
            ip.append("%d.%d.%d.%d" % (
                random.randint(2, 254), random.randint(2, 254), random.randint(2, 254), random.randint(2, 254)))

        if not word or len(word) <= 0:
            return None

        results = testAttribute(urlTmp % word, [attr1, attr2, attr3])

        if not results or len(results) <= 2:
            print 'error =======> ', word
            return None

        newWord = HsGameSystemWords()
        newWord.words = word
        newWord.pron = results[0]
        newWord.meaning = results[1]
        newWord.lx = results[2]

        try:
            newWord.save()
            # return newWord
        except Exception, ex:
            print ex.message

        return HsGameSystemWords.objects.filter(words=word).first()
    @staticmethod
    @csrf_exempt
    def initProunce(request):
        words = HsGameSystemWords.objects.all()
        prous = HsGameUnitWords.objects.all()
        for index in range(10000):
            ip.append("%d.%d.%d.%d" % (
                random.randint(2, 254), random.randint(2, 254), random.randint(2, 254), random.randint(2, 254)))
        currentDetailCount = 0
        for oneProus in prous:
            if WordInit.checkExist(words, oneProus.wcode):
                continue

            print "deal word = " + oneProus.wcode
            WordInit.initProunceNet(oneProus.wcode)
        return HttpResponse("Ok")

    @staticmethod
    @csrf_exempt
    def initProunce2(request):
        words = HsGameSystemWordsCopy.objects.all()
        prous = HsTempT.objects.all()

        currentDetailCount = 0
        for keyIndex in range(len(accounts)):
            print 'keyIndex====%d'%keyIndex
            # keyIndex = 0
            # try:
            #     keyIndex = int(request.GET.get("keyIndex"))
            # except Exception, e:
            #     keyIndex = 0
            for oneProus in prous:
                if not oneProus.words or len(oneProus.words) <= 0:
                    continue
                if WordInit.checkExist(words, oneProus.words):
                    continue

                # oneProus.words = oneProus.words.strip()
                means, pron, uspron, ukpron = WordInit.init(oneProus.words, keyIndex)

                if means == -1:
                    break

                # if not pron:
                #     continue

                currentDetailCount = currentDetailCount + 1
                newWord = HsGameSystemWordsCopy()
                newWord.words = oneProus.words
                newWord.meaning = means
                newWord.pron = pron
                newWord.uspron = uspron
                newWord.ukpron = ukpron
                try:
                    newWord.save()
                except Exception, ex:
                    print ex.message

                    # print "wait next loop"
                    # time.sleep(10*60)

        return HttpResponse("Ok ,Have deal count =  %d"%(currentDetailCount))


    @staticmethod
    def init(word,index = 0):
        global accounts
        key = accounts[index][0]
        keyfrom = accounts[index][1]

        # 60638690  youdao111
        # keyfrom = neverland & key = 969918857
        # key = '993123434'  keyfrom = 'pdblog'  # 有道keyfrom
        # 702271149   HTTP-TESTdddaa
        url= "http://fanyi.youdao.com/openapi.do?keyfrom=%s&key=%s&type=data&doctype=json&version=1.1&q=%s"%(keyfrom,key,word)
        try:
            res = requests.get(url).json()
        except Exception,ex:
            print url
            if 'Expecting value' in ex.message:
                return -1, None, None, None
            return None, None, None, None
        #{"translation":["集团"],"basic":{"us-phonetic":"ɡrup","phonetic":"gruːp","uk-phonetic":"gruːp","explains":["n. 组；团体","adj. 群的；团体的","vt. 把\u2026聚集；把\u2026分组","vi. 聚合"]},"query":"group","errorCode":0,"web":[{"value":["群","群组","族 (化学)"],"key":"group"},{"value":["维珍集团","维京集团","维珍团体"],"key":"Virgin Group"},{"value":["麦格理集团","麦格理银行","麦格理银行"],"key":"Macquarie Group"}]}

        if not res.has_key('basic'):
            return None,None,None,None
        else:
            # 含义
            meanings = None
            meaningList = res["basic"]["explains"]
            for one in meaningList:
                if not meanings:
                    meanings = one
                else:
                    meanings = meanings + "<br>" + one
            # print "meaning===>" + meanings

            # 发音
            pron = None
            us = None
            uk = None
            if res["basic"].has_key("phonetic"):
                pron = res["basic"]["phonetic"]

            if res["basic"].has_key("us-phonetic"):
                us = res["basic"]["us-phonetic"]

            if res["basic"].has_key("uk-phonetic"):
                uk = res["basic"]["uk-phonetic"]

            if not pron:
                if uk:
                    pron = uk
                else:
                    pron = us
            return meanings,pron ,us,uk

    @staticmethod
    def checkExist(words,word):
        for one in words:
            if one.words == word:
                # print 'skip====' + word
                return True

        return False