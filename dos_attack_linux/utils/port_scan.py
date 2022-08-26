import os
import platform
import subprocess

# install nmap
nmap_v = os.system('nmap -V')
plat_info = platform.platform()
if nmap_v != 0:
    try:
        if 'Ubuntu' in plat_info:
            os.system('apt-get -o Acquire::http::proxy="http://10.50.128.110:3128/" install nmap')
        elif 'centos' in plat_info:
            res = subprocess.Popen('cat /etc/yum.conf', shell=True, stdout=subprocess.PIPE)
            r = res.communicate()
            if 'proxy=http://10.50.128.110:3128' not in r[0].decode('utf-8'):
                os.system('echo "proxy=http://10.50.128.110:3128" >> /etc/yum.conf')
            os.system('yum install -y nmap')
    except Exception as e:
        print(f"======nmap installation failed======\n{e}\n")

# install python3-nmap
try:
    import nmap3
except ImportError:
    try:
        os.system('sudo pip3 install python3-nmap --proxy="http://10.50.128.110:3128"')
        import nmap3
    except Exception as e:
        print(f"======python3-nmap installation failed======\n{e}\n")

def port_scan_tcp(dst_ip):
    tcpPorts = []
    nm = nmap3.NmapScanTechniques()
    result = nm.nmap_tcp_scan(target=dst_ip, args='-p 0-65535')[dst_ip]['ports']
    for i in range(len(result)):
        tcpPorts.append(result[i]['portid'])
    return tcpPorts

if __name__ == "__main__":
    pass