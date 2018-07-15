#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *

class WebCenterApi(object):
    @staticmethod
    @csrf_exempt
    def openHome(request):
        renterDict = {}
        return render(request, 'index.html',renterDict )

    @staticmethod
    @csrf_exempt
    def openAbout(request):
        renterDict = {}
        return render(request, 'about.html',renterDict )

    @staticmethod
    @csrf_exempt
    def openContect(request):
        renterDict = {}
        return render(request, 'contect.html',renterDict )

    @staticmethod
    @csrf_exempt
    def openHr(request):
        renterDict = {}
        return render(request, 'hr.html',renterDict )


    @staticmethod
    @csrf_exempt
    def openNews(request):
        renterDict = {}
        return render(request, 'news.html',renterDict )


    @staticmethod
    @csrf_exempt
    def openProduct(request):
        renterDict = {}
        return render(request, 'product.html',renterDict )


    @staticmethod
    @csrf_exempt
    def openService(request):
        renterDict = {}
        return render(request, 'service.html',renterDict )


    @staticmethod
    @csrf_exempt
    def openFooter(request):
        renterDict = {}
        return render(request, 'footer.html',renterDict )

    # ###############################################################################################################
    @staticmethod
    @csrf_exempt
    def openNews102645(request):
        renterDict = {}
        return render(request, 'newsDetail_102645.html',renterDict )

    @staticmethod
    @csrf_exempt
    def openNews102648(request):
        renterDict = {}
        return render(request, 'newsDetail_102648.html',renterDict )

    @staticmethod
    @csrf_exempt
    def openNews102651(request):
        renterDict = {}
        return render(request, 'newsDetail_102651.html', renterDict)

    @staticmethod
    @csrf_exempt
    def openNews102653(request):
        renterDict = {}
        return render(request, 'newsDetail_102653.html', renterDict)

    @staticmethod
    @csrf_exempt
    def openNews102656(request):
        renterDict = {}
        return render(request, 'newsDetail_102656.html', renterDict)

    @staticmethod
    @csrf_exempt
    def openNews102659(request):
        renterDict = {}
        return render(request, 'newsDetail_102659.html', renterDict)

    @staticmethod
    @csrf_exempt
    def openNews102662(request):
        renterDict = {}
        return render(request, 'newsDetail_102662.html', renterDict)
