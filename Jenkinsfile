echo "env.CHANGE_TARGET: ${env.CHANGE_TARGET}"
echo "env.GIT_BRANCH: ${env.GIT_BRANCH}"
echo "env.BRANCH_NAME: ${env.BRANCH_NAME}"

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
        DATABASE_HOST='192.168.144.135'
        DATABASE_PORT=5432
    }

    stages {
        // stage('Check PR Target') {
        //     when {
        //         expression {
        //             // Kiểm tra nếu đây là pull request
        //             echo "env.CHANGE_TARGET: ${env.CHANGE_TARGET}"
        //             echo "env.GIT_BRANCH: ${env.GIT_BRANCH}"
        //             if (env.CHANGE_TARGET) {
        //                 // Lấy thông tin nhánh mục tiêu của pull request
        //                 def prTargetBranch = env.CHANGE_TARGET
        //                 echo "Pull Request target branch: ${prTargetBranch}"
        //                 // Chỉ chạy nếu nhánh mục tiêu là 'main'
        //                 return prTargetBranch == 'main'
        //             } else {
        //                 // Không phải là pull request, chạy cho bất kỳ nhánh nào
        //                 echo "Not a pull request 2"
        //                 return true
        //             }
        //         }
        //     }
        //     steps {
        //         echo "Proceeding with build..."
        //     }
        // }
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
                    docker.image(env.DOCKER_IMAGE).inside("-e DATABASE_NAME=${DATABASE_NAME} 
                    -e DATABASE_USER=${DATABASE_USER} 
                    -e DATABASE_PASSWORD=${DATABASE_PASSWORD}
                    -e DATABASE_HOST=${DATABASE_HOST}
                    -e DATABASE_PORT=${DATABASE_PORT}") {
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
