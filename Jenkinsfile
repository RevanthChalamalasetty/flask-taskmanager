
pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID     = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
        AWS_REGION            = 'us-east-1'
        ECR_REPO              = '486336528116.dkr.ecr.us-east-1.amazonaws.com/flask-taskmanager'
        IMAGE_TAG             = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Running pytest...'
                sh '''
                    python3.9 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pytest tests/ -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image with tag: ${BUILD_NUMBER}"
                sh '''
                    docker build -t ${ECR_REPO}:${IMAGE_TAG} .
                    docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_REPO}:latest
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                echo 'Pushing image to AWS ECR...'
                sh '''
                    /usr/local/bin/aws ecr get-login-password \
                        --region ${AWS_REGION} | \
                        docker login \
                        --username AWS \
                        --password-stdin ${ECR_REPO}

                    docker push ${ECR_REPO}:${IMAGE_TAG}
                    docker push ${ECR_REPO}:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to EKS...'
                sh '''
                    /usr/local/bin/kubectl set image deployment/flask-taskmanager \
                        flask-taskmanager=${ECR_REPO}:${IMAGE_TAG} \
                        --record || \
                    /usr/local/bin/kubectl apply -f k8s/deployment.yaml

                    /usr/local/bin/kubectl apply -f k8s/service.yaml

                    /usr/local/bin/kubectl rollout status \
                        deployment/flask-taskmanager \
                        --timeout=120s
                '''
            }
        }

        stage('Verify') {
            steps {
                echo 'Verifying deployment...'
                sh '''
                    /usr/local/bin/kubectl get pods
                    /usr/local/bin/kubectl get services
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline succeeded! Flask app deployed to Kubernetes.'
        }
        failure {
            echo '❌ Pipeline failed. Check logs above.'
        }
        always {
            sh 'docker system prune -f || true'
        }
    }
}