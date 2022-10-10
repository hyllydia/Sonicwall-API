###Author:Meng xiangqiao
### Introduction
These scripts can achieve DOS attack by different protocols flood on the linux platform. 
It mainly uses scapy, python3-nmap, netifaces and threading.

#### Notice：Please make sure that Python3 and python3-pip have been installed, and that the pip3 and python3 commands are availabled before running the main scripts.

### Directory Structure
- utils
    - ifaces_util : get network card information of the host 
    - logger_util : define the log handler, format, level
    - port_scan : scan ports of the destination host by nmap
    - thread_util_refactory : define thread functions to send packets 


- log : record the log generated during running the scripts


- dos_attack_tcp_flood : main function of TCP flood.


- dos_attack_udp_flood : main function of UDP flood.


- dos_attack_icmp_flood : main function of ICMP flood.


- dos_attack_mix_flood : TCP、UDP and ICMP packets are sent to the destination host concurrently in a way of infinite 
loop by threading

### Detailed description
- select destination port: 
The dos_attack_tcp_flood and dos_attack_udp_flood can select manual input or generating 
randomly destination port. The destination port generating randomly is that scans ports of the target host and five 
ports are selected from the scan results randomly. Packets are sent to these five ports concurrently.


- select sending packets mode: The dos_attack_tcp_flood, dos_attack_udp_flood and dos_attack_icmp_flood can choose to 
send a certain mount of packets or sending packets in a way of infinite loop. Notice: You can select sending packets mode if you 
choose manual input port. However, you can only send a certain mount of packets when you choose to generate port randomly.


- select source IP mode: Source IP can use local host IP or random IP. 


- select interface: The script can list all interfaces. You need to select the interface used to send packets.