pipeline {
    agent any

    environment {
        DOCKER_USER = credentials('docker-hub-creds')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/rahman5828/ecommerce-app-demo.git'
            }
        }

        stage('Install & Test') {
            agent {
                docker {
                    image 'python:3.11-slim'
                }
            }
            steps {
                sh '''
                    pip install --no-cache-dir -r requirements.txt
                    pytest --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                        # Build and push latest image
                        docker build -t $DOCKER_USER/ecommerce-app:latest .
                        docker push $DOCKER_USER/ecommerce-app:latest
                    '''
                }
            }
        }

        stage('Deploy to Azure VM') {
            steps {
                sshagent(['azure-vm-ssh']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no azureuser@172.190.253.33 "
                            docker rm -f ecommerce-app || true &&
                            docker pull rahman5828/ecommerce-app:latest &&
                            docker run -d -p 5000:5000 --restart always --name ecommerce-app rahman5828/ecommerce-app:latest
                        "
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline succeeded!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs!"
        }
    }
}

