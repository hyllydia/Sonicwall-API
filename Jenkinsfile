#!groovy
pipeline
{
    agent{node{
                label: "yhou-server"
                customerworkspace: "${workspace}"

           }
    }
    options{
            skipDefaultCheckout()
    }
    stages{
          stage("git pull source code"){
                steps{
                echo "updated code"
                sh'''
                sudo rm -rf $workspace/workspace/yhou_test
                '''
          dir('workspace/yhou_test'){
                git credentialsId: 'gitlab-yhou2022', url: 'http://10.7.1.41/yhou/yhou-python-scritps.git'
                }
                }
          }

}
}


