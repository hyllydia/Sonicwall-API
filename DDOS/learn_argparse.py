import argparse
def func():
    parser = argparse.ArgumentParser( description=' python Master.py --file <botnet.file> --target-ip x.x.x.x --target-port xx')
    parser.add_argument('--file',type=str, required=True,help='specify botnet file')
    parser.add_argument('--target-ip', type=str, required=True, help='specify target ip')
    parser.add_argument('--target-port', type=int, required=True, help='specify target port')
    args = parser.parse_args()
    print(type(args))
    target_ip = args.target_ip
    print(target_ip)
    target_port = args.target_port
    print(target_port)
    file = args.file
    print(file)
    with open(file,'r') as f:
        for line in f.readlines():
            line=line.strip("\n")
            host=line.split(":")[0]
            user=line.split(":")[1]
            passwd=line.split(":")[2]
            print(host+"&"+user+"&"+passwd)
if __name__=="__main__":
    func()

