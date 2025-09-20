pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  // Jenkins credentials ID
        DOCKER_IMAGE = "rahman5828/ecommerce-app:latest"
        VM_USER = "azureuser"
        VM_HOST = "172.190.253.33"   // replace with your Azure VM public IP
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/rahman5828/ecommerce-app-demo.git'
            }
        }

        stage('Run Tests') {
            agent {
                docker {
                    image 'python:3.11-slim'
                }
            }
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest --maxfail=1 --disable-warnings -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $DOCKER_IMAGE ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh "echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin"
                    sh "docker push $DOCKER_IMAGE"
                }
            }
        }

        stage('Deploy to Azure VM') {
            steps {
                script {
                    sshagent (credentials: ['azure-vm-ssh']) {  // Jenkins credentials ID for your SSH private key
                        sh """
                        ssh -o StrictHostKeyChecking=no $VM_USER@$VM_HOST '
                            docker pull $DOCKER_IMAGE &&
                            docker stop ecommerce-app || true &&
                            docker rm ecommerce-app || true &&
                            docker run -d -p 5000:5000 --name ecommerce-app $DOCKER_IMAGE
                        '
                        """
                    }
                }
            }
        }
    }
}

