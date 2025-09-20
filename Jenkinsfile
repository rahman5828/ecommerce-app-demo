pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "rahman5828/ecommerce-app"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/rahman5828/ecommerce-app-demo.git'
            }
        }

        stage('Install Dependencies') {
            agent {
                docker { image 'python:3.11-slim' }
            }
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Run Tests') {
            agent {
                docker { image 'python:3.11-slim' }
            }
            steps {
                sh 'pytest --maxfail=1 --disable-warnings -q || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_HUB_REPO:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push $DOCKER_HUB_REPO:latest
                    '''
                }
            }
        }

        stage('Deploy to Azure VM') {
            steps {
                sshagent(['azure-vm-ssh']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no azureuser@172.190.253.33 '
                          sudo docker pull rahman5828/ecommerce-app:latest &&
                          sudo docker stop ecommerce-app || true &&
                          sudo docker rm ecommerce-app || true &&
                          sudo docker run -d -p 5000:5000 --name ecommerce-app rahman5828/ecommerce-app:latest
                        '
                    '''
                }
            }
        }
    }
}

