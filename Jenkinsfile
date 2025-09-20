pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "rahman5828/ecommerce-app"
        VM_HOST = "172.190.253.33"      // replace if VM IP changes
        VM_USER = "azureuser"
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/rahman5828/ecommerce-app-demo.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings -q || true'
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds',
                                                  usernameVariable: 'DOCKER_USER',
                                                  passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker build -t $DOCKER_HUB_REPO:latest .
                        docker push $DOCKER_HUB_REPO:latest
                    '''
                }
            }
        }

        stage('Deploy to Azure VM') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'azure-vm-ssh',
                                                  keyFileVariable: 'SSH_KEY',
                                                  usernameVariable: 'SSH_USER')]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no -i $SSH_KEY $SSH_USER@$VM_HOST '
                            docker pull $DOCKER_HUB_REPO:latest &&
                            docker stop ecommerce-app || true &&
                            docker rm ecommerce-app || true &&
                            docker run -d -p 5000:5000 --name ecommerce-app $DOCKER_HUB_REPO:latest
                        '
                    '''
                }
            }
        }
    }
}

