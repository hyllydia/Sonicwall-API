#coding:utf-8
#1、requests库
#2、sys.argv[]用来接收另一个python文件传递过来的参数；os.system("python 1.py {} {}".format(a,b))    a=sys.argv[1]   b=sys.argv[2]
#3、requests_toolbelt.adapters 用来设置虚拟IP，需要用不同的ip从同一个出口出去
import requests
from requests.auth import HTTPBasicAuth
from requests_toolbelt.adapters import source
import json
import sys
import urllib3
import time
urllib3.disable_warnings()

def user_login(ipstr,username):
        print(ipstr)
        print(username)
        s = requests.Session()
        new_source = source.SourceAddressAdapter(ipstr)
        s.mount('https://', new_source)
        url="https://172.247.24.1/api/sonicos/auth"
       # geturl="http://10.202.6.105:8888"
        geturl="https://10.7.4.37"
        getuserstatusurl="https://172.247.24.1/sonicui/7/session-status/"
        payload={"override":'false',"snwl":'true'}
        data=json.dumps(payload)
        header={
                'Conection':'keep alive',
                'Accept':'application/json, text/plain, */*',
                'Content-Type': 'application/json;charset=UTF-8',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8'
                }
        try:
            requests.packages.urllib3.disable_warnings()
            re1 = s.get(geturl,headers=header,verify=False,allow_redirects=True)
            time.sleep(1)
            print (re1.history)

            re = s.post(url, auth=HTTPBasicAuth(username, '123@abc'), headers=header,data=data,verify=False)
            print(re.json())
            re.raise_for_status()
            print (re)

            if (re.status_code == 200):
                print("Login successful.")
                re3 = s.get(getuserstatusurl,headers=header,verify=False)
                time.sleep(3)
                re3.raise_for_status()
                print(re3)
                time.sleep(2)

                re2 = s.get(geturl,headers=header,verify=False)
                time.sleep(3)
                re2.raise_for_status()
                print (re2)

        except requests.exceptions.RequestException as e:
                print ("- LoginERROR - Web service exception, msg  {}".format(e))
        time.sleep(2)

if __name__=="__main__":
        ipstr = sys.argv[1]
        username = sys.argv[2]
        user_login(ipstr,username)