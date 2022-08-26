import os
try:
    import netifaces
except ImportError as e:
    try:
        os.system('sudo pip3 install netifaces --proxy="http://10.50.128.110:3128"')
        print('netifaces have been installed successfully! ! !')
        import netifaces
    except Exception as e:
        print(f"======netifaces installation failed======\n{e}\n")

def get_ifaces():
    # get the default gateway and nicname
    routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
    routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]

    # list the all interface and select the one to send packets
    ifaces_info = {}

    print("The interfaces of local host are given below : ")

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
    return ifaces_info

if __name__ == '__main__':
    get_ifaces()