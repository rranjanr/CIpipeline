# Secure CI/CD Pipeline with DevSecOps Integration

This project demonstrates a secure CI/CD pipeline with DevSecOps practices integrated throughout the software development lifecycle.

## Project Overview

This is a simple Flask application with a CI/CD pipeline that includes:

- Automated testing
- Security scanning
- Container security
- Dependency vulnerability checking
- Secure deployment
- Robust rollback mechanisms

## Security Features Implemented

### 1. Code Security
- **SAST (Static Application Security Testing)** using Bandit
- **Dependency checking** with Safety
- **Code coverage** reporting to identify untested code

### 2. Container Security
- **Non-root user** execution in Docker
- **Minimal base image** (Python slim)
- **Container scanning** with Trivy
- **Security options** like no-new-privileges
- **Resource limits** to prevent DoS attacks

### 3. CI/CD Security
- **Versioned artifacts** instead of using 'latest' tag
- **Secure credentials management** with Jenkins credentials
- **Comprehensive testing** before deployment
- **Automated rollback** on deployment failure
- **Artifact cleanup** to prevent leaking sensitive data

### 4. Deployment Security
- **Health checks** to verify proper application function
- **Deployment verification** with automated testing
- **Container isolation** with proper networking
- **Proper secret management**

## Application Components

- `app.py` - Simple Flask application with a health endpoint
- `test_app.py` - Test suite with HTML validation
- `Dockerfile` - Secure container configuration
- `Jenkinsfile` - CI/CD pipeline definition with security stages
- `deploy.yml` - Ansible playbook for deployment
- `docker-compose.yml` - Local development environment
- `pyreq.txt` - Python dependencies with secure versions

## CI/CD Pipeline Stages

1. **Checkout** - Fetch source code
2. **Security Scan (SAST)** - Static analysis for vulnerabilities
3. **Dependency Check** - Check for vulnerable dependencies
4. **Test** - Run automated tests with coverage
5. **Backup Current Image** - Preserve current deployment for rollback
6. **Build** - Build Docker image with security best practices
7. **Container Security Scan** - Scan container for vulnerabilities
8. **Push to Registry** - Push versioned image to registry
9. **Deploy** - Deploy with health checks and rollback capability

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Jenkins with appropriate plugins
- Ansible

### Running Locally

```bash
docker-compose up -d
```

Access the application at http://localhost:8001

### Running the Tests

```bash
pip install -r pyreq.txt
pytest test_app.py
```

### CI/CD Pipeline Execution

The pipeline is triggered on code changes and runs all security checks and tests automatically before deployment.

## Security Practices

- Dependencies are kept up-to-date with security patches
- All images are scanned for vulnerabilities
- No passwords or secrets in code (using credential management)
- Non-root execution in containers
- Proper error handling and logging
- Comprehensive health checks

## Improvements Made

- Updated Flask and dependencies to secure versions
- Added health endpoint for monitoring
- Implemented container security best practices
- Added comprehensive security scanning
- Improved rollback mechanisms
- Added proper credential handling
- Implemented resource limits
- Added network isolation
- Enhanced security in ansible-jenkins-windows.yml:
  - Restricted Docker socket access with read-only permissions
  - Added user constraints to prevent containers from running as root
  - Implemented dedicated network isolation
  - Set appropriate resource limits to prevent DoS attacks
  - Added health checks for service monitoring
  - Limited ports to only be accessible from localhost
  - Added security options to prevent privilege escalation
  - Improved volume management with proper named volumes

## Quick Start Guide

For a comprehensive guide on setting up and using this pipeline after cloning the repository, please refer to [instruction.readme.md](instruction.readme.md).

### TL;DR Commands

```bash
# Run the Flask application
docker-compose up -d

# Access the application
# Open http://localhost:8001 in your browser

# Run the tests
docker exec flask pytest test_app.py -v

# Start Jenkins and Ansible (Windows)
docker-compose -f ansible-jenkins-windows.yml up -d

# Start Jenkins and Ansible (Linux/Mac)
docker-compose -f ansible-jenkins-linux-mac.yml up -d

# Get Jenkins initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Access Jenkins
# Open http://localhost:8080 in your browser

# Test Ansible deployment
docker exec ansible ansible-playbook /root/deploy.yml -v
```

## System Requirements

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space
- Internet connection for pulling images

## Common Issues

1. **Unhealthy Container Status**: If the Flask container shows as "unhealthy", check the logs with `docker logs flask`. The most common cause is the health check failing before the application fully starts.

2. **Jenkins Plugin Installation Failures**: If Jenkins plugins fail to install, restart Jenkins with `docker restart jenkins` and try again.

3. **Pipeline Failures**: Check the Jenkins console output for detailed error messages. Most failures occur due to Docker Hub authentication issues or test failures.

4. **Docker Socket Permission Issues**: On Linux, you may need to adjust permissions for the Docker socket with `sudo chmod 666 /var/run/docker.sock`.

## Production Deployment Considerations

This pipeline is primarily designed for demonstration and learning purposes. For production use, consider:

1. Setting up proper SSL/TLS for all services
2. Implementing proper secret management (e.g., HashiCorp Vault)
3. Using dedicated managed Jenkins services
4. Implementing proper backups for all volumes and data
5. Adding comprehensive monitoring and alerting
6. Separating environments (dev/staging/prod)

## License

This project is licensed under the MIT License - see the LICENSE file for details.