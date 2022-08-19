#!/usr/bin/bash
echo "sending files:" > test.log
n=`cat demoIplist.txt | wc -l` #分发的ip数量
echo $n
fileName=DDoS.py #分发文件名
echo "file:$fileName"
for i in `seq $n`
    do
#passwd=`cat demoPassword.txt | head -$i | tail -1`
        passwd='sonicwall'
        ip=`cat demoIplist.txt | head -$i | tail -1`
        echo $ip
##自动交互
        expect <<EOF
        spawn scp $fileName sonicwall@$ip:/home/sonicwall/
        expect "yes/no" {send "yes\n;exp_untinue"}
        expect "password" {send "$passwd\n"}
        expect eof
EOF
        if [ $? -eq 0 ]
        then
            echo "$ip：success" >>demoScpLog.log
            echo "$ip：success"
        else
            echo "$ip:fail" >>demoScpLog.log
            echo "$ip：fail"
        fi
    done
echo "completed!!!"
