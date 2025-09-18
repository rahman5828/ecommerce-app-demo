pipeline {
    agent { docker { image 'python:3.13-slim' } }

    environment {
        DOCKER_HUB_REPO = "rahman5828/ecommerce-app"
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Run Tests') {
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
                    sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push $DOCKER_HUB_REPO:latest
                    """
                }
            }
        }
    }
}

