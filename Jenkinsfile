pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = "rahman5828/ecommerce-app"
        CONTAINER_NAME  = "ecommerce-app"
        HOST_PORT       = "5001"
        CONTAINER_PORT  = "5000"
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/rahman5828/ecommerce-app-demo.git'
            }
        }

        stage('Install Dependencies & Run Tests') {
            steps {
                script {
                    docker.image('python:3.11-slim').inside {
                        sh 'pip install --no-cache-dir -r requirements.txt'
                        sh 'pytest --maxfail=1 --disable-warnings -q || true'
                    }
                }
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
                    sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push $DOCKER_HUB_REPO:latest
                    """
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh """
                    # Stop and remove old container if running
                    docker rm -f $CONTAINER_NAME || true
                    
                    # Run new container
                    docker run -d -p $HOST_PORT:$CONTAINER_PORT --restart always --name $CONTAINER_NAME $DOCKER_HUB_REPO:latest
                """
            }
        }
    }
}

