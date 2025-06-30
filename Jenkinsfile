pipeline {
    agent any
    
    environment {
        DOCKER_HUB_REPO = 'your-dockerhub-username/python-file-server'
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
        BUILD_VERSION = "${BUILD_NUMBER}-${GIT_COMMIT[0..7]}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    python3 -m py_compile app.py
                    echo "Python syntax check passed"
                '''
            }
        }
        
        stage('Build & Push Docker Image') {
            steps {
                script {
                    def image = docker.build("${DOCKER_HUB_REPO}:${BUILD_VERSION}")
                    
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        image.push()
                        image.push("latest")
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                        # Update image in deployment
                        sed -i "s|your-dockerhub-username/python-file-server:latest|${DOCKER_HUB_REPO}:${BUILD_VERSION}|g" k8s-all.yaml
                        
                        # Apply all Kubernetes resources
                        kubectl apply -f k8s-all.yaml
                        
                        # Wait for rollout
                        kubectl rollout status deployment/file-server -n file-server --timeout=300s
                        
                        # Verify deployment
                        kubectl get pods -n file-server
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                sh '''
                    sleep 30
                    kubectl exec -n file-server deployment/file-server -- curl -f http://localhost:5000/health
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed!"
        }
    }
}
