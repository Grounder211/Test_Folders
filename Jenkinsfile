pipeline {
    agent any

    environment {
        IMAGE_NAME = "server-app"
        GHCR_REPO = "ghcr.io/grounder211/${IMAGE_NAME}"
        DOCKER_TAG = "${GHCR_REPO}:latest"
        K8S_YAML = "deployment.yaml"
        DEPLOY_NAMESPACE = "default"
    }

    options {
        disableConcurrentBuilds()
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Grounder211/Test_Folders.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_TAG .'
            }
        }

        stage('Login to GHCR') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'ghcr-creds', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                    sh 'echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USER --password-stdin'
                }
            }
        }

        stage('Push to GHCR') {
            steps {
                sh 'docker push $DOCKER_TAG'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh """
                kubectl apply -f $K8S_YAML --namespace=$DEPLOY_NAMESPACE
                kubectl rollout status deployment/server-deployment --namespace=$DEPLOY_NAMESPACE
                """
            }
        }
    }

    post {
        success {
            echo "✅ Deployment successful!"
        }
        failure {
            echo "❌ Deployment failed!"
        }
    }
}
