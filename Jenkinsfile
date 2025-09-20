pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "rahman5828/ecommerce-app"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/rahman5828/ecommerce-app-demo.git'
            }
        }

        stage('Install Dependencies & Run Tests') {
            steps {
                docker.image('python:3.11-slim').inside {
                    sh '''
                        pip install --no-cache-dir -r requirements.txt
                        pytest --maxfail=1 --disable-warnings -q
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $DOCKER_HUB_REPO:latest .
                '''
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
                withCredentials([sshUserPrivateKey(credentialsId: 'azure-vm-ssh', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no -i $SSH_KEY azureuser@172.190.253.33 << 'EOF'
                            echo ">>> Stopping old container..."
                            sudo docker rm -f ecommerce-app || true

                            echo ">>> Pulling latest image..."
                            sudo docker pull $DOCKER_HUB_REPO:latest

                            echo ">>> Running new container..."
                            sudo docker run -d -p 5000:5000 --name ecommerce-app --restart always $DOCKER_HUB_REPO:latest
                        EOF
                    '''
                }
            }
        }
    }
}

