#coding:utf-8
"""
Author:Hou Yuling
Time:12/16/2021 2:56 PM
"""
# -*- coding: utf-8 -*-
from pyVim.connect import SmartConnect
from pyVmomi import vim
import ssl


# si= SmartConnect(host="10.10.10.30", user="administrator@ylpay.vm", pwd="I7GdS]=fe1[13VkoBmbG",sslContext=s)
# # si= SmartConnect(host="10.8.9.20", user="administrator@ylpay.cn", pwd="50qgfFZKniKzu!J3zgL",sslContext=s)
# content=si.content
class GetVmData(object):
    """docstring for GetVmData,获取VM相关数据"""

    def __init__(self, host, user, password):
        super(GetVmData, self).__init__()
        # 主机房信息
        # self.host = "10.10.10.30"
        # self.user = "administrator@ylpay.vm"
        # self.passwd = "I7GdS]=fe1[13VkoBmbG"
        # 测试环境信息
        # self.host = "10.8.9.20"
        # self.user = "administrator@ylpay.cn"
        # self.passwd = "50qgfFZKniKzu!J3zgL"
        self.user = user
        self.host = host
        self.password = password
        s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        s.verify_mode = ssl.CERT_NONE
        self.sslContext = s
        try:
            self.client = SmartConnect(host=host,
                                       user=user,
                                       pwd=password,
                                       sslContext=self.sslContext
                                       )
            self.content = self.client.content
            self.result = True
        except Exception as e:
            self.result = False
            self.message = e

    def get_all_objs(self, obj_type, folder=None):
        if folder is None:
            container = self.content.viewManager.CreateContainerView(self.content.rootFolder, obj_type, True)
        else:
            container = self.content.viewManager.CreateContainerView(folder, obj_type, True)
        return container.view

    def get_obj(self, obj_type, name):
        obj = None
        content = self.content
        container = content.viewManager.CreateContainerView(content.rootFolder, obj_type, True)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj

    # 获取数据中心
    def get_datacenter(self):
        return self._get_all_objs([vim.Datecenter])

    # 根据数据中心名称获取数据中心对象
    def get_datacenter_by_name(self, datacenter_name):
        return self._get_all_objs([vim.Datacenter], datacenter_name)


vm = GetVmData(host="10.8.9.20", user="administrator@ylpay.cn", password="50qgfFZKniKzu!J3zgL")
getAllVms = vm._get_all_objs([vim.VirtualMachine])
res = vm._get_all_objs([vim.HostSystem])
for vm in getAllVms:
    print(vm.summary.guest.hostName)
# try:
#     if len(temp_ip.split('.')[2]) == 1:
#         temp['app_ip'] = temp_ip
#     if len(temp_ip.split('.')[2]) == 2:
#         temp['manager_ip'] = temp_ip
# except Exception as e:
#     print("======> ERROR IS %s" % e)