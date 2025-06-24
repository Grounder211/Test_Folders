pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/Grounder211/Test_Folders.git'
        REPO_DIR = 'DroneRepo'
        TARGET_DIR = 'C:/Users/ebalnee/OneDrive - Ericsson/Desktop/RepoDump'
    }

    stages {
        stage('Clone if Missing') {
            steps {
                script {
                    bat """
                    if not exist "%REPO_DIR%\\.git" (
                        git clone %REPO_URL% %REPO_DIR%
                    )
                    """
                }
            }
        }

        stage('Pull Latest Changes') {
            steps {
                dir("${env.REPO_DIR}") {
                    bat "git pull"
                }
            }
        }

        stage('Copy New/Changed Files Only') {
            steps {
                bat """
                xcopy "%REPO_DIR%\\*" "%TARGET_DIR%\\" /D /E /Y /I
                """
            }
        }

        stage('Done') {
            steps {
                echo "Incremental sync complete — new/changed files copied to ${env.TARGET_DIR}"
            }
        }
    }
}
