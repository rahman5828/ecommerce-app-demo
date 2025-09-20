pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "rahman5828/ecommerce-app"
    }

    stages {
        stage('Checkout') {
            steps {
                // Default SCM checkout
                checkout scm
            }
        }

        stage('Install & Test') {
            agent {
                docker { image 'python:3.11-slim' }
            }
            steps {
                sh '''
                  pip install --no-cache-dir -r requirements.txt
                  pytest --maxfail=1 --disable-warnings -q || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t $DOCKER_HUB_REPO:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds',
                                                  usernameVariable: 'DOCKER_USER',
                                                  passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                      echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                      docker push $DOCKER_HUB_REPO:latest
                    '''
                }
            }
        }

        stage('Deploy to Azure VM') {
            steps {
                sshagent(['azure-vm-ssh']) {
                    sh """
                      ssh -o StrictHostKeyChecking=no azureuser@172.190.253.33 '
                        docker rm -f ecommerce-app || true &&
                        docker pull ${DOCKER_HUB_REPO}:latest &&
                        docker run -d -p 5000:5000 --restart always --name ecommerce-app ${DOCKER_HUB_REPO}:latest
                      '
                    """
                }
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Pipeline failed. Check logs!"
        }
    }
}

