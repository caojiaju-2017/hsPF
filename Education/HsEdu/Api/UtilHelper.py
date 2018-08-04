#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid,os
# import Image
class UtilHelper(object):
    @staticmethod
    def newUuid():
        '''
        新建UUID
        :return:
        '''
        return  uuid.uuid1().__str__().replace("-", "")
    @staticmethod
    def GetFileNameAndExt(filename):
        (filepath, tempfilename) = os.path.split(filename);
        (shotname, extension) = os.path.splitext(tempfilename);
        return shotname, extension
    @staticmethod
    def getGetParams(request):
        getParams = {}
        for oneParam in request.GET:
            # print "paramname=%s,paramvalue=%s"%(oneParam,request.GET.get(oneParam))
            getParams[oneParam.lower()] = request.GET.get(oneParam)
        return getParams
    @staticmethod
    def getPostParams(request):
        '''
        获取请求post参数
        :return:
        '''
        postDataList = {}
        if request.method == 'POST':
            for key in request.POST:
                try:
                    postDataList[key.lower()] = request.POST.getlist(key)[0]
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

    @staticmethod
    def getCommand(request):
        try:
            command = request.GET.get('command').upper()
            return command
        except:
            return None

    @staticmethod
    def getOrgCode(request):
        try:
            getParams = UtilHelper.getGetParams(request)
            if getParams.has_key("orgsign"):
                return getParams['orgsign']

            postParams = UtilHelper.getPostParams(request)
            if postParams.has_key("orgsign"):
                return postParams['orgsign']
        except:
            postParams = UtilHelper.getPostParams(request)
            if postParams.has_key("orgsign"):
                return postParams['orgsign']
            return None


    @staticmethod
    def getUserCode(request):
        try:
            ucode = request.GET.get('logincode').upper()
            return ucode
        except:
            return None

    @staticmethod
    def getMd5(stringValue):
        import md5
        m1 = md5.new()

        try:
            m1.update(stringValue.encode(encoding='utf-8'))
        except:
            m1.update(stringValue)
        return m1.hexdigest()

    @staticmethod
    def make_thumb(path, thumb_file, size):
        """生成缩略图"""
        img = Image.open(path)
        width, height = img.size
        # 裁剪图片成正方形
        if width > height:
            delta = (width - height) / 2
            box = (delta, 0, width - delta, height)
            region = img.crop(box)
        elif height > width:
            delta = (height - width) / 2
            box = (0, delta, width, height - delta)
            region = img.crop(box)
        else:
            region = img

            # 缩放
        thumb = region.resize((size, size), Image.ANTIALIAS)

        base, ext = os.path.splitext(os.path.basename(path))
        # filename = os.path.join(thumb_path, '%s_thumb.jpg' % (base,))
        # print filename
        # 保存
        thumb.save(thumb_file, quality=70)
if __name__ == "__main__":
    print UtilHelper.getMd5("command=TERMINAL_LOGINmac=02-00-00-00-00-00myip=192.168.1.108orgsign=00049e403acd11e888eb989096c1d888regcode=terminal=b068455c3edf40c9b4220cf95f38f169timestamp=1523260423450version=AndroidV1.0.0g^4)=h@ir_n!azd^wh8*+p6*y1#uvsjd%d4lzyv_egwyj^$hi_")