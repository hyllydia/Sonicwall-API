#coding:utf-8
"""
Author:Hou Yuling
Time:4/7/2022 3:48 PM
"""
import requests
import demo_data
import logging
import json
import time
import datetime
from requests.auth import HTTPBasicAuth
import copy
import urllib3
urllib3.disable_warnings()


class Test_sdwan:
    def __init__(self,username,password,ipstr):
        self.username=username
        self.password=password
        self.url="https://"+ipstr+'/api/sonicos'

    def api_login(self,username,password):
        url = self.url + demo_data.path_Auth
        body = {'override': True}
        headers = {'Content-Type': 'application/json', 'Accept-Encoding': 'application/json'}
        try:
            r = requests.post(url, auth=HTTPBasicAuth(username=username, password=password), data=json.dumps(body), headers=headers,
                              verify=False)
            msg_res = r.json()['status']['info'][0]['message']
            if (r.status_code==200):
                print("Login successful.")
                logging.info("login response msg:{}".format(msg_res))
            else:
                logging.error("login error msg:{}".format(msg_res))
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print ("- LoginERROR - Web service exception, msg = {}".format(e))

    def api_commit(self):
        url = self.url + demo_data.path_Commit
        headers = {'Content-Type': 'application/json', 'Accept-Encoding': 'application/json','Connection':'close'}
        try:
            res = requests.post(url, headers=headers, verify=False,stream=False)
            print(res.json())
            msg_commit_res = res.json()['status']['info'][0]['message']
            logging.info("Commit status code =={}!!commit respond message:{} ".format(res.status_code,msg_commit_res))
            max_code=res.status_code
            print(max_code)
            if "Unauthorized" in msg_commit_res:
                print ("For commit--Unauthorized. Try to login again.")
                self.api_login(username=self.username,password=self.password)
            elif "Not allowed in current mode" in msg_commit_res:
                print ("commit error--{}. Try to set config mode.".format(msg_commit_res))
                self.set_configMode()
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            t = datetime.datetime.now()
            print ("{}- CommitERROR - Web service exception, msg = {}".format(t,e))

    def set_configMode(self):
        url=self.url + '/config-mode'
        body={}
        headers = {'Content-Type': 'application/json', 'Accept-Encoding': 'application/json', 'Connection': 'close'}
        try:
            r=requests.post(url=url,headers=headers,data=body,verify=False,stream=False,timeout=150)
            print(r.json())
        except Exception as e:
            print(type(e))
            print(e.args)

    def temp_list(self,dict1,x):
        temp_list = []
        for m in range(1,x):
            temp_dict = copy.deepcopy(dict1)
            temp_list.append(temp_dict)
        return temp_list

    def run_start_params(self,sn):
            if sn >= 255:
                b = sn // 255 +1
                a = sn % 255
            else:
                b = 1
                a = sn
            return a, b

    def test_tunnel_vpn(self,sn,en,vlan_id=3400,Flag=True):
        sn,en=int(sn),int(en)
        m=2
        x=2
        num=en+1
        vlan_id = vlan_id + m
        Tunnel_VPN_list = self.temp_list(demo_data.test_tunnel_vpn, x)
        #print(Tunnel_VPN_list)
        for i in range(sn,num):
            caseobj_tunnel_vpn=[]
            casebody_tunnel_vpn={"vpn": {"policy": caseobj_tunnel_vpn}}
            tunnel_vpn_name = "tunnel_vpn" + str(m)
            print(tunnel_vpn_name)
            url_test_tunnel_vpn = self.url+ "/vpn/policies/ipv4/tunnel-interface/name/" + tunnel_vpn_name
            #print(url_test_tunnel_vpn)
            """5700"""
            interface_name = 'X28:V' + str(vlan_id)
            print(interface_name)
            gw_ip = "14." + "110" + "." + str(m) + ".1"
            peer_ike_id=gw_ip

            params_vpn = Tunnel_VPN_list[0]['vpn']['policy'][0]
            params_vpn['ipv4']['tunnel_interface']['name'] = tunnel_vpn_name
            params_vpn['ipv4']['tunnel_interface']['enable'] = Flag
            params_vpn['ipv4']['tunnel_interface']['gateway']['primary'] = gw_ip
            params_vpn['ipv4']['tunnel_interface']['bound_to']['interface'] = interface_name
            params_vpn['ipv4']['tunnel_interface']['auth_method']['shared_secret']['ike_id']['peer']['ipv4'] = peer_ike_id
            caseobj_tunnel_vpn.append(params_vpn)
            m+=2
            vlan_id+=2
            data_tunnel_vpn=json.dumps(casebody_tunnel_vpn)
            try:
                self.api_login(username=self.username,password=self.password)
                headers = {'Content-Type': 'application/json', 'Accept-Encoding': 'application/json','Connection': 'close'}
                r=requests.put(url=url_test_tunnel_vpn,headers=headers,data=data_tunnel_vpn,verify=False,stream=False,timeout=150)
                print(r.json())
                msg_res = r.json()['status']['info'][0]['message']
                logging.info("post {} to {} objects, status_code=={},response msg:{}".format(sn, en, r.status_code, msg_res))
                if "Unauthorized" in msg_res:
                    print("For post {}-{} object msg error--{}. Try to login again.".format(sn, en, msg_res))
                    self.api_login(username=self.username, password=self.password)
                elif "Not allowed in current mode" in msg_res:
                    print("For post {}-{} object msg error--{}. Try to set config mode.".format(sn, en, msg_res))
                    self.set_configMode()
                    r.raise_for_status()
            except Exception as e:
                print(type(e))
                print(e.args)
            finally:
                self.api_commit()

if __name__=="__main__":
    ipstr="10.7.5.155"
    username="admin"
    password="sonicwall"
    sdwan_test=Test_sdwan(ipstr=ipstr,username=username,password=password)
    sdwan_test.api_login(username=username, password=password)
    for i in range(1,100):
        print("*****"+str(i)+" Disable tunnel VPN:")
        sdwan_test.test_tunnel_vpn(sn=1,en=64,Flag=False)
        time.sleep(100)
        print("*****"+str(i)+" Enable tunnel VPN:")
        sdwan_test.test_tunnel_vpn(sn=1,en=64,Flag=True)
        time.sleep(100)


