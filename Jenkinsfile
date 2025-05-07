pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'rranzan2001/flask'
        // Use timestamped versioning instead of 'latest'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}-${new Date().format('yyyyMMdd-HHmmss')}"
        PREVIOUS_IMAGE_TAG = 'previous'
        // Use credential binding for secrets
        DOCKERHUB_CREDENTIALS = credentials('docker-hub-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Security Scan - SAST') {
            steps {
                script {
                    try {
                        // Run Bandit for Python SAST scanning
                        sh '''
                            pip install bandit
                            bandit -r . -f json -o bandit-results.json || true
                        '''
                    } catch (Exception e) {
                        echo "SAST scan warning: ${e.message}"
                        // Don't fail the build, but flag it
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }

        stage('Dependency Check') {
            steps {
                script {
                    try {
                        // Check dependencies for vulnerabilities
                        sh '''
                            pip install safety
                            safety check -r pyreq.txt --json > safety-results.json || true
                        '''
                    } catch (Exception e) {
                        echo "Dependency check warning: ${e.message}"
                        // Don't fail the build, but flag it
                        currentBuild.result = 'UNSTABLE'
                    }
                }
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
                            export PYTHONPATH=${WORKSPACE}
                            export FLASK_ENV=testing
                            python -m pip install --no-cache-dir -r pyreq.txt

                            echo "Running tests with coverage..."
                            python -m pytest test_app.py -v --capture=no --disable-warnings --cov=app --cov-report=xml:test-results/coverage.xml
                        '''
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error "Tests failed: ${e.message}"
                    }
                }
            }
            post {
                always {
                    // Publish test and coverage results
                    junit allowEmptyResults: true, testResults: 'test-results/*.xml'
                    publishCoverage adapters: [cobertura('test-results/coverage.xml')]
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
                            docker pull ${DOCKER_IMAGE_NAME}:${PREVIOUS_IMAGE_TAG} || true
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
                        // Build with specific tag instead of latest
                        sh """
                            docker build -t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} .
                            docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:latest
                        """
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error "Build failed: ${e.message}"
                    }
                }
            }
        }

        stage('Container Security Scan') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    try {
                        // Scan for container vulnerabilities using Trivy
                        sh """
                            docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v \$(pwd):/root aquasec/trivy:latest image --format json --output trivy-results.json ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} || true
                        """
                    } catch (Exception e) {
                        echo "Container scan warning: ${e.message}"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }

        stage('Push to Registry') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                script {
                    try {
                        // Login to Docker Hub securely
                        sh """
                            echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin
                            docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                            docker push ${DOCKER_IMAGE_NAME}:latest
                            docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:${PREVIOUS_IMAGE_TAG}
                            docker push ${DOCKER_IMAGE_NAME}:${PREVIOUS_IMAGE_TAG}
                        """
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error "Push failed: ${e.message}"
                    } finally {
                        // Always logout to prevent credential leakage
                        sh 'docker logout'
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
                        // Update the deploy.yml with the new image tag
                        sh """
                            sed -i 's|image: rranzan2001/flask:latest|image: rranzan2001/flask:${DOCKER_IMAGE_TAG}|g' deploy.yml
                            docker exec -u root ansible ansible-playbook /root/deploy.yml
                        """

                        // Health check to verify deployment
                        sh """
                            # Wait for container to be ready
                            sleep 10
                            # Check health endpoint
                            curl -f http://localhost:8001/health || exit 1
                        """
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        echo "Deployment failed: ${e.message}. Rolling back..."

                        // Enhanced rollback strategy
                        sh """
                            sed -i 's|image: rranzan2001/flask:${DOCKER_IMAGE_TAG}|image: rranzan2001/flask:${PREVIOUS_IMAGE_TAG}|g' deploy.yml
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
            // Archive artifacts and reports
            archiveArtifacts artifacts: '*-results.json', allowEmptyArchive: true
        }
        always {
            // Clean sensitive data
            sh '''
                docker rmi $(docker images -q ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}) || true
                rm -f trivy-results.json safety-results.json bandit-results.json || true
            '''
            // Clean workspace using available commands
            deleteDir()
        }
    }
}
