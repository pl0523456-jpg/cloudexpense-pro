# CloudExpense Pro Architecture

## Overview

CloudExpense Pro is a cloud-native expense management application built on AWS using a containerized architecture.

The application is designed to be:

- Highly Available
- Secure
- Scalable
- Easy to Maintain
- Automated through CI/CD

---

## High-Level Architecture

```text
                Internet
                    │
                    ▼
             Route 53 (DNS)
                    │
                    ▼
        AWS Certificate Manager
              HTTPS / SSL
                    │
                    ▼
      Application Load Balancer
                    │
      ┌─────────────┴─────────────┐
      ▼                           ▼
 ECS Fargate Task          ECS Fargate Task
 Flask Container           Flask Container
      │                           │
      └─────────────┬─────────────┘
                    │
        ┌───────────┴────────────┐
        ▼                        ▼
 Amazon RDS PostgreSQL      Amazon S3
      Database          Receipt Storage
```

---

## AWS Services

| Service | Purpose |
|----------|---------|
| Route 53 | Domain name resolution |
| ACM | SSL certificate management |
| ALB | Load balancing and health checks |
| ECS Fargate | Container hosting |
| ECR | Docker image registry |
| RDS PostgreSQL | Relational database |
| S3 | Receipt storage |
| CloudWatch | Monitoring and logs |
| IAM | Identity and access management |
| Secrets Manager | Secure secret storage |
| SNS | Notifications |
| CloudFormation | Infrastructure as Code |

---

## Security Design

- Private subnets for ECS and RDS
- Least privilege IAM policies
- Secrets stored in AWS Secrets Manager
- HTTPS enforced
- Security Groups restrict traffic
- No database exposed to the public internet

---

## Scalability

Future improvements include:

- Auto Scaling for ECS
- Multi-AZ RDS deployment
- CloudFront for static content
- WAF for application protection
