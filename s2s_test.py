#coding:utf-8
"""
Author:Hou Yuling
Time:3/10/2022 2:03 PM
"""
import datetime
import time
import demo_data
import requests
import json
from requests.auth import HTTPBasicAuth
import logging
import urllib3
import copy
urllib3.disable_warnings()

class DEMO_api:
    def __init__(self,username,password,ipstr):
        self.username=username
        self.password=password
        self.url="https://"+ipstr+'/api/sonicos'

    def run_start_params(self,sn):
            if sn >= 255:
                b = sn // 255 +1
                a = sn % 255
            else:
                b = 1
                a = sn
            return a, b

    def dealwith_FOR_loop(self,sn,num,step):
        n = sn + step
        if n <= num and sn <= num:
            loop = n
        elif n > num and num > sn:
            loop = num
        else:
            print ("please enter right num!!")
        return loop

    def dealwith_abc(self,a,b,c):
        if a > 255:
            a = 0
            b += 1
        if b > 255:
            b = 0
            c += 1
        return a,b,c

    def temp_list(self,dict1,x):
        temp_list = []
        for m in range(1,x):
            temp_dict = copy.deepcopy(dict1)
            temp_list.append(temp_dict)
        return temp_list
        #return [temp_list.append(copy.deepcopy(dict1)) for m in range(1,x)]

    def post_vlan_interfaces(self,ipstr,sn,en,step=1,vlan_id=1):
        sn,en=int(sn),int(en)
        url_vlan_interfaces=self.url+demo_data.path_vlan_interfaces
        #print(url_vlan_interfaces)
        a, b = self.run_start_params(sn)
        # SDWAN VPN Target
        #vlan_id=3400
        # SDWAN WAN Target
        #vlan_id=3000
        num=en+1
        x=step+1
        vlan_id=vlan_id+a
        #print(vlan_id)
        Vlan_interfaces_list=self.temp_list(demo_data.Vlan_interfaces,x)
        for i in range(sn,num,step):
            caseobj_vlan_interfaces=[]
            casebody_vlan_interfaces={"interfaces":caseobj_vlan_interfaces}
            loop=i+step
            t=0
            for j in range(i,loop):
                """
                SDWAN WAN Target:
                5700HA: X28:V3001~X28:V3255  31.111.1.2/24~31.111.255.2/24
                """
                """
                SDWAN VPN Target:
                11700: X23:V3401~X23:V3528  14.110.1.1/24~14.110.128.1/24
                5700HA: X28:V3401~X28:V3528  14.110.1.2/24~14.110.128.2/24
                添加不同firewall注意修改参数
                """
                """5700HA"""
                # vlan_interface="X28"
                # vlan_interface_ip="14."+"110."+str(a)+".2"

                """11700"""
                # vlan_interface="X23"
                # vlan_interface_ip="14."+"110."+str(a)+".1"

                """SDWAN WAN Target的时候需要配置gateway， 但是VPN Target的时候不需要配置gateway"""

                vlan_interface="X28"
                vlan_interface_ip="31."+"111."+str(a)+".2"
                gateway_ip="31."+"111."+str(a)+".1"
                #print(gateway_ip)
                
                params_vlan_interfaces = Vlan_interfaces_list[t]['interfaces'][0]
                params_vlan_interfaces['ipv4']['name']=vlan_interface
                params_vlan_interfaces['ipv4']['vlan'] = vlan_id
                print(vlan_id)
                params_vlan_interfaces['ipv4']['ip_assignment']['mode']['static']['ip']= vlan_interface_ip

                """SDWAN WAN Target的时候需要配置gateway， 但是VPN Target的时候不需要配置gateway"""
                params_vlan_interfaces['ipv4']['ip_assignment']['mode']['static']['gateway']=gateway_ip

                caseobj_vlan_interfaces.append(params_vlan_interfaces)
                #print(caseobj_vlan_interfaces)
                a+=1
                t+=1
                vlan_id+=1
            data_vlan_interfaces=json.dumps(casebody_vlan_interfaces)
            max_code = self.post_object(ipstr, url_vlan_interfaces, data_vlan_interfaces, i, loop - 1)

    def delete_vlan_interfaces(self,ipstr,sn,en,step=1,vlan_id=1):
        #vlan_id=3000
        sn,en=int(sn),int(en)
        a,b=self.run_start_params(sn)
        vlan_id=vlan_id+a
        vlan_interface='X28'
        num=en+1
        for i in range(sn,num,step):
            loop=i++step
            for j in range(i,loop):
                url_delete_vlan_interfaces = self.url + demo_data.path_vlan_interfaces + "/name/" + vlan_interface + "/vlan/" + str(vlan_id)
                print(url_delete_vlan_interfaces)
                try:
                    self.api_login(username=username,password=password)
                    r=requests.delete(url=url_delete_vlan_interfaces,verify=False)
                    print(r.json())
                    print(r.status_code)
                except requests.exceptions.RequestException as e:
                    logging.error(e)
                    print ("- PostERROR - Web service exception, msg = {}".format(e))
                finally:
                    self.api_commit(url_delete_vlan_interfaces)
                vlan_id+=1

    def delete_tunnel_interfaces(self,ipstr,sn,en,step=1):
        sn, en = int(sn), int(en)
        a, b = self.run_start_params(sn)

        num = en + 1
        for i in range(sn, num, step):
            loop = i + +step
            for j in range(i, loop):
                tunnel_interface_name = "tunnel_" + str(a)
                url_delete_tunnel_interfaces = self.url + demo_data.path_tunnel_vpn_interface + "/name/" + tunnel_interface_name
                print(url_delete_tunnel_interfaces)
                try:
                    self.api_login(username=self.username, password=self.password)
                    r = requests.delete(url=url_delete_tunnel_interfaces, verify=False)
                    print(r.json())
                    print(r.status_code)
                except requests.exceptions.RequestException as e:
                    logging.error(e)
                    print("- PostERROR - Web service exception, msg = {}".format(e))
                finally:
                    self.api_commit(url_delete_tunnel_interfaces)
                a += 1

    def post_tunnel_interface(self,ipstr,sn,en,step=1):
        sn, en = int(sn), int(en)
        url_tunnel_vpn_interface= self.url + demo_data.path_tunnel_vpn_interface
        a, b = self.run_start_params(sn)
        num = en + 1
        x = step + 1
        tunnel_vpn_interface_list = self.temp_list(demo_data.tunnel_vpn_interface, x)
        for i in range(sn, num, step):
            caseobj_tunnel_vpn_interface = []
            casebody_tunnel_vpn_interface = {"tunnel_interfaces": caseobj_tunnel_vpn_interface}
            loop = i + step
            t = 0
            for j in range(i, loop):
                tunnel_interface_name="tunnel_"+str(j)
                print(tunnel_interface_name)
                """11700"""
                tunnel_interface_ip="150."+"1."+str(a)+".1"
                """5700HA"""
                #tunnel_interface_ip = "160." + "1." + str(a) + ".1"
