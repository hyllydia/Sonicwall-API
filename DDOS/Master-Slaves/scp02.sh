#!/usr/bin/bash
echo "sending files:" > test.log
#n=`cat demoIplist.txt | wc -l` #分发的ip数量
n=5
echo $n
m=71
fileName=DDOS.py #分发文件名
echo "file:$fileName"
for i in `seq $n`
    do
        #passwd=`cat demoPassword.txt | head -$i | tail -1`
        passwd='sonicwall'
				#ip=`cat demoIplist.txt |head -$i | tail -1`
				#这里的问题：读到的ip地址后多加了一个换行符“ ”， 放在scp命令中就报错
        #ip=`cat demoIplist.txt |awk 'NR==$i{print \\\$0}'`
				#这里的问题：该命令在shell脚本中不起作用
        ip=10.7.3.$m
        echo $ip
##自动交互
        expect <<EOF
        spawn scp $fileName sonicwall@$ip:/home/sonicwall/
        expect "(yes/no)?" {send "yes\n;exp_untinue"}
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
        let m++
    done
echo "completed!!!"