#coding:utf-8
#1、subprocess第三方库用来运行命令，subprocess.Popen(cmd,shell=True)
#2、format()的用法
#3、xrange返回的是一个生成器，range返回的是一个列表；
#4.os.system()用来调用执行另外一个python文件，并且传递参数
import subprocess
import os
import datetime
import telnetlib
import time
import re,sys
import string
import signal

usernumber=10
cyclenumber=2

def cycle():
    c=cyclenumber

    for o in range(1,c):
        print("n=",o)
        add_virtual()
    time.sleep(10)
    for p in range(1,c):
        print("n=",p)
        del_virtual()

def deal_ab(a,b):
    if b>255:
        b=0
        a+=1
    return (a,b)


def add_virtual():
    a=24
    b=10
    for i in range(1,usernumber):
        print(i)
        a,b = deal_ab(a,b)
        cmd = "ifconfig ens192:{} 172.247.{}.{}/24 up".format(i,a,b)
        #cmd =("ifconfig ens192:%d 172.1.%d.%d/16" %(i,a,b))
        subprocess.Popen(cmd,shell=True)
        ip_login = "172.247.{}.{}".format(a,b)
        username = "test{}".format(i)
        os.system("python userlogin.py {} {}".format(ip_login,username))
        #x = ("%d %d" % (a,b))
        #print(x)
        b+=1

def del_virtual():
    a=1
    b=1
    for i in range(1,usernumber):
        print(i)
        a,b = deal_ab(a,b)
        cmd = "ifconfig ens192:{} 172.16.{}.{}/16 down".format(i,a,b)
        #cmd =("ifconfig ens192:%d 172.1.%d.%d/16" %(i,a,b))
        subprocess.Popen(cmd,shell=True)
        b+=1
    
if __name__=="__main__":
    start_time = datetime.datetime.now()
    print("start:{}".format(start_time))
    #add_virtual()
    cycle()
    end_time = datetime.datetime.now()
    print("end:{}".format(end_time))