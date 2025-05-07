# Complete Guide to Using Your CI/CD Pipeline

This guide provides detailed instructions on how to set up, run, and test your entire CI/CD pipeline after cloning the repository. Follow these steps carefully to ensure a proper deployment of your DevSecOps environment.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Running the Flask Application](#running-the-flask-application)
4. [Setting Up Jenkins](#setting-up-jenkins)
5. [Configuring Ansible](#configuring-ansible)
6. [Testing the Complete Pipeline](#testing-the-complete-pipeline)
7. [Troubleshooting](#troubleshooting)
8. [Security Considerations](#security-considerations)

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- Docker (version 20.10 or above)
- Docker Compose
- Git
- A modern web browser
- Python 3.9+ (for local development)

## Initial Setup

After cloning the repository, follow these steps to set up your environment:

### 1. Navigate to the Repository Directory

```bash
cd /path/to/cloned/repository
```

### 2. Check File Permissions

Ensure deploy.yml and other configuration files have proper permissions:

**On Windows:**
No specific permission changes needed.

**On Linux/Mac:**
```bash
chmod 644 deploy.yml
chmod 644 *.yml
```

### 3. Verify Environment Files

Check that all required files are present:
- Flask application (app.py)
- Tests (test_app.py)
- Docker configuration (Dockerfile, docker-compose.yml)
- CI/CD configuration (Jenkinsfile)
- Deployment configuration (deploy.yml)
- Docker Compose files for CI/CD infrastructure
  - Windows: ansible-jenkins-windows.yml
  - Linux/Mac: ansible-jenkins-linux-mac.yml

## Running the Flask Application

First, let's ensure the Flask application runs correctly:

### 1. Build and Run the Flask Application

```bash
docker-compose up -d
```

This command builds the Flask application using the Dockerfile and starts the container.

### 2. Verify the Application is Running

Open your web browser and navigate to:
- http://localhost:8001

You should see the DevOps Learning Journey page.

### 3. Check the Health Endpoint

The application has a health endpoint at:
- http://localhost:8001/health

You should see a JSON response like: `{"status":"healthy","version":"1.0.0"}`

### 4. Run Tests on the Flask Application

To run tests directly on the container:

```bash
docker exec flask pytest test_app.py -v
```

Alternatively, to run tests locally (requires Python and dependencies):

```bash
pip install -r pyreq.txt
pytest test_app.py -v
```

## Setting Up Jenkins

Now we'll set up the Jenkins CI server:

### 1. Start the Jenkins and Ansible Containers

**For Windows:**
```bash
docker-compose -f ansible-jenkins-windows.yml up -d
```

**For Linux/Mac:**
```bash
docker-compose -f ansible-jenkins-linux-mac.yml up -d
```

### 2. Get the Jenkins Admin Password

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
Make note of this password as you'll need it to unlock Jenkins.

### 3. Access Jenkins

Open your web browser and navigate to:
- http://localhost:8080 (Linux/Mac)
- http://localhost:8080 (Windows - localhost access only)

### 4. Initial Jenkins Configuration

1. Enter the admin password you obtained earlier
2. Install suggested plugins
3. Create an admin user
4. Configure Jenkins URL (default is fine)

### 5. Install Required Jenkins Plugins

Go to "Manage Jenkins" > "Manage Plugins" > "Available" and install:
- Docker Pipeline
- Docker
- Pipeline
- Git Integration
- Credentials Binding
- Blue Ocean (optional but recommended for better UI)

### 6. Configure Jenkins Credentials

1. Go to "Manage Jenkins" > "Manage Credentials"
2. Click on "Jenkins" under "Stores scoped to Jenkins"
3. Click on "Global credentials"
4. Click "Add Credentials"
5. Add your Docker Hub credentials:
   - Kind: Username with password
   - Scope: Global
   - Username: Your Docker Hub username
   - Password: Your Docker Hub password
   - ID: docker-hub-credentials
   - Description: Docker Hub Credentials

### 7. Create a Jenkins Pipeline

1. From the Jenkins dashboard, click "New Item"
2. Enter a name (e.g., "flask-pipeline")
3. Select "Pipeline" and click OK
4. In the Pipeline section, select "Pipeline script from SCM"
5. Select "Git" as the SCM
6. Enter your repository URL
7. Specify the branch (e.g., "*/main" or "*/master")
8. Script Path: "Jenkinsfile"
9. Click "Save"

## Configuring Ansible

The Ansible container is configured to use the deploy.yml playbook:

### 1. Verify Ansible Configuration

The deploy.yml file is mounted into the Ansible container and will be used for deployments.

### 2. Test Ansible Deployment Manually

```bash
docker exec ansible ansible-playbook /root/deploy.yml -v
```

This should deploy or update the Flask application container.

## Testing the Complete Pipeline

Let's test the complete pipeline:

### 1. Make a Change to the Application

Edit app.py to make a small change, for example, update the version number:

```python
@app.route('/health')
def health_check():
    """Endpoint for health monitoring"""
    return jsonify({"status": "healthy", "version": "1.0.1"})
```

### 2. Commit Your Changes (if using Git locally)

```bash
git add app.py
git commit -m "Update app version"
git push
```

### 3. Trigger the Jenkins Pipeline

1. Go to your Jenkins pipeline
2. Click "Build Now"
3. Watch the pipeline execution in the "Stage View" or "Blue Ocean" interface

### 4. Verify Deployment Success

Once the pipeline completes:
1. Check the Flask application at http://localhost:8001
2. Verify the health endpoint shows the updated version

## Troubleshooting

### Container Issues

If containers aren't starting properly:

```bash
# Check container status
docker ps -a

# Check container logs
docker logs flask
docker logs jenkins
docker logs ansible

# Restart containers
docker restart flask
docker restart jenkins
docker restart ansible
```

### Pipeline Failures

1. Check the Jenkins build logs for errors
2. Common issues:
   - Docker Hub authentication failures
   - Test failures
   - Container build errors
   - Deployment issues

### Flask Application Issues

If the Flask application isn't responding:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' flask

# Check application logs
docker logs flask
```

## Security Considerations

Your CI/CD pipeline includes several security enhancements:

1. **Container Security**:
   - Non-root user execution
   - Read-only file system where appropriate
   - Container resource limits
   - No-new-privileges security option

2. **Network Security**:
   - Proper network isolation
   - Limited port exposure (localhost only for Jenkins)

3. **Pipeline Security**:
   - Secure credential handling
   - Dependency vulnerability scanning
   - SAST code scanning
   - Container image scanning

4. **General Security Best Practices**:
   - Regular updates of dependencies
   - Proper error handling
   - Health monitoring
   - Automated testing

## Advanced Usage

### Customizing the Pipeline

To customize the CI/CD pipeline:

1. Edit the Jenkinsfile to add or modify pipeline stages
2. Update deploy.yml to change deployment configurations
3. Modify docker-compose.yml to adjust container settings

### Adding New Tests

To add new tests:

1. Create new test functions in test_app.py
2. Follow the existing pattern for test fixtures and assertions
3. Run the tests locally to verify they pass

### Updating Dependencies

To update dependencies:

1. Edit pyreq.txt with the new package versions
2. Test locally to ensure compatibility
3. Rebuild the container to apply changes:
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```

## Maintenance and Updates

### Regular Maintenance Tasks

1. Update dependencies monthly to ensure security patches
2. Review and update security scanning configurations
3. Check and rotate credentials
4. Test backup and restore procedures

### Monitoring

Monitor your application for:
1. Container health status
2. Application performance
3. Security vulnerabilities
4. Pipeline execution times