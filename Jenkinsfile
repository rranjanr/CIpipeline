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
            agent {
                docker {
                    image 'python:3.9-slim'
                    args '--init'
                    reuseNode true
                }
            }
            steps {
                script {
                    try {
                        // Create test results directory
                        sh 'mkdir -p test-results'
                        
                        // Install dependencies with specific version pins
                        sh '''
                            echo "Installing dependencies..."
                            python -m pip install --no-cache-dir -r pyreq.txt
                            
                            echo "Running tests..."
                            pytest test_app.py -v --junitxml=test-results/junit.xml --capture=no
                        '''
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error "Tests failed: ${e.message}"
                    }
                }
            }
            post {
                always {
                    junit(
                        allowEmptyResults: true,
                        testResults: 'test-results/junit.xml',
                        skipPublishingChecks: true
                    )
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
        always {
            cleanWs()
        }
    }
}
