pipeline {
    agent any

    environment {
        IMAGE_NAME = 'vinhbh/vdt-api'
        TAG_NAME = '1.0'
        VDT_API_DOCKERFILE_PATH = './vdt_api'
        VDT_API_DOCKER_COMPOSE_FILE_PATH = './vdt_api'
        DOCKER_IMAGE = "${IMAGE_NAME}:${TAG_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Clone code from branch main'
                git branch: 'main', url: 'https://github.com/Vinh1507/vdt-api'
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
        stage('Start Services with Docker Compose') {
            steps {
                script {
                    sh '''
                        cd ./vdt_api
                        docker compose up -d
                        '''
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image(DOCKER_IMAGE).inside {
                        sh '''
                        cd /app
                        python manage.py test
                        '''
                    }
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
