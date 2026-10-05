# Production Server Automation Platform

![AWS](https://img.shields.io/badge/AWS-Cloud-orange?logo=amazonaws)
![Terraform](https://img.shields.io/badge/Terraform-IaC-7B42BC?logo=terraform)
![Ansible](https://img.shields.io/badge/Ansible-Automation-black?logo=ansible)
![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?logo=docker)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?logo=githubactions)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?logo=nginx)
![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql)

A production-style AWS server provisioning, configuration management, and application deployment platform built with Terraform, Ansible, Docker, AWS Systems Manager, and GitHub Actions.

The project demonstrates how to provision AWS infrastructure with Infrastructure as Code, automatically configure an application server with Ansible, deploy a containerized application, and implement secure CI/CD using GitHub Actions with AWS OIDC authentication.

---

## 🚀 Project Overview

This project automates the complete lifecycle of a production-style application server.

The platform provisions AWS infrastructure with Terraform, configures the server with Ansible, runs the TaskFlow application using Docker Compose, exposes the application through Nginx, and provides automated deployments through GitHub Actions and AWS Systems Manager.

### Deployment Flow

    Developer
        │
        │ git push
        ▼
    GitHub Repository
        │
        ▼
    GitHub Actions
        │
        ├── Terraform validation
        ├── Ansible validation
        └── AWS authentication using OIDC
                │
                ▼
            AWS IAM Role
                │
                ▼
        AWS Systems Manager
                │
                ▼
          Application EC2
                │
           ┌────┴────┐
           │         │
         Nginx   Docker Compose
                     │
               ┌─────┴─────┐
               │           │
            TaskFlow   PostgreSQL
               API

---

## 🏗️ Architecture

    ┌──────────────────────┐
    │       GitHub         │
    │   Source Repository  │
    └──────────┬───────────┘
               │
        Git Push / CI
               │
               ▼
    ┌──────────────────────┐
    │   GitHub Actions     │
    │        CI/CD         │
    └──────────┬───────────┘
               │
        OIDC Authentication
               │
               ▼
    ┌──────────────────────┐
    │      AWS IAM         │
    │ GitHub Actions Role  │
    └──────────┬───────────┘
               │
        AWS Systems Manager
               │
               ▼
    ┌────────────────────────────────────────┐
    │              AWS VPC                   │
    │                                        │
    │   ┌────────────────────────────────┐   │
    │   │         Application EC2        │   │
    │   │                                │   │
    │   │       ┌──────────────┐         │   │
    │   │       │    Nginx     │ :80    │   │
    │   │       └──────┬───────┘         │   │
    │   │              │                 │   │
    │   │              ▼                 │   │
    │   │       ┌──────────────┐         │   │
    │   │       │ TaskFlow API │         │   │
    │   │       │    :5000     │         │   │
    │   │       └──────┬───────┘         │   │
    │   │              │                 │   │
    │   │              ▼                 │   │
    │   │       ┌──────────────┐         │   │
    │   │       │ PostgreSQL   │         │   │
    │   │       │     :5432    │         │   │
    │   │       └──────────────┘         │   │
    │   └────────────────────────────────┘   │
    └────────────────────────────────────────┘

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Cloud | AWS |
| Infrastructure as Code | Terraform |
| Configuration Management | Ansible |
| Compute | Amazon EC2 |
| Networking | Amazon VPC |
| Containerization | Docker |
| Application Orchestration | Docker Compose |
| Reverse Proxy | Nginx |
| Application | Python / Flask |
| Database | PostgreSQL |
| CI/CD | GitHub Actions |
| Authentication | GitHub OIDC + AWS IAM |
| Remote Management | AWS Systems Manager |
| Version Control | Git / GitHub |

---

## 📦 TaskFlow Application

TaskFlow is a lightweight Flask-based task management API used as the application workload for this infrastructure automation project.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application information |
| GET | `/health` | Health check |
| GET | `/api/tasks` | List tasks |
| POST | `/api/tasks` | Create task |
| PUT | `/api/tasks/<id>` | Update task |
| DELETE | `/api/tasks/<id>` | Delete task |

### Application Architecture

    Nginx :80
        │
        ▼
    TaskFlow Flask API :5000
        │
        ▼
    PostgreSQL :5432

The Flask API is bound only to localhost:

    127.0.0.1:5000

Therefore, the application port is not directly exposed to the Internet.

---

## 🏗️ Terraform Infrastructure

Terraform provisions the AWS infrastructure required to run TaskFlow.

### Resources

- VPC
- Public subnet
- Internet Gateway
- Route table
- Security group
- EC2 instance
- IAM role
- IAM instance profile
- AWS Systems Manager permissions
- GitHub Actions IAM role
- GitHub OIDC trust relationship

### Network

    VPC
    10.50.0.0/16
    │
    └── Public Subnet
        10.50.1.0/24
        │
        └── Application EC2

### Security Group

| Port | Purpose | Access |
|---|---|---|
| 80 | HTTP / Nginx | Public |
| 22 | SSH administration | Restricted trusted source |
| 5000 | Flask API | Not publicly exposed |
| 5432 | PostgreSQL | Not publicly exposed |

The application architecture intentionally exposes only Nginx publicly.

---

## ⚙️ Ansible Configuration Management

Ansible configures the application server after Terraform provisions the infrastructure.

### Configuration Flow

    Ansible
       │
       ├── Common system configuration
       │
       ├── Docker installation
       │
       ├── TaskFlow application deployment
       │
       └── Nginx configuration

### Ansible Roles

    ansible/
    ├── inventory/
    ├── group_vars/
    ├── playbooks/
    │   └── site.yml
    └── roles/
        ├── common/
        ├── docker/
        ├── application/
        └── nginx/

The project uses AWS EC2 dynamic inventory based on resource tags, avoiding hardcoded application-server IP addresses.

---

## 🔎 Dynamic AWS Inventory

Ansible discovers the application server automatically using AWS tags.

Example tags:

    Project = production-server-automation
    Role    = application-server

This allows a newly created application EC2 instance to be automatically discovered by Ansible without manually changing an IP address.

---

## 🔐 Security

Security was treated as a core part of the project.

### GitHub OIDC

GitHub Actions does not store long-lived AWS access keys.

Instead:

    GitHub Actions
          │
          │ OIDC token
          ▼
       AWS IAM
          │
          ▼
    Temporary AWS credentials

The IAM role trust policy restricts access to the specific GitHub repository and `main` branch.

### AWS Systems Manager

The deployment process uses AWS Systems Manager rather than requiring GitHub Actions to connect directly to the EC2 instance over SSH.

    GitHub Actions
          │
          ▼
    AWS Systems Manager
          │
          ▼
    Application EC2

### Application Security

- PostgreSQL is not Internet-facing.
- Flask port `5000` is not Internet-facing.
- Nginx is the public application entry point.
- SSH is restricted rather than exposed globally.
- GitHub Actions uses short-lived OIDC credentials.
- EC2 uses an IAM instance profile for Systems Manager access.

---

## 🔄 CI/CD Pipeline

Every push to `main` can trigger the deployment workflow.

    Developer
       │
       │ git push
       ▼
    GitHub
       │
       ▼
    GitHub Actions
       │
       ├── Terraform format validation
       ├── Terraform initialization
       ├── Terraform validation
       ├── Ansible syntax validation
       │
       ▼
    AWS OIDC Authentication
       │
       ▼
    AWS IAM Role
       │
       ▼
    Discover Application EC2
       │
       ▼
    AWS Systems Manager
       │
       ├── Update application repository
       ├── Rebuild Docker image
       ├── Start Docker Compose services
       └── Reload Nginx
       │
       ▼
    Application Health Check
       │
       ▼
    ✅ Deployment Successful

---

## 🧪 Deployment Validation

The deployment was validated through multiple layers.

### Infrastructure

- Terraform plan/apply
- VPC and subnet creation
- EC2 provisioning
- Security group validation
- IAM configuration
- SSM connectivity

### Configuration

- Ansible syntax validation
- Ansible deployment
- Dynamic inventory discovery
- Docker installation
- Nginx configuration
- Application deployment

### Application

Health endpoint:

    GET /health

Example response:

    {
      "service": "taskflow-api",
      "status": "healthy"
    }

### Database

PostgreSQL container health was verified through Docker Compose.

### CRUD

The TaskFlow API was tested for:

- Create task
- Read tasks
- Update task
- Delete task

---

## 📁 Project Structure

    production-server-automation/
    │
    ├── app/
    │   ├── app.py
    │   ├── models/
    │   ├── routes/
    │   ├── Dockerfile
    │   ├── docker-compose.yml
    │   ├── requirements.txt
    │   └── .env.example
    │
    ├── terraform/
    │   ├── main.tf
    │   ├── variables.tf
    │   ├── outputs.tf
    │   ├── iam.tf
    │   ├── github-actions.tf
    │   └── ...
    │
    ├── ansible/
    │   ├── ansible.cfg
    │   ├── inventory/
    │   │   └── aws_ec2.yml
    │   ├── group_vars/
    │   │   └── all.yml
    │   ├── playbooks/
    │   │   └── site.yml
    │   └── roles/
    │       ├── common/
    │       ├── docker/
    │       ├── application/
    │       └── nginx/
    │
    ├── .github/
    │   └── workflows/
    │       └── deploy.yml
    │
    ├── docs/
    │
    ├── .gitignore
    └── README.md

---

## 🚀 Deployment

### Provision Infrastructure

    cd terraform

    terraform init

    terraform plan \
      -var="allowed_ssh_cidr=<TRUSTED_IP>/32" \
      -var="key_name=microservice-key"

    terraform apply \
      -var="allowed_ssh_cidr=<TRUSTED_IP>/32" \
      -var="key_name=microservice-key"

### Configure Server with Ansible

    cd ../ansible

    ansible-inventory --graph

    ansible all -m ping

    ansible-playbook playbooks/site.yml

### Verify Application

    curl http://<PUBLIC_IP>/health

---

## 🔧 Configuration Management

The server is designed to be reproducible.

A new application EC2 instance can be provisioned by Terraform and automatically discovered by Ansible using AWS tags.

The configuration process installs and configures:

    Ubuntu
      ↓
    Docker
      ↓
    TaskFlow
      ↓
    PostgreSQL
      ↓
    Nginx

This eliminates dependency on manually configured servers.

---

## 📊 DevOps Concepts Demonstrated

This project demonstrates practical experience with:

- Infrastructure as Code
- Configuration Management
- AWS networking
- EC2 provisioning
- IAM
- GitHub OIDC
- Secure CI/CD
- AWS Systems Manager
- Dynamic inventory
- Docker
- Docker Compose
- Nginx reverse proxy
- Flask API deployment
- PostgreSQL
- Infrastructure reproducibility
- Security hardening
- Automated deployment
- Health checks
- Git-based deployments

---

## 💡 Lessons Learned

### Infrastructure as Code

Infrastructure should be reproducible through code rather than relying on manually configured servers.

### Dynamic Discovery

Using AWS dynamic inventory prevents infrastructure automation from depending on hardcoded IP addresses.

### Secure CI/CD

OIDC provides a safer alternative to storing long-lived AWS access keys in GitHub.

### Remote Management

AWS Systems Manager allows secure server administration and deployment without requiring public SSH access from CI/CD systems.

### Defense in Depth

The application protects internal services by exposing only Nginx publicly while keeping Flask and PostgreSQL private.

---

## 🎯 Project Outcome

The final platform provides an end-to-end Infrastructure as Code, Configuration Management, Containerization, and CI/CD workflow.

    Terraform
       ↓
    AWS Infrastructure
       ↓
    Ansible
       ↓
    Configured Application Server
       ↓
    Docker Compose
       ↓
    TaskFlow + PostgreSQL
       ↓
    Nginx
       ↓
    GitHub Actions
       ↓
    OIDC + AWS Systems Manager
       ↓
    Automated Deployment

The project demonstrates a production-oriented approach to provisioning, configuring, securing, and continuously deploying a containerized application on AWS.

---

## 👨‍💻 Author

**Ashish Thakur**

Cloud & DevOps Engineer | AWS | Terraform | Kubernetes | Docker | CI/CD

GitHub: https://github.com/ashyT-Cloud

---

## ⭐ Future Improvements

- Replace Flask development server with Gunicorn
- HTTPS with ACM and a domain name
- Application Load Balancer
- Auto Scaling
- Remote Terraform state
- AWS Secrets Manager integration
- CloudWatch monitoring
- Centralized logging
- Blue/Green deployment
- Automated rollback
- Production database architecture
- Multi-environment deployment