#
                tunnel_vpn="tunnel_vpn"+str(j)

                params_tunnel_vpn_interface = tunnel_vpn_interface_list[t]['tunnel_interfaces'][0]
                params_tunnel_vpn_interface['vpn']['name'] = tunnel_interface_name
                params_tunnel_vpn_interface['vpn']['ip_assignment']['mode']['static']['ip']=tunnel_interface_ip
                params_tunnel_vpn_interface['vpn']['policy']=tunnel_vpn

                caseobj_tunnel_vpn_interface.append(params_tunnel_vpn_interface)
                a+=1
                t+=1
            data_tunnel_vpn_interface = json.dumps(casebody_tunnel_vpn_interface)
            max_code = self.post_object(ipstr, url_tunnel_vpn_interface, data_tunnel_vpn_interface, i, loop - 1)

    def post_sdwan_groups(self,ipstr,sn,en,step=1,vlan_id=1):
        sn,en=int(sn),int(en)
        url_sdwan_groups=self.url+demo_data.path_sdwan_groups
        a, b = self.run_start_params(sn)
        num = en + 1
        x = step + 1
        sdwan_groups_list=self.temp_list(demo_data.sdwan_groups,x)
        for i in range(sn,num,step):
            caseobj_sdwan_groups = []
            casebody_sdwan_groups = {"sdwan": { "group":caseobj_sdwan_groups}}
            loop = i + step
            t = 0
            for j in range(i,loop,2):
                vlan_ida = vlan_id+a*2-1
                vlan_idb = vlan_id + a*2
                interface="X28"
                sdwan_group_name='sdwan_group'+str(a)
                print(sdwan_group_name)
                params_sdwan_groups =sdwan_groups_list[t]['sdwan']['group'][0]
                params_sdwan_groups['name']=sdwan_group_name
                params_sdwan_groups['interface'][0]['name']=interface+":V"+str(vlan_ida)
                params_sdwan_groups['interface'][1]['name']=interface+":V"+str(vlan_idb)
                t+=1
                a+=1
                caseobj_sdwan_groups.append(params_sdwan_groups)
            data_sdwan_groups=json.dumps(casebody_sdwan_groups)
            max_code = self.post_object(ipstr, url_sdwan_groups, data_sdwan_groups, i, loop - 1)

    def post_sdwan_vpn_groups(self, ipstr, sn, en, step=1):
        sn, en = int(sn), int(en)
        url_sdwan_groups = self.url + demo_data.path_sdwan_groups
        a, b = self.run_start_params(sn)
        num = en + 1
        x = step + 1
        sdwan_groups_list = self.temp_list(demo_data.sdwan_groups, x)
        for i in range(sn, num, step):
            caseobj_sdwan_groups = []
            casebody_sdwan_groups = {"sdwan": {"group": caseobj_sdwan_groups}}
            loop = i + step
            t = 0
            for j in range(i, loop, 2):
                tunnel_vpn_interface_name1 ="tunnel_"+str(a*2-1)
                tunnel_vpn_interface_name2 = "tunnel_" + str(a*2)
                sdwan_group_name = 'sdwan_vpn_group' + str(a)
                print(sdwan_group_name)

                params_sdwan_groups = sdwan_groups_list[t]['sdwan']['group'][0]
                params_sdwan_groups['name'] = sdwan_group_name
                params_sdwan_groups['interface'][0]['name'] = tunnel_vpn_interface_name1
                params_sdwan_groups['interface'][1]['name'] = tunnel_vpn_interface_name2
                t += 1
                a+= 1
                caseobj_sdwan_groups.append(params_sdwan_groups)
            data_sdwan_groups = json.dumps(casebody_sdwan_groups)
            max_code = self.post_object(ipstr, url_sdwan_groups, data_sdwan_groups, i, loop - 1)

    def post_sdwan_probes(self,ipstr,sn,en,step=1):
        sn,en=int(sn),int(en)
        url_probe=self.url+demo_data.path_sdwan_probes
        url_ao=self.url+demo_data.path_AO
        a,b = self.run_start_params(sn)
        num = en+1
        x=step+1
        AO_list=self.temp_list(demo_data.AO_Host,x)
        Probe_list=self.temp_list(demo_data.sdwan_probes,x)
        for i in range(sn,num,step):
            caseobj_ao=[]
            caseobj_probe=[]
            casebody_ao={"address_objects":caseobj_ao}
            casebody_probe={"sdwan":{"sla_probe":caseobj_probe}}
            loop = i +step
            t=0
            for j in range(i,loop):
                #a, b, c = self.dealwith_abc(a, b, c)
                ao_host="31."  + "112." + str(a) + ".1"
                #print(ao_host)
                params_ao = AO_list[t]['address_objects'][0]
                params_ao["ipv4"]["name"] = ao_host
                params_ao["ipv4"]["zone"] = "WAN"
                params_ao["ipv4"]["host"]["ip"] =ao_host
                caseobj_ao.append(params_ao)
                #sdwan_probes
                sdwan_probe1="sdwan_probe"+str(a*2-1)
                print(sdwan_probe1)
                sdwan_probe2="sdwan_probe"+str(a*2)
                print(sdwan_probe2)
                sdwan_group_name="sdwan_group"+str(a)
                print(sdwan_group_name)
                probe_target=ao_host
                #type-ping
                params_probe1=Probe_list[t]["sdwan"]["sla_probe"][0]
                params_probe1["ipv4"]["name"]=sdwan_probe1
                params_probe1["ipv4"]["sdwan_group"]=sdwan_group_name
                params_probe1["ipv4"]["probe"]["target"]["name"]=probe_target
                #type-TCP
                params_probe2 = Probe_list[t]["sdwan"]["sla_probe"][1]
                params_probe2["ipv4"]["name"] = sdwan_probe2
                params_probe2["ipv4"]["sdwan_group"] = sdwan_group_name
                params_probe2["ipv4"]["probe"]["target"]["name"] = probe_target

                caseobj_probe.append(params_probe1)
                caseobj_probe.append(params_probe2)
                a+=1
                t+=1
            data_ao=json.dumps(casebody_ao)
            data_probe=json.dumps(casebody_probe)
            #message1 = self.post_object(ipstr, url_ao, data_ao, i, loop - 1)
            max_code = self.post_object(ipstr, url_probe, data_probe, i, loop - 1)

    def post_sdwan_paths(self,ipstr,sn,en,step=1):
        sn, en = int(sn), int(en)
        url_path = self.url + demo_data.path_sdwan_paths
        a, b = self.run_start_params(sn)
        num = en + 1
        x = step + 1
        Path_list = self.temp_list(demo_data.sdwan_paths, x)
        for i in range(sn, num, step):
            caseobj_path = []
            casebody_path = {"sdwan": {"path_selection_profile": caseobj_path}}
            loop = i + step
            t = 0
            for j in range(i, loop):
                sdwan_path1="sdwan_path"+str(a*3-2)
                sdwan_path2 = "sdwan_path" + str(a*3-1)
                sdwan_path3 = "sdwan_path" + str(a*3)
                sdwan_probe_name="sdwan_probe"+str(a*2)
                sdwan_group_name="sdwan_group"+str(a)
                #Lowest Latency
                params_path1 = Path_list[t]["sdwan"]["path_selection_profile"][0]
                params_path1["name"] = sdwan_path1
                params_path1["sdwan_group"] = sdwan_group_name
                params_path1["sla_probe"] = sdwan_probe_name
                #Lowest Packet Loss
                params_path2 = Path_list[t]["sdwan"]["path_selection_profile"][1]
                params_path2["name"] = sdwan_path2
                params_path2["sdwan_group"] = sdwan_group_name
                params_path2["sla_probe"] = sdwan_probe_name
                #Lowest Jitter
                params_path3 = Path_list[t]["sdwan"]["path_selection_profile"][2]
                params_path3["name"] = sdwan_path3
                params_path3["sdwan_group"] = sdwan_group_name
                params_path3["sla_probe"] = sdwan_probe_name

                caseobj_path.append(params_path1)
                caseobj_path.append(params_path2)
                caseobj_path.append(params_path3)

                a += 1
                t += 1

            data_path = json.dumps(casebody_path)
            #message1 = self.post_object(ipstr, url_ao, data_ao, i, loop - 1)
            max_code = self.post_object(ipstr, url_path, data_path, i, loop - 1)

    def post_sdwan_vpn_paths(self,ipstr,sn,en,step=1):
        sn, en = int(sn), int(en)
        url_path = self.url + demo_data.path_sdwan_paths
        a, b = self.run_start_params(sn)
        num = en + 1
        x = step + 1
        Path_list = self.temp_list(demo_data.sdwan_vpn_paths, x)
        for i in range(sn, num, step):
            caseobj_path = []
            casebody_path = {"sdwan": {"path_selection_profile": caseobj_path}}
            loop = i + step
            t = 0
            for j in range(i, loop):
                sdwan_path1="sdwan_vpn_path"+str(a*3-2)
                print(sdwan_path1)
                sdwan_path2 = "sdwan_vpn_path" + str(a*3-1)
                print(sdwan_path2)
                sdwan_path3 = "sdwan_vpn_path" + str(a*3)
                print(sdwan_path3)
                sdwan_probe_name="VPN Probe - sdwan_vpn_group"+str(a)
                sdwan_group_name="sdwan_vpn_group"+str(a)
                #Lowest Latency
                params_path1 = Path_list[t]["sdwan"]["path_selection_profile"][0]
                params_path1["name"] = sdwan_path1
                params_path1["sdwan_group"] = sdwan_group_name
                params_path1["sla_probe"] = sdwan_probe_name
                #Lowest Packet Loss
                params_path2 = Path_list[t]["sdwan"]["path_selection_profile"][1]
                params_path2["name"] = sdwan_path2
                params_path2["sdwan_group"] = sdwan_group_name
                params_path2["sla_probe"] = sdwan_probe_name
                #Lowest Jitter
                params_path3 = Path_list[t]["sdwan"]["path_selection_profile"][2]
                params_path3["name"] = sdwan_path3
                params_path3["sdwan_group"] = sdwan_group_name
                params_path3["sla_probe"] = sdwan_probe_name

                caseobj_path.append(params_path1)
                caseobj_path.append(params_path2)
                caseobj_path.append(params_path3)

                a += 1
                t += 1

            data_path = json.dumps(casebody_path)
            #message1 = self.post_object(ipstr, url_ao, data_ao, i, loop - 1)
            max_code = self.post_object(ipstr, url_path, data_path, i, loop - 1)

    def post_sdwan_rules(self,ipstr,sn,en,step=1):
        sn, en = int(sn), int(en)
        url_sdwan_rules = self.url + demo_data.path_sdwan_rules
        a, b = self.run_start_params(sn)
        num = en + 1
        x = step + 1
        sdwan_rules_list = self.temp_list(demo_data.sdwan_rules, x)
        for i in range(sn, num, step):
            caseobj_sdwan_rules = []
            casebody_sdwan_rules = {"route_policies": caseobj_sdwan_rules}
            loop = i + step
            t = 0
            for j in range(i, loop):
                interface_name = "sdwan_group"+str(a)
                rule1_name = "sdwan_rule"+str(a*3-2)
                print(rule1_name)
                rule2_name="sdwan_rule"+str(a*3-1)
                print(rule2_name)
                rule3_name="sdwan_rule"+str(a*3)
                print(rule3_name)
                path1_name="sdwan_path"+str(a*3-2)
                path2_name = "sdwan_path" + str(a*3-1)
                path3_name = "sdwan_path" + str(a*3)
                metric_value = a

                # path1_rule
                params_rule1 = sdwan_rules_list[t]["route_policies"][0]
                params_rule1["ipv4"]["interface"] = interface_name
                params_rule1["ipv4"]["metric"] = metric_value
                params_rule1["ipv4"]["path_selection_profile"] = path1_name
                params_rule1["ipv4"]["name"] = rule1_name
                # path2_rule
                params_rule2 = sdwan_rules_list[t]["route_policies"][1]
                params_rule2["ipv4"]["interface"] = interface_name
                params_rule2["ipv4"]["metric"] = metric_value
                params_rule2["ipv4"]["path_selection_profile"] = path2_name
                params_rule2["ipv4"]["name"] = rule2_name
                # # path3_rule
                params_rule3 = sdwan_rules_list[t]["route_policies"][2]
                params_rule3["ipv4"]["interface"] = interface_name
                params_rule3["ipv4"]["metric"] = metric_value
                params_rule3["ipv4"]["path_selection_profile"] = path3_name
                params_rule3["ipv4"]["name"] = rule3_name

                caseobj_sdwan_rules.append(params_rule1)
                caseobj_sdwan_rules.append(params_rule2)
                caseobj_sdwan_rules.append(params_rule3)

                a += 1
                t += 1
            data_rule = json.dumps(casebody_sdwan_rules)
            # message1 = self.post_object(ipstr, url_ao, data_ao, i, loop - 1)
            max_code = self.post_object(ipstr, url_sdwan_rules, data_rule, i, loop - 1)

    def post_sdwan_vpn_rules(self,ipstr,sn,en,step=1):
        sn, en = int(sn), int(en)
        url_sdwan_rules = self.url + demo_data.path_sdwan_rules
        a, b = self.run_start_params(sn)
        num = en + 1
        x = step + 1
        sdwan_rules_list = self.temp_list(demo_data.sdwan_vpn_rules, x)
        for i in range(sn, num, step):
            caseobj_sdwan_rules = []
            casebody_sdwan_rules = {"route_policies": caseobj_sdwan_rules}
            loop = i + step
            t = 0
            for j in range(i, loop):
                interface_name = "sdwan_vpn_group" + str(a)
                metric_value=a
                rule1_name = "sdwan_vpn_rule" + str(a * 3 - 2)
                print(rule1_name)
                rule2_name = "sdwan_vpn_rule" + str(a * 3 - 1)
                print(rule2_name)
                rule3_name = "sdwan_vpn_rule" + str(a * 3)
                print(rule3_name)
                path1_name = "sdwan_vpn_path" + str(a * 3 - 2)
                path2_name = "sdwan_vpn_path" + str(a * 3 - 1)
                path3_name = "sdwan_vpn_path" + str(a * 3)

                # path1_rule
                params_rule1 = sdwan_rules_list[t]["route_policies"][0]
                params_rule1["ipv4"]["interface"] = interface_name
                params_rule1["ipv4"]["metric"] = metric_value                
                params_rule1["ipv4"]["path_selection_profile"] = path1_name
                params_rule1["ipv4"]["name"] = rule1_name
                # path2_rule
                params_rule2 = sdwan_rules_list[t]["route_policies"][1]
                params_rule2["ipv4"]["interface"] = interface_name
                params_rule2["ipv4"]["metric"] = metric_value
                params_rule2["ipv4"]["path_selection_profile"] = path2_name
                params_rule2["ipv4"]["name"] = rule2_name
                # # path3_rule
                params_rule3 = sdwan_rules_list[t]["route_policies"][2]
                params_rule3["ipv4"]["interface"] = interface_name
                params_rule3["ipv4"]["metric"] = metric_value
                params_rule3["ipv4"]["path_selection_profile"] = path3_name
                params_rule3["ipv4"]["name"] = rule3_name

                caseobj_sdwan_rules.append(params_rule1)
                caseobj_sdwan_rules.append(params_rule2)
                caseobj_sdwan_rules.append(params_rule3)

                a += 1
                t += 1
            data_rule = json.dumps(casebody_sdwan_rules)
            # message1 = self.post_object(ipstr, url_ao, data_ao, i, loop - 1)
            max_code = self.post_object(ipstr, url_sdwan_rules, data_rule, i, loop - 1)

    def post_vpn_chained_3rd(self,ipstr,sn,en,step=1):
        sn, en = int(sn), int(en)
        url_vpn = self.url + demo_data.path_VPN
        url_ao = self.url + demo_data.path_AO
        #a, b = self.run_start_params(sn)
        # print(a)#a=73
        # print(b)#b=14
        a=1
        b=10
        c = 57
        num = en + 1
        x = step + 1
        AO_list = self.temp_list(demo_data.AO_Subnet, x)
        VPN_list = self.temp_list(demo_data.VPN_Chained_3rd, x)
        for i in range(sn, num, step):
            caseobj_ao = []
            caseobj_vpn = []
            casebody_ao = {'address_objects': caseobj_ao}
            casebody_vpn = {"vpn": {"policy": caseobj_vpn}}
            # loop = self.dealwith_FOR_loop(i, num, step)
            # print(loop)
            loop = i + step
            t = 0
            for j in range(i, loop):
                a, b, c = self.dealwith_abc(a, b, c)
                # AO
                ao_name = "51." + str(b) + "." + str(a) + ".0"
                print(ao_name)
                params_ao = AO_list[t]['address_objects'][0]
                params_ao["ipv4"]["name"] = ao_name
                params_ao["ipv4"]["zone"] = "VPN"
                params_ao["ipv4"]["network"]["subnet"] = ao_name
                caseobj_ao.append(params_ao)
                # VPN_Chained_3rd
                vpn_pol_name = 'VPN_Chained_3rd_' + str(j)
                print(vpn_pol_name)
                gw_ip = "172." + str(c) + "." + str(b) + "." + str(a)
                #print(gw_ip)
                #peer_ike_id = gw_ip
                local_name = "X27 Subnet"
                remote_name = ao_name
                params_vpn = VPN_list[t]['vpn']['policy'][0]
                params_vpn['ipv4']['site_to_site']['name'] = vpn_pol_name
                params_vpn['ipv4']['site_to_site']['gateway']['primary'] = gw_ip
                params_vpn['ipv4']['site_to_site']['network']['local']['name'] = local_name
                params_vpn['ipv4']['site_to_site']['network']['remote']['destination_network']['name'] = remote_name
                #params_vpn['ipv4']['site_to_site']['auth_method']['shared_secret']['ike_id']['peer'][
                 #   'ipv4'] = peer_ike_id
                caseobj_vpn.append(params_vpn)
                a += 1
                t += 1

            data_ao = json.dumps(casebody_ao)
            data_vpn = json.dumps(casebody_vpn)
            # print(data_vpn)
            message1 = self.post_object(ipstr, url_ao, data_ao, i, loop - 1)
            max_code = self.post_object(ipstr, url_vpn, data_vpn, i, loop - 1)

    def post_s2s_vpn_IKEv2(self,ipstr,sn,en,step=1):
        sn,en=int(sn),int(en)
        #url_vpn = "https://" + ipstr + demo_data.path_VPN
        #url_ao = "https://" + ipstr +demo_data.path_AO
        url_vpn = self.url + demo_data.path_VPN
        url_ao = self.url + demo_data.path_AO
        a,b=self.run_start_params(sn)
        c=1
        num=en+1
        x=step+1
        AO_list=self.temp_list(demo_data.AO_Subnet,x)
        VPN_list=self.temp_list(demo_data.VPN_IKEv2,x)
        for i in range(sn,num,step):
            caseobj_ao=[]
            caseobj_vpn=[]
            casebody_ao = {'address_objects': caseobj_ao}
            casebody_vpn = {"vpn": {"policy": caseobj_vpn}}
            #loop = self.dealwith_FOR_loop(i, num, step)
            #print(loop)
            loop= i + step
            t=0
            for j in range(i,loop):
                a, b, c = self.dealwith_abc(a, b, c)
                #AO
                ao_name = "21." + str(b) + "." + str(a) + ".0"
                params_ao=AO_list[t]['address_objects'][0]
                params_ao["ipv4"]["name"]=ao_name
                params_ao["ipv4"]["zone"]="VPN"
                params_ao["ipv4"]["network"]["subnet"]=ao_name
                caseobj_ao.append(params_ao)
                #VPN_IKEv2
                vpn_pol_name='VPN_IKEv2_'+str(j)
                print(vpn_pol_name)
                gw_ip = "172." + str(c) + "." + str(b) + "." + str(a)
                peer_ike_id=gw_ip
                local_name="X0 Subnet"
                remote_name=ao_name
                params_vpn=VPN_list[t]['vpn']['policy'][0]
                params_vpn['ipv4']['site_to_site']['name']=vpn_pol_name
                params_vpn['ipv4']['site_to_site']['gateway']['primary']=gw_ip
                params_vpn['ipv4']['site_to_site']['network']['local']['name']=local_name
                params_vpn['ipv4']['site_to_site']['network']['remote']['destination_network']['name'] = remote_name
                params_vpn['ipv4']['site_to_site']['auth_method']['shared_secret']['ike_id']['peer']['ipv4'] = peer_ike_id
                caseobj_vpn.append(params_vpn)
                a+=1
                t+=1

            data_ao=json.dumps(casebody_ao)
            data_vpn=json.dumps(casebody_vpn)
           # print(data_vpn)
            message1=self.post_object(ipstr,url_ao,data_ao,i,loop-1)
            max_code = self.post_object(ipstr, url_vpn, data_vpn, i, loop - 1)

    def post_tunnel_vpn(self,ipstr,sn,en,step=1,vlan_id=1):
        sn,en=int(sn),int(en)
        url_tunnel_vpn = self.url + demo_data.path_tunnel_vpn
        a,b=self.run_start_params(sn)
        num=en+1
        x=step+1
        vlan_id=vlan_id+a
        VPN_list=self.temp_list(demo_data.tunnel_vpn,x)
        for i in range(sn,num,step):
            caseobj_tunnel_vpn=[]
            casebody_tunnel_vpn = {"vpn": {"policy": caseobj_tunnel_vpn}}
            #loop = self.dealwith_FOR_loop(i, num, step)
            #print(loop)
            loop= i + step
            t=0
            for j in range(i,loop):
                #tunnel_vpn
                tunnel_vpn_name='tunnel_vpn'+str(j)
                print(tunnel_vpn_name)
                """
                11700
                """
                interface_name='X23:V'+str(vlan_id)
                print(interface_name)
                gw_ip = "14." + "110"+ "." + str(a) +".2"
                peer_ike_id = gw_ip
                """
                5700HA
                """
                # interface_name = 'X28:V' + str(vlan_id)
                # print(interface_name)
                # gw_ip = "14." + "110" + "." + str(a) + ".1"
                # peer_ike_id=gw_ip

                #print(peer_ike_id)
                params_vpn=VPN_list[t]['vpn']['policy'][0]
                params_vpn['ipv4']['tunnel_interface']['name']=tunnel_vpn_name
                params_vpn['ipv4']['tunnel_interface']['gateway']['primary']=gw_ip
                params_vpn['ipv4']['tunnel_interface']['bound_to']['interface']=interface_name
                params_vpn['ipv4']['tunnel_interface']['auth_method']['shared_secret']['ike_id']['peer']['ipv4']=peer_ike_id

                caseobj_tunnel_vpn.append(params_vpn)

                a+=1
                t+=1
                vlan_id+=1
            data_tunnel_vpn=json.dumps(casebody_tunnel_vpn)
            max_code = self.post_object(ipstr, url_tunnel_vpn, data_tunnel_vpn, i, loop - 1)

    def post_object(self,ipstr,url,data,sn,en):
        headers = {'Content-Type': 'application/json', 'Accept-Encoding': 'application/json','Connection':'close'}
        try:
            self.api_login(username=self.username,password=self.password)
            r = requests.post(url, data=data, headers=headers, stream=False,verify=False, timeout=150)
            print(r.json())
            msg_res = r.json()['status']['info'][0]['message']
            #print(type(msg_res))
            logging.info("post {} to {} objects, status_code=={},response msg:{}".format(sn,en,r.status_code,msg_res))
            if "Unauthorized" in msg_res:
                print ("For post {}-{} object msg error--{}. Try to login again.".format(sn,en,msg_res))
                self.api_login(username=self.username,password=self.password)
            elif "Not allowed in current mode" in msg_res:
                print ("For post {}-{} object msg error--{}. Try to set config mode.".format(sn, en, msg_res))
                self.set_configMode()
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(e)
            print ("- PostERROR - Web service exception, msg = {}".format(e))
        finally:
            max_code = self.api_commit()
            return max_code

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
                #self.post_object(ipstr, url_vpn, data_vpn, i, loop - 1)
                #self.api_commit(ipstr)
            elif "Not allowed in current mode" in msg_commit_res:
                print ("commit error--{}. Try to set config mode.".format(msg_commit_res))
                self.set_configMode()
            res.raise_for_status()
            return max_code
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

    def api_login(self,username,password):
        url = self.url + demo_data.path_Auth
        #url= "https://" + ipstr + demo_data.path_Auth
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


