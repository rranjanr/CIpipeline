pipeline{
agent any

environment {
    DOCKER_IMAGE_NAME = 'apurwasingh/flask'
    DOCKER_IMAGE_TAG = 'latest'
}

stages{
    stage('Checkout'){
        steps {
            checkout scm
        }
    }
    stage('Build'){
        steps{
            script{
                docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}").push()
                }
            }
        }
    }
    stage('Deploy'){
        steps{
            script{
                sh "docker exec -u root ansible ansible-playbook /root/deploy.yml"
            }
        }
    }
}

 }
