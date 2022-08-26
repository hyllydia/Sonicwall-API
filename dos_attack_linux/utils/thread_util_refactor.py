from scapy.all import *
from scapy.layers.inet import *
import threading

class packThread():
    def __init__(self, counts, src_ip, dst_ip, iface_name, logger, protocol='', send_pack_type='q', port_list=None):
        self.counts = counts
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.logger = logger
        self.iface_name = iface_name
        self.protocol = protocol
        self.send_pack_type = send_pack_type
        self.port_list = port_list

    def sendPack(self, counts, dport=None):
        pack = None
        num = 0
        protocol = ''
        if self.protocol == 'TCP':
            data = bytes(random.choice([64, 128, 256]) - 54)
            pack = IP(src=self.src_ip, dst=self.dst_ip) / TCP(flags='S', sport=RandShort(), dport=int(dport)) / data
        elif self.protocol == 'UDP':
            data = bytes(random.choice([64, 128, 256]) - 42)
            pack = IP(src=self.src_ip, dst=self.dst_ip) / UDP(sport=RandShort(), dport=int(dport)) / data
        elif self.protocol == 'ICMP':
            data = bytes(random.choice([64, 128, 256]) - 42)
            icmp_type = random.choice([3, 4, 5, 8, 11])
            pack = IP(src=self.src_ip, dst=self.dst_ip) / ICMP(type=icmp_type) / data
        if self.send_pack_type == 'l' or self.send_pack_type == 'L':
            while True:
                send(pack, iface=self.iface_name, count=50000, verbose=0)
                res = send(pack, iface=self.iface_name, verbose=0, return_packets=True)
                p = res[-1].proto
                num += 50001
                if p == 17:
                    protocol = 'UDP'
                elif p == 6:
                    protocol = 'TCP'
                elif p == 1:
                    protocol = 'ICMP'
                self.logger.debug('The %s %s packets have been sent to the port %s of dst host' % (num, protocol, dport))
        elif self.send_pack_type == 'q' or self.send_pack_type == 'Q':
            send(pack, iface=self.iface_name, count=counts, verbose=0)

    def startThread(self, thread_num, dport=None):
        self.logger.debug('Create %s threads to send packets to port %s' % (thread_num, dport))
        threads = []
        count_per_send = self.counts // thread_num
        rest_pack_count = self.counts % thread_num
        for i in range(thread_num):
            if i == thread_num - 1:
                thr = threading.Thread(target=self.sendPack, args=(count_per_send + rest_pack_count, dport))
            else:
                thr = threading.Thread(target=self.sendPack, args=(count_per_send, dport))
            threads.append(thr)
            thr.start()
        return threads

    def joinThread(self, threads):
        for i in threads:
            i.join()

    def sendPackThread(self, dport=None):
        if 10000 <= self.counts <= 50000:
            threads = self.startThread(2, dport)
            self.joinThread(threads)
        elif 50000 < self.counts <= 100000:
            threads = self.startThread(5, dport)
            self.joinThread(threads)
        elif 100000 < self.counts <= 1000000:
            threads = self.startThread(10, dport)
            self.joinThread(threads)
        elif self.counts > 1000000:
            threads = self.startThread(20, dport)
            self.joinThread(threads)
        else:
            if self.counts != 0:
                self.logger.debug('The %s packets are sending to the port %s of dst host' % (self.counts, dport))
            self.sendPack(self.counts, dport)

    def portsThread(self, port_list):
        thread_list = []
        for i in range(len(port_list)):
            thr = threading.Thread(target=self.sendPackThread, args=(port_list[i], ))
            thread_list.append(thr)
            thr.start()
        self.joinThread(thread_list)
        for j in range(len(port_list)):
            self.logger.info('%s packages has been sent to the port %s of %s! ! !' % (self.counts, port_list[j], self.dst_ip))

    def protocolThread(self, tcp_dport, udp_dport):
        thread_list = []
        protocol_list = ['TCP', 'UDP', 'ICMP']
        for i in range(len(protocol_list)):
            self.protocol = protocol_list[i]
            if protocol_list[i] == 'TCP':
                thr = threading.Thread(target=self.sendPack, args=(self.counts, tcp_dport))
            elif protocol_list[i] == 'UDP':
                thr = threading.Thread(target=self.sendPack, args=(self.counts, udp_dport))
            else:
                thr = threading.Thread(target=self.sendPack, args=(self.counts, ))
            thread_list.append(thr)
            thr.start()
        self.joinThread(thread_list)

if __name__ == "__main__":
    pass