#!/usr/bin/python
# -*- coding:utf-8 -*-
import socket
import  subprocess
import  re
import  psutil
import uuid
import pythoncom
import wmi
__all__ = ['MonitorHelper']

class MonitorHelper(object):

    @staticmethod
    def getHostCpuUseage():
        '''
        获取本机CPU
        :return:
        '''
        # print ("getHostCpuUseage")
        return str(int(psutil.cpu_percent(1)))

    @staticmethod
    def getHostDiskUseage():
        '''
        获取磁盘总使用比例
        :return:
        '''
        # print("getHostDiskUseage")
        pythoncom.CoInitialize()
        c = wmi.WMI()

        # 获取硬盘使用百分情况
        total = 0
        freeSpace = 0
        for disk in c.Win32_LogicalDisk(DriveType=3):
            total = total + int(disk.Size)
            freeSpace = freeSpace + int(disk.FreeSpace)

        if total == 0:
            return "0"

        return str(int(100.0 * (total - freeSpace) / total))

    @staticmethod
    def getHostMemoryUseage():
        phymem = psutil.virtual_memory()
        return  str(int(round(phymem.percent)))

if __name__ == "__main__":
    help(MonitorHelper)
    print (MonitorHelper.getHostCpuUseage())
    print(MonitorHelper.getHostDiskUseage())
    print(MonitorHelper.getHostMemoryUseage())