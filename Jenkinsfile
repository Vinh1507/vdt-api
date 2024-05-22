pipeline {
    agent any

    environment {
        IMAGE_NAME = 'vinhbh/vdt-api'
        TAG_NAME = '3.0'
        VDT_API_DOCKERFILE_PATH = './vdt_api'
        VDT_API_DOCKER_COMPOSE_FILE_PATH = './vdt_api'
        DOCKER_IMAGE = "${IMAGE_NAME}:${TAG_NAME}"
    }

    stages {
        stage('Check PR Target') {
            when {
                expression {
                    // Kiểm tra nếu đây là pull request
                    if (env.CHANGE_TARGET) {
                        // Lấy thông tin nhánh mục tiêu của pull request
                        def prTargetBranch = env.CHANGE_TARGET
                        echo "Pull Request target branch: ${prTargetBranch}"
                        // Chỉ chạy nếu nhánh mục tiêu là 'main'
                        return prTargetBranch == 'main'
                    } else {
                        // Không phải là pull request, chạy cho bất kỳ nhánh nào
                        echo "Not a pull request 2"
                        return true
                    }
                }
            }
            steps {
                echo "Proceeding with build..."
            }
        }
        stage('Checkout') {
            steps {
                echo "Clone code from branch ${env.BRANCH_NAME}"
                git branch: env.BRANCH_NAME, url: 'https://github.com/Vinh1507/vdt-api'
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
