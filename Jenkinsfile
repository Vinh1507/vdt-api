echo "env.CHANGE_TARGET: ${env.CHANGE_TARGET}"
echo "env.BRANCH_NAME: ${env.BRANCH_NAME}"

pipeline {
    agent any

    environment {
        IMAGE_NAME = 'vinhbh/vdt_api'
        VDT_API_DOCKERFILE_PATH = './vdt_api'
        VDT_API_DOCKER_COMPOSE_FILE_PATH = './vdt_api'
        DATABASE_NAME = 'vdt_db'
        DATABASE_USER = 'vinhbh'
        DATABASE_PASSWORD = '123456789'
        DATABASE_HOST = '192.168.144.143'
        DATABASE_PORT = 31495
        DOCKER_HUB_CREDENTIALS = 'dockerhub_vinhbh'
        GITHUB_CREDENTIALS = 'github-token-v3'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Clone code from branch ${env.BRANCH_NAME}"
                    git branch: env.BRANCH_NAME, url: 'https://github.com/Vinh1507/vdt-api'
                }
                script {
                    def tagVersion = sh(script: 'git describe --tags --abbrev=0', returnStdout: true).trim()
                    env.TAG_NAME = tagVersion
                    echo "Tag version: ${env.TAG_NAME}"
                }
            }
        }
        stage('Build Image') {
            steps {
                script {
                    echo "Image version: ${env.IMAGE_NAME}:${env.TAG_NAME}"
                    sh "docker build -t ${env.IMAGE_NAME}:${env.TAG_NAME} ${VDT_API_DOCKERFILE_PATH}"
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image("${env.IMAGE_NAME}:${env.TAG_NAME}").inside("-e DATABASE_NAME=${DATABASE_NAME} -e DATABASE_USER=${DATABASE_USER} -e DATABASE_PASSWORD=${DATABASE_PASSWORD} -e DATABASE_HOST=${DATABASE_HOST} -e DATABASE_PORT=${DATABASE_PORT}") {
                        sh '''
                        cd /app
                        python manage.py test -v 2
                        '''
                    }
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                // Login to Docker Hub
                withCredentials([usernamePassword(credentialsId: env.DOCKER_HUB_CREDENTIALS, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                }
                // Push Docker image to Docker Hub
                sh "docker push ${env.IMAGE_NAME}:${env.TAG_NAME}"
            }
        }
        stage('Clone Repo Config') {
            steps {
                echo "Clone code from branch ${env.BRANCH_NAME}"
                git branch: env.BRANCH_NAME , credentialsId: env.GITHUB_CREDENTIALS, url: 'https://github.com/Vinh1507/vdt-api-config'
            }
        }
        stage('Modify file helm values') {
            steps {
                script {
                    sh "sed -i 's/^  tag.*/  tag: \"${env.TAG_NAME}\"/' helm-values/values-prod.yaml"
                }
            }
        }
        stage('Push changes to config repo') {
            steps {
                sh 'git add .'
                sh 'git commit -m "Update helm values with new image version"'
                sh 'git config --global user.email "hoangvinh1577@gmail.com"'
                sh 'git config --global user.name "VinhBh"'
                withCredentials([gitUsernamePassword(credentialsId: env.GITHUB_CREDENTIALS, gitToolName: 'Default')]) {
                    sh "git push -u origin main"
                }
            }
            
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'All tests passed!'
        }
        failure {
            echo 'Some tests failed. Please check the output above.'
        }
    }
}
