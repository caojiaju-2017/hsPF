#!/usr/bin/env python
# -*- coding: utf-8 -*-

from include import *

class Api(object):
    @staticmethod
    @csrf_exempt
    def openHome(request):
        return render(request, 'three/1.html', {})