#!/usr/bin/env python
# -*- coding: utf-8 -*-
from include import *

class ResourceApi(object):
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