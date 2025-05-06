pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'rranzan2001/flask'
        DOCKER_IMAGE_TAG = 'latest'
        PREVIOUS_IMAGE_TAG = 'previous'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                script {
                    try {
                        // Create and enter Python virtual environment
                        sh '''
                            python -m venv venv
                            . venv/bin/activate
                            pip install -r pyreq.txt
                            python -m pytest test_app.py --junitxml=test-results/junit.xml
                        '''
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error "Tests failed: ${e.message}"
                    }
                }
            }
        }

        stage('Backup Current Image') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    try {
                        // Tag current production image as 'previous' for backup
                        sh """
                            docker pull ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} || true
                            docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:${PREVIOUS_IMAGE_TAG} || true
                        """
                    } catch (Exception e) {
                        echo "No previous image to backup: ${e.message}"
                    }
                }
            }
        }

        stage('Build') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    try {
                        docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                        docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                            docker.image("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}").push()
                        }
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        // Restore previous image tag if build fails
                        sh """
                            docker tag ${DOCKER_IMAGE_NAME}:${PREVIOUS_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} || true
                        """
                        error "Build/Push failed: ${e.message}"
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    try {
                        sh "docker exec -u root ansible ansible-playbook /root/deploy.yml"
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        // If deployment fails, rollback to previous version
                        sh """
                            docker tag ${DOCKER_IMAGE_NAME}:${PREVIOUS_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                            docker exec -u root ansible ansible-playbook /root/deploy.yml
                        """
                        error "Deployment failed and rolled back: ${e.message}"
                    }
                }
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed! Previous version will remain active.'
        }
        success {
            echo 'Pipeline completed successfully! New version is deployed.'
        }
    }
}
