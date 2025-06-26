pipeline {
    agent any

    environment {
        IMAGE_NAME = 'neeraj010702/zip-server:latest'
        WORK_DIR = 'C:/Users/Public/Downloads/Server'
        KUBECONFIG='C:/Users/ebalnee/.kube/config'

    }

    stages {
        stage('Prepare Directory') {
            steps {
                bat """
                if not exist "%WORK_DIR%" mkdir "%WORK_DIR%"
                xcopy /Y /E /I . "%WORK_DIR%"
                """
            }
        }

        stage('Docker Build & Push') {
            steps {
                dir("${env.WORK_DIR}") {
                    bat "docker build -t %IMAGE_NAME% ."
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        bat """
                        echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                        docker push %IMAGE_NAME%
                        """
                    }
                }
            }
        }

        stage('K8s Deploy') {
            steps {
                bat "kubectl get nodes"

                bat "kubectl apply -f k8s/deployment.yaml --validate=false"
            }
        }
    }
}
