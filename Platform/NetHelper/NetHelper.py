#!/usr/bin/python
# -*- coding:utf-8 -*-
import socket
import  subprocess
import  re
import  psutil
import uuid
import pythoncom
import wmi

__all__ = ['NetHelper']
class NetHelper(object):
    def __init__(self):
        pass

    @staticmethod
    def getBroacastAddree():
        '''
        获取IP以及子网掩码,windows 下的命令是ipconfig,LINUX下是ifconfig,倘若再不行，我们直接用python获取ip
        :return:
        '''
        try:
            try:
                sys_cmd = subprocess.Popen('ipconfig', stdout=subprocess.PIPE)
            except:
                sys_cmd = subprocess.Popen('ifconfig', stdout=subprocess.PIPE)
        except:  #####如果用ipconfig命令无法获取到机器的ip,使用python的socket模块获取
            ip_add = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            index_ = ip_add.rfind(".")
            return [ip_add[:index_] + ".255"]
        cmd_res = sys_cmd.stdout.read()
        pattern = re.compile(r'((\d+\.){3}\d+\s)')  #########正则匹配
        ip_list = pattern.findall(cmd_res)
        ip_add = []
        for i in ip_list:
            if int(i[0].rstrip().split(".")[-1]) == 0:
                subMask = str(i[0])
            else:
                ip_info = i[0][:i[0].rfind(".")]
                if ip_info not in ip_add: ip_add.append(ip_info)
        #########计算广播地址
        broad_list = []
        for j in ip_add:
            subMask_split = subMask.split(".")
            myIp = (j + ".1").split(".")
            str_cast = ""
            for i in range(4):
                xx = (int(myIp[i]) & int(subMask_split[i])) | ((int(subMask_split[i])) ^ 255)
                str_cast = str_cast + str(xx) + "."
            broad_list.append(str_cast.rstrip("."))
        return broad_list

    @staticmethod
    def getHostIp():
        '''
        获取本机IP
        :return:
        '''
        # return "192.168.1.208"
        myname = socket.getfqdn(socket.gethostname())
        # 获取本机ip
        myaddr = socket.gethostbyname(myname)
        return myaddr

    @staticmethod
    def getHostMac():
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])



if __name__ == "__main__":
    help(NetHelper)
    print (NetHelper.getBroacastAddree())