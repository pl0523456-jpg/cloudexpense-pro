# CloudExpense Pro

A cloud-native expense management platform built using AWS, Docker, CI/CD, and Infrastructure as Code.

## Project Overview

CloudExpense Pro is a SaaS-style expense management application designed to help organizations manage employee expense submissions, approval workflows, and financial reporting.

The goal of this project is to simulate a real-world production application while demonstrating cloud engineering practices including automation, security, scalability, and continuous improvement.

## Business Problem

Many companies still manage employee expenses using emails and spreadsheets, creating problems such as:

- Lost receipts
- Manual approval processes
- Limited visibility
- Difficult reporting
- Poor audit tracking

CloudExpense Pro provides a centralized platform where employees can submit expenses, managers can approve requests, and finance teams can generate reports.

---

# Features

## Employee

- User registration and authentication
- Submit expense claims
- Upload receipts
- Track expense status
- View expense history

## Manager

- Review expense requests
- Approve or reject expenses
- Add comments

## Finance

- View approved expenses
- Generate reports
- Export expense data

## Administrator

- Manage users
- Monitor application activity
- Review audit logs

---

# Technology Stack

## Application

- Python
- Flask
- PostgreSQL

## Cloud Platform

- AWS

Planned AWS services:

- Amazon ECS
- Amazon ECR
- Amazon RDS
- Amazon S3
- Application Load Balancer
- CloudWatch
- IAM
- Secrets Manager
- Route53
- ACM

## DevOps

- Git
- GitHub
- GitHub Actions
- Docker
- CloudFormation

---

# Architecture

The application will follow a cloud-native architecture:

