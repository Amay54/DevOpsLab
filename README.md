# DevOps Lab 3: Monitoring, Logging & DevSecOps

A production-grade, enterprise-ready DevOps implementation demonstrating end-to-end Observability, Centralized Logging with the ELK Stack, Metrics Monitoring with Prometheus & Grafana, DevSecOps Security Automation, Feature Flags, and Automated Testing (Load & Selenium).

---

## 📋 Table of Contents
1. [Architecture Overview](#-architecture-overview)
2. [Project Structure](#-project-structure)
3. [Question 1: Centralized Logging (ELK Stack)](#-question-1-centralized-logging-elk-stack)
4. [Question 2: DevSecOps & CI/CD Security](#-question-2-devsecops--cicd-security)
5. [Question 3: Prometheus & Grafana Monitoring](#-question-3-prometheus--grafana-monitoring)
6. [Question 4: Feature Flags & Automated Testing](#-question-4-feature-flags--automated-testing)
7. [Question 5: Comprehensive Final Report](#-question-5-comprehensive-final-report)
8. [Quick Start Guide](#-quick-start-guide)
9. [API Endpoints](#-api-endpoints)

---

## 🏛 Architecture Overview

```
Developer / Code Commit
           │
           ▼
Version Control (GitHub)
           │
           ▼
CI/CD Pipeline (GitHub Actions)
  ├── 1. Dependency Audit (npm audit)
  ├── 2. Unit & Integration Testing (Jest)
  ├── 3. SAST Static Code Analysis (Semgrep)
  ├── 4. Container Vulnerability Scanning (Trivy)
  └── 5. Secure Multi-Stage Image Build
           │
           ▼
Container Orchestration (Docker Compose)
           │
           ▼
Target Application (Node.js Express on :3000)
    ├── Feature Flags (Dark Mode, Dynamic Dashboard)
    ├── Security Middleware (Helmet, CORS, Rate Limit)
    │
    ├── Structured Logs (Winston JSON)
    │       │
    │       ▼
    │   Logstash (:5044/:9600)
    │       │
    │       ▼
    │   Elasticsearch (:9200)
    │       │
    │       ▼
    │   Kibana Dashboard (:5601)
    │
    └── Telemetry Metrics (prom-client on /metrics)
            │
            ▼
        Prometheus (:9090)
            │
            ▼
        Grafana Dashboards (:3001)
```

---

## 📁 Project Structure

```
DevOpsLab/
├── .github/
│   └── workflows/
│       └── devsecops-pipeline.yml         # GitHub Actions DevSecOps workflow
├── .dockerignore                           # Exclusions for clean container builds
├── .env                                    # Feature flags ON configuration
├── .env.flags-off                          # Feature flags OFF configuration
├── .semgrep.yml                            # Custom Semgrep SAST security rules
├── Dockerfile                              # Secure multi-stage, non-root Dockerfile
├── docker-compose.yml                      # Full-stack Docker Compose orchestration
├── docker-compose.elk.yml                  # Dedicated ELK stack Docker Compose
├── docker-compose.monitoring.yml           # Dedicated Monitoring Docker Compose
├── package.json                            # Node.js dependencies and automation scripts
├── src/
│   ├── app.js                              # Express application with logs, metrics, flags
│   ├── logs/
│   │   └── app.log                         # Structured JSON application log file
│   └── __tests__/
│       └── app.test.js                     # Jest + Supertest API test suite
├── Lab3_Submission/
│   ├── generate_reports.py                 # Automated PDF report generator
│   ├── configs/
│   │   ├── elk/
│   │   │   ├── logstash/logstash.conf      # Logstash pipeline configuration
│   │   │   └── generate-logs.js            # Realistic traffic & log generator
│   │   ├── monitoring/
│   │   │   ├── prometheus.yml              # Prometheus scrape configuration
│   │   │   ├── grafana-datasource.yml      # Grafana Prometheus datasource
│   │   │   ├── grafana-dashboard.json      # Grafana pre-built monitoring dashboard
│   │   │   └── grafana-dashboard-provisioning.yml
│   │   └── security/
│   │       ├── run-security-scans.ps1      # PowerShell security scan runner
│   │       └── run-security-scans.sh       # Bash security scan runner
│   ├── testing/
│   │   ├── load/
│   │   │   └── load-test.js                # High-concurrency load testing suite
│   │   └── selenium/
│   │       └── test-app.js                 # Selenium WebDriver automated E2E tests
│   ├── screenshots/                        # Evidence screenshots directory
│   └── reports/                            # Generated university submission PDFs
│       ├── Q1_Centralized_Logging_ELK_Report.pdf
│       ├── Q2_DevSecOps_CICD_Security_Report.pdf
│       ├── Q3_Prometheus_Grafana_Monitoring_Report.pdf
│       ├── Q4_Feature_Flags_Load_Selenium_Testing_Report.pdf
│       └── Q5_Monitoring_Logging_DevSecOps_Final_Report.pdf
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```powershell
npm install
```

### 2. Run the Application Locally
```powershell
# Flags ON mode (default)
npm start

# Flags OFF mode
npm run start:flags-off
```

### 3. Run Automated Tests
```powershell
# Unit & integration tests
npm test

# Load test (30 concurrent VUs, 15 seconds)
npm run test:load

# Automated UI / Selenium test suite
npm run test:selenium
```

### 4. Run DevSecOps Security Scans
```powershell
# Run dependency vulnerability audit
npm run audit

# Run full security suite via PowerShell
powershell -ExecutionPolicy Bypass -File Lab3_Submission/configs/security/run-security-scans.ps1
```

### 5. Launch Infrastructure via Docker Compose
```powershell
# Launch full stack (App + ELK + Prometheus + Grafana)
docker-compose up -d

# Or launch ELK stack only
docker-compose -f docker-compose.elk.yml up -d

# Or launch Monitoring stack only
docker-compose -f docker-compose.monitoring.yml up -d
```

### 6. Generate All 5 PDF Reports
```powershell
python Lab3_Submission/generate_reports.py
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web portal UI (responds with Dark/Light theme based on feature flag) |
| `GET` | `/api/health` | Comprehensive application health status, uptime, and memory |
| `GET` | `/api/users` | Simulated user directory JSON payload |
| `POST` | `/api/login` | Authentication endpoint with credential validation |
| `GET` | `/api/dashboard` | Dynamic dashboard layout (switches between v1 and v2 based on flag) |
| `GET` | `/metrics` | Prometheus telemetry metrics scrape endpoint |