if __name__=="__main__":
    ipstr='10.7.100.27'
    username='admin'
    password='password'
    test=DEMO_api(username=username,password=password,ipstr=ipstr)
    test.api_login(username=username,password=password)

    #Add vpn tunnels
    start_time=datetime.datetime.now()
    test.post_s2s_vpn_IKEv2('10.7.100.202',1,3,1)
    #test.post_vpn_chained_3rd(ipstr=ipstr, sn=10,en=5500,step=100)
    end_time=datetime.datetime.now()
    print(end_time-start_time)

    #Add vlan interfaces
    #test.post_vlan_interfaces(ipstr,1,10,1)
    #test.delete_vlan_interfaces('10.7.5.155',1,10,1)

    """SDWAN WAN Target"""
    """vlan interfaces X28:V3001(31.111.1.2)~X28:V3255(31.111.255.2)"""
    #test.post_vlan_interfaces(ipstr=ipstr, sn=2, en=2, step=1,vlan_id=3000)
    """sdwan groups 255 vlan interfaces , 128 sdwan groups"""
    #test.post_sdwan_groups(ipstr=ipstr,sn=1,en=2,step=1,vlan_id=3000)
    """128*2=256 sdwan probes(Type tcp/Type ping)"""
    #test.post_sdwan_probes(ipstr=ipstr,sn=1,en=1,step=1)
    """128*3=384 """
    #test.post_sdwan_paths(ipstr=ipstr,sn=2,en=2,step=1)
    """128*3=384"""
    #test.post_sdwan_rules(ipstr=ipstr,sn=1,en=128,step=1)


    """SDWAN VPN Target"""
    """
    vlan interfaces
    5700HA:X28:V3401(14.110.1.2~14.110.128.2)~X28:V3528(14.110.1.1~14.110.128.1)(128)
    11700:X23:V3401~X23:V3528(128)
    SYS-S6000-1: vlan3401~vlan3528(tagged te0/48,90(5700HA), 0/47(11700), te0/100-103,108-110(IXIA Cards))  with vb scripts
    """
    # test.post_vlan_interfaces(ipstr=ipstr,sn=2,en=128,step=1,vlan_id=3400)
    # time.sleep(3)

    """
    tunnel_vpn
    5700HA:128 tunnel vpn
    11700:128 tunnel vpn
    """
    #test.post_tunnel_vpn(ipstr=ipstr,sn=13,en=13,step=1,vlan_id=3400)
    # time.sleep(3)
    """
    tunnel interfaces
    5700: 128绑定tunnel vpn
    11700:128 绑定 tunnel vpn
    """
    #test.post_tunnel_interface(ipstr=ipstr,sn=2,en=2,step=1)
    # time.sleep(3)
    """
    sdwan vpn groups
    5700: 64
    11700:64
    """
    # test.post_sdwan_vpn_groups(ipstr=ipstr,sn=1,en=64,step=1)
    # time.sleep(3)
    """
    sdwan vpn paths
    5700: 64*3=192
    11700: 64*3=192
    """
    # test.post_sdwan_vpn_paths(ipstr=ipstr,sn=1,en=64,step=1)
    # time.sleep(3)
    """
    sdwan vpn rules
    5700:64*3=192
    11700:64*3=192
    """
    #test.post_sdwan_vpn_rules(ipstr,sn=1,en=64,step=1)


    #Delete vlan interfaces
    #test.delete_vlan_interfaces(ipstr=ipstr, sn=1, en=10, vlan_id=3400)
    #Delete tunnel interfaces
    #test.delete_tunnel_interfaces(ipstr=ipstr,sn=9,en=128,step=1)
