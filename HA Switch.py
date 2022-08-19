#coding:utf-8
"""
Author:Hou Yuling
Time:6/6/2022 10:54 AM
"""
import telnetlib
import datetime
import time


class HA_Switch:
    def __init__(self):
        self.tn=telnetlib.Telnet()
    def switch_ha_mode(self,host,port,admin,password):
        try:
            self.tn.open(host=host,port=port, timeout=2)
            self.tn.read_until(b'login:',timeout=2)
            self.tn.write(('root').encode('ascii')+b'\n')
            self.tn.read_until(b'Password:',timeout=3)
            self.tn.write(("123456").encode('ascii')+b'\n')
            print("***")
            self.tn.read_until(b'User:',timeout=3)
            self.tn.write(b'\n')
            self.tn.write(b'\n')
            command=self.tn.read_some()
            print(command.decode())
            if "User:" in command.decode():
                self.tn.write(b'\n')
                self.tn.write(b'\n')
                print("before admin")
                self.tn.write(admin.encode('ascii') + b'\n')
                self.tn.read_until(b'Password:', timeout=2)
                self.tn.write(password.encode('ascii') + b'\n')
                self.tn.write(b'\n')
                self.tn.read_until(b'>', timeout=2)
            self.tn.write(b'\n')
            #print("**")
            self.tn.write(('config').encode('ascii') + b'\n')
            time.sleep(2)
            command=self.tn.read_very_eager()
            #print(command)
            if '#' in command.decode():
                print('Enter config mode successfully!')
            elif "[no]:" in command.decode():
                self.tn.write(('yes').encode('ascii') + b'\n')
                self.tn.read_until(b'#',timeout=0.5)
                print('Enter config mode successfully!')
            """进入HA"""
            cmd1="high-availability"
            cmd2="force-failover"
            self.tn.write(b'\n')
            self.tn.write(cmd1.encode('ascii')+b"\n")
            self.tn.read_until(b"#",timeout=2)
            self.tn.write(b'\n')
            self.tn.write(cmd2.encode('ascii')+b"\n")
            self.tn.read_until(b'[no]:',timeout=2)
            self.tn.write(('yes').encode('ascii')+b'\n')
            print("HA switch successfully!")
            #command=self.tn.read_very_eager()

            time.sleep(300)

        except Exception as e:
            print("error:{}".format(e))


if __name__=="__main__":
    ha_switch=HA_Switch()
    """sys 5700-1"""
    console_host="10.7.1.103"
    console_port="2010"
    admin="admin"
    password="sonicwall"
    print(datetime.datetime.now())
    for i in range(1,51):
        print("***"+str(i)+"***")
        print(datetime.datetime.now())
        ha_switch.switch_ha_mode(host=console_host,port=console_port,admin=admin,password=password)
        time.sleep(10)
    print(datetime.datetime.now())

