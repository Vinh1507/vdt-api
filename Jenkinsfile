echo "env.CHANGE_TARGET: ${env.CHANGE_TARGET}"
echo "env.BRANCH_NAME: ${env.BRANCH_NAME}"

if (env.CHANGE_TARGET && env.CHANGE_TARGET != 'main'){
    echo "Not a Pull Request target branch main"
    return;
}

pipeline {
    agent any

    environment {
        IMAGE_NAME = 'vinhbh/vdt-api'
        TAG_NAME = '3.0'
        VDT_API_DOCKERFILE_PATH = './vdt_api'
        VDT_API_DOCKER_COMPOSE_FILE_PATH = './vdt_api'
        DOCKER_IMAGE = "${IMAGE_NAME}:${TAG_NAME}"
        DATABASE_NAME='vdt_db'
        DATABASE_USER='vinhbh'
        DATABASE_PASSWORD='123456789'
        DATABASE_HOST='192.168.144.129'
        DATABASE_PORT=5432
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Clone code from branch ${env.BRANCH_NAME}"
                git branch: env.BRANCH_NAME, url: 'https://github.com/Vinh1507/vdt-api'
            }
        }
        stage('Build Image') {
            steps {
                script {
                    echo "Image version: ${env.DOCKER_IMAGE}"
                    sh "docker build -t ${env.DOCKER_IMAGE} ${VDT_API_DOCKERFILE_PATH}"
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    docker.image(env.DOCKER_IMAGE).inside("-e DATABASE_NAME=${DATABASE_NAME} -e DATABASE_USER=${DATABASE_USER} -e DATABASE_PASSWORD=${DATABASE_PASSWORD} -e DATABASE_HOST=${DATABASE_HOST} -e DATABASE_PORT=${DATABASE_PORT}") {
                        sh '''
                        cd /app
                        python manage.py test -v 2
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
