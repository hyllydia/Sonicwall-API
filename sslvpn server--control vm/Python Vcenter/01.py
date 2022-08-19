#coding:utf-8
"""
Author:Hou Yuling
Time:12/16/2021 2:03 PM
Tips:加判断条件，判断所需要的vms的状态是否全部poweroff或者poweron?
"""
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim,vmodl
import time
MAX_DEPTH=10
class Vcenter:
    def __init__(self,host_ip,username,password):
        self.host_ip = host_ip
        self.username = username
        self.password = password
        self.client = SmartConnect(
            user=username,
            pwd=password,
            host=host_ip,
            disableSslCertValidation=True
    )

    def get_vmnames(self):
        try:
            content=self.client.RetrieveContent()
            for child in content.rootFolder.childEntity:
                if hasattr(child, 'vmFolder'):
                    datacenter = child
                    vmfolder = datacenter.vmFolder
                    vmlist = vmfolder.childEntity
                    for vm in vmlist:
                        self.print_vminfo(vm)
                        #print(type(vm.summary.config.name))
                        return (vm.summary.config.name)
        except Exception as e:
            print(e)
    def print_vminfo(self,vm, depth=1):
        """
        Print information for a particular virtual machine or recurse into a folder
        with depth protection
        """

        # if this is a group it will have children. if it does, recurse into them
        # and then return
        if hasattr(vm, 'childEntity'):
            if depth > MAX_DEPTH:
                return
            vmlist = vm.childEntity
            for child in vmlist:
                self.print_vminfo(child, depth + 1)
            return

        summary = vm.summary
        print(summary.config.name)

    def wait_for_tasks(self,tasks):
        """Given the service instance and tasks, it returns after all the
       tasks are complete
       """
        property_collector = self.client.content.propertyCollector
        task_list = [str(task) for task in tasks]
        # Create filter
        obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                     for task in tasks]
        property_spec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,
                                                                   pathSet=[],
                                                                   all=True)
        filter_spec = vmodl.query.PropertyCollector.FilterSpec()
        filter_spec.objectSet = obj_specs
        filter_spec.propSet = [property_spec]
        pcfilter = property_collector.CreateFilter(filter_spec, True)
        try:
            version, state = None, None
            # Loop looking for updates till the state moves to a completed state.
            while task_list:
                update = property_collector.WaitForUpdates(version)
                for filter_set in update.filterSet:
                    for obj_set in filter_set.objectSet:
                        task = obj_set.obj
                        for change in obj_set.changeSet:
                            if change.name == 'info':
                                state = change.val.state
                            elif change.name == 'info.state':
                                state = change.val
                            else:
                                continue

                            if not str(task) in task_list:
                                continue

                            if state == vim.TaskInfo.State.success:
                                # Remove task from taskList
                                task_list.remove(str(task))
                            elif state == vim.TaskInfo.State.error:
                                raise task.info.error
                # Move to next version
                version = update.version
        finally:
            if pcfilter:
                pcfilter.Destroy()

    def vm_poweroff(self,start,end,bname):
        vmnames = []
        for i in range(start, end + 1):
            vmnames.append(bname + str(i))
        #print(vmnames)
        for vm_name in vmnames:
            print(vm_name)
        content = self.client.RetrieveContent()
        for child in content.rootFolder.childEntity:
            if hasattr(child, 'vmFolder'):
                datacenter = child
                vmfolder = datacenter.vmFolder
                vmlist = vmfolder.childEntity
                try:
                    tasks = [vm.PowerOff() for vm in vmlist if vm.summary.config.name in vmnames]
                    #print(tasks)
                    time.sleep(5)
                    self.wait_for_tasks(tasks)
                    print("Virtual Machines have been powered off successfully")
                except vmodl.MethodFault as error:
                    print("Caught vmodl fault : " + error.msg)
                except Exception as error:
                    print("Caught Exception : " + str(error))

    def vm_poweron(self, start, end, bname):
        vmnames = []
        for i in range(start, end + 1):
            vmnames.append(bname + str(i))
        # for vm_name in vmnames:
        #     print(vm_name)
        content = self.client.RetrieveContent()
        for child in content.rootFolder.childEntity:
            if hasattr(child, 'vmFolder'):
                datacenter = child
                vmfolder = datacenter.vmFolder
                vmlist = vmfolder.childEntity
                try:
                    tasks = [vm.PowerOn() for vm in vmlist if vm.summary.config.name in vmnames]
                    time.sleep(5)
                    self.wait_for_tasks(tasks)
                    print("Virtual Machines have been powered on successfully")
                except vmodl.MethodFault as error:
                    print("Caught vmodl fault : " + error.msg)
                except Exception as error:
                    print("Caught Exception : " + str(error))
    def VmManage_99_99(self):
        start99, end99 = 241, 250
        bname99 = "sslvpntest-99."
        self.vm_poweroff(start99,end99,bname99)
        time.sleep(20)
        self.vm_poweron(start99,end99,bname99)
    def VmManage_99_100(self):
        start100, end100 = 2, 52
        bname100 = "sslvpn-99."
        self.vm_poweroff(start100,end100,bname100)
        time.sleep(20)
        self.vm_poweron(start100,end100,bname100)
    def VmManage_99_200(self):
        start200, end200 = 140,149
        bname200 = "sslvpn-99."
        self.vm_poweroff(start200,end200,bname200)
        time.sleep(20)
        self.vm_poweron(start200,end200,bname200)

if __name__=="__main__":
    host99, user99, pwd99 = "10.7.99.99", "root", "123qwe!@#QWE"
    v99=Vcenter(host99,user99,pwd99)
    v99.VmManage_99_99()
    # time.sleep(20)
    # host100, user100, pwd100 = "10.7.99.100", "root", "sonicwall2010"
    # v100=Vcenter(host100,user100,pwd100)
    # v100.VmManage_99_100()
    # time.sleep(20)
    # host200, user200, pwd200 = "10.7.99.200", "root", "sonicwall2010"
    # v200=Vcenter(host200,user200,pwd200)
    # v200.VmManage_99_200()

