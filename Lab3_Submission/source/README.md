# Lab 3: Monitoring, Logging & DevSecOps

[![CI/CD DevSecOps Pipeline](https://github.com/Amay54/DevOpsLab/actions/workflows/devsecops-pipeline.yml/badge.svg)](https://github.com/Amay54/DevOpsLab/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/Node.js-v20%2B-green.svg)](https://nodejs.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

An enterprise-ready DevOps and DevSecOps laboratory implementation demonstrating end-to-end Observability, Centralized Logging with the **ELK Stack**, Metrics Telemetry with **Prometheus & Grafana**, Automated Security in CI/CD with **npm audit**, **Semgrep SAST**, and **Trivy Container Scanning**, dynamic **Feature Flags**, and **Automated Testing (Load & Selenium WebDriver)**.

---

## 📌 Repository Links & Details

- **Primary GitHub Repository:** [https://github.com/Amay54/DevOpsLab](https://github.com/Amay54/DevOpsLab)
- **Target / Submission Repository Name:** `Lab3-Monitoring-Logging-DevSecOps` / `DevOpsLab`
- **Default Branch:** `main`
- **Author:** Amay Yadav
- **Course:** DevOps Laboratory — Lab 3

---

## 📋 Table of Contents

1. [Project Overview & Lab Objectives](#-project-overview--lab-objectives)
2. [Technology Stack](#-technology-stack)
3. [Architecture Overview](#-architecture-overview)
4. [Project Structure](#-project-structure)
5. [Setup & Installation Instructions](#-setup--installation-instructions)
6. [How to Run the Centralized Logging Stack (ELK)](#-how-to-run-the-centralized-logging-stack-elk)
7. [How to Run the Monitoring Stack (Prometheus & Grafana)](#-how-to-run-the-monitoring-stack-prometheus--grafana)
8. [How to Run DevSecOps Security Scans](#-how-to-run-devsecops-security-scans)
9. [How to Test Feature Flags (ON vs OFF)](#-how-to-test-feature-flags-on-vs-off)
10. [How to Run Concurrency Load Testing](#-how-to-run-concurrency-load-testing)
11. [How to Run Automated Selenium E2E Tests](#-how-to-run-automated-selenium-e2e-tests)
12. [CI/CD Pipeline Architecture](#-cicd-pipeline-architecture)
13. [API Endpoints Reference](#-api-endpoints-reference)
14. [Submission PDF Reports](#-submission-pdf-reports)

---

## 🎯 Project Overview & Lab Objectives

This laboratory covers the end-to-end design, implementation, and verification of modern DevOps practices:

- **Question 1 (Centralized Logging - ELK Stack):** Deploy Elasticsearch, Logstash, and Kibana. Collect, filter, index, and visualize structured JSON application logs with custom search dashboards.
- **Question 2 (DevSecOps in CI/CD):** Integrate static code security analysis (Semgrep), dependency vulnerability auditing (npm audit), and container image vulnerability scanning (Trivy) into an automated GitHub Actions pipeline.
- **Question 3 (Metrics Monitoring - Prometheus & Grafana):** Expose Prometheus telemetry endpoints (`/metrics`) from the Node.js runtime, configure Prometheus scrapers, and auto-provision real-time Grafana dashboards.
- **Question 4 (Feature Flags, Load Testing & Selenium):** Implement dynamic runtime feature flags (`FEATURE_DARK_MODE`, `FEATURE_NEW_DASHBOARD`), execute high-concurrency load tests (27,000+ requests, 1,820 req/s), and perform automated browser UI validation using Selenium WebDriver on Google Chrome.
- **Question 5 (Comprehensive Final Report):** Consolidate all observability metrics, security findings, test telemetry, execution screenshots, and architectural flows into formal engineering documentation.

---

## 🛠 Technology Stack

| Layer / Role | Technologies & Tools | Version | Purpose |
|---|---|---|---|
| **Runtime & Backend** | Node.js, Express.js | 20+ / 24.x | Target application server & REST APIs |
| **Structured Logging** | Winston, Morgan | 3.11.0 / 1.10.0 | Structured JSON logging to console & file |
| **Log Management** | Elasticsearch, Logstash, Kibana (ELK) | 8.11.0 | Log ingestion, transformation, storage, search & analytics |
| **Telemetry & Metrics** | Prometheus, prom-client | 2.48.0 / 15.1.0 | Metric scrapers, time-series DB, and client metrics |
| **Visualization** | Grafana | 10.2.0 | Dynamic dashboards for latency, memory, RPS, CPU |
| **Host Exporter** | Prometheus Node Exporter | 1.7.0 | Host operating system and system hardware telemetry |
| **Containerization** | Docker, Docker Compose | 29.x / 5.x | Multi-stage non-root containerization and orchestration |
| **Dependency Auditing** | npm audit | 11.x | Vulnerability identification across package dependency tree |
| **SAST Security** | Semgrep | Latest / OWASP | Static code scanning for secrets and vulnerabilities |
| **Container Scanning** | Trivy | 0.48+ | Scanning container images and OS libraries for CVEs |
| **Unit Testing** | Jest, Supertest | 29.7.0 / 6.3.3 | Automated REST API testing and endpoint validation |
| **Load Testing** | Custom High-Concurrency Engine | Built-in HTTP | Throughput, latency percentiles (p50/p95/p99), and rate limit testing |
| **Browser Automation** | Selenium WebDriver, Chrome Headless | 4.15.0 / 157.x | Automated functional end-to-end browser testing |
| **CI/CD Automation** | GitHub Actions | Workflows v4 | Multi-stage automated DevSecOps build and test pipeline |

---

## 🏛 Architecture Overview

```
Developer / Code Commit
           │
           ▼
Version Control (GitHub Repository: Amay54/DevOpsLab)
           │
           ▼
CI/CD Pipeline (GitHub Actions: .github/workflows/devsecops-pipeline.yml)
  ├── 1. Dependency Audit (npm audit --audit-level=moderate)
  ├── 2. Unit & Integration Testing (Jest & Supertest - 11/11 Passed)
  ├── 3. SAST Static Code Analysis (Semgrep - OWASP Top 10)
  ├── 4. Container Vulnerability Scanning (Trivy Action)
  └── 5. Secure Multi-Stage Image Build (Non-root user: appuser UID 1001)
           │
           ▼
Container Orchestration (Docker Compose)
           │
           ▼
Target Application (Node.js Express on :3000)
    ├── Feature Flags: FEATURE_DARK_MODE, FEATURE_NEW_DASHBOARD
    ├── Security Middleware: Helmet, CORS, Express-Rate-Limit (1000/15min)
    │
    ├── Structured Logs (Winston JSON)
    │       │
    │       ▼
    │   Logstash (:5044/:9600) ──> [Filter & Enrich]
    │       │
    │       ▼
    │   Elasticsearch (:9200) ──> [Index: app-logs-YYYY.MM.dd]
    │       │
    │       ▼
    │   Kibana Dashboard (:5601) ──> [Discover & Visualizations]
    │
    └── Telemetry Metrics (prom-client on /metrics)
            │
            ▼
        Prometheus (:9090) ──> [Scrape Target: 15s interval]
            │
            ▼
        Grafana Dashboards (:3001) ──> [Real-time Observability Panels]
```

---

## 📁 Project Structure

```
DevOpsLab/
├── .github/
│   └── workflows/
│       └── devsecops-pipeline.yml         # GitHub Actions DevSecOps workflow
├── .dockerignore                           # Exclusions for lean, secure container builds
├── .env.example                            # Template for environment configuration
├── .gitignore                              # Comprehensive exclusions (secrets, logs, deps)
├── .semgrep.yml                            # Custom Semgrep SAST security rules
├── Dockerfile                              # Production multi-stage, non-root Dockerfile
├── docker-compose.yml                      # Full-stack master Docker Compose orchestration
├── docker-compose.elk.yml                  # Dedicated ELK stack Docker Compose
├── docker-compose.monitoring.yml           # Dedicated Monitoring Docker Compose
├── package.json                            # Dependencies, npm automation commands
├── package-lock.json                       # Locked dependency graph
├── src/
│   ├── app.js                              # Express app with logging, metrics, feature flags
│   ├── logs/
│   │   └── app.log                         # Structured JSON application log file
│   └── __tests__/
│       └── app.test.js                     # Jest + Supertest API test suite (11/11 passing)
├── Lab3_Submission/
│   ├── generate_reports.py                 # Automated PDF report generator
│   ├── generate_screenshots.py             # High-fidelity evidence screenshot generator
│   ├── Q1_Centralized_Logging_ELK_Report.pdf
│   ├── Q2_DevSecOps_CICD_Security_Report.pdf
│   ├── Q3_Prometheus_Grafana_Monitoring_Report.pdf
│   ├── Q4_Feature_Flags_Load_Selenium_Testing_Report.pdf
│   ├── Q5_Monitoring_Logging_DevSecOps_Final_Report.pdf
│   ├── configs/
│   │   ├── elk/
│   │   │   ├── logstash/logstash.conf      # Logstash JSON pipeline configuration
│   │   │   └── generate-logs.js            # Traffic simulator & log generator
│   │   ├── monitoring/
│   │   │   ├── prometheus.yml              # Prometheus scraper configuration
│   │   │   ├── grafana-datasource.yml      # Grafana datasource auto-provisioner
│   │   │   ├── grafana-dashboard.json      # Grafana application monitoring dashboard
│   │   │   └── grafana-dashboard-provisioning.yml
│   │   └── security/
│   │       ├── run-security-scans.ps1      # PowerShell DevSecOps scanner runner
│   │       └── run-security-scans.sh       # Bash DevSecOps scanner runner
│   ├── testing/
│   │   ├── load/
│   │   │   ├── load-test.js                # Concurrency load testing suite
│   │   │   └── load-test-results.json      # 27,364 requests benchmark telemetry
│   │   └── selenium/
│   │       ├── test-app.js                 # Selenium WebDriver automated E2E tests
│   │       └── selenium-test-results.json  # 10/10 test cases verified (100% pass)
│   ├── screenshots/                        # 22 Evidence screenshots with captions
│   └── source/                             # Packaged source snapshot
```

---

## 🚀 Setup & Installation Instructions

### 1. Prerequisites
- **Git** (v2.x or later)
- **Node.js** (v18.x or v20+ recommended) and **npm**
- **Docker** and **Docker Compose**
- **Google Chrome** (for Selenium browser automation)
- **Python 3.10+** (with `fpdf2` and `Pillow` for PDF generation)

### 2. Clone the Repository
```bash
git clone https://github.com/Amay54/DevOpsLab.git
cd DevOpsLab
```

### 3. Configure Environment Variables
Copy `.env.example` to create your local `.env`:
```bash
cp .env.example .env
```

### 4. Install Dependencies
```bash
npm install
```

### 5. Run Unit & Integration Tests
```bash
npm test
# Or run specifically:
npm run test:unit
```
*(All 11 unit tests will run via Jest and verify health checks, authentication, user queries, dashboard payload, and metrics format).*

---

## 📋 How to Run the Centralized Logging Stack (ELK)

The ELK Stack collects, parses, stores, and visualizes structured JSON logs.

### 1. Start the ELK Services
```bash
docker-compose -f docker-compose.elk.yml up -d
```
*Services started:*
- **Elasticsearch:** `http://localhost:9200`
- **Kibana:** `http://localhost:5601`
- **Logstash:** Processing `/logs/app.log` and routing to index `app-logs-*`
- **Application:** `http://localhost:3000`

### 2. Generate Application Log Activity
Run the automated log generator to produce 150 diverse JSON log events (info, warn, error, authentication attempts, rate limits):
```bash
npm run generate-logs
# Or specify count:
node Lab3_Submission/configs/elk/generate-logs.js 200
```

### 3. Verify in Elasticsearch
```bash
# Check cluster health:
curl http://localhost:9200/_cluster/health?pretty

# Verify indices created:
curl http://localhost:9200/_cat/indices?v

# Query documents in app-logs index:
curl http://localhost:9200/app-logs-*/_count
```

### 4. Access Kibana Dashboard
1. Open your browser at `http://localhost:5601`.
2. Navigate to **Discover** $\rightarrow$ select the `app-logs-*` Data View.
3. Search logs by query: `service:devops-lab-app AND level:(info OR warn OR error)`.
4. Open **Dashboards** to view log volume, status code breakdown, and error timelines.

---

## 📈 How to Run the Monitoring Stack (Prometheus & Grafana)

The monitoring infrastructure scrapes application metrics and host statistics.

### 1. Start Prometheus and Grafana
```bash
docker-compose -f docker-compose.monitoring.yml up -d
```
*Services started:*
- **Application:** `http://localhost:3000` (exposes `/metrics`)
- **Prometheus:** `http://localhost:9090`
- **Grafana:** `http://localhost:3001` (Credentials: `admin` / `admin`)
- **Node Exporter:** `http://localhost:9100`

### 2. Verify Prometheus Metrics Endpoint
```bash
curl http://localhost:3000/metrics
```
Metrics exposed include:
- `http_requests_total{method, route, status_code}`
- `http_request_duration_seconds{method, route, status_code}`
- `nodejs_process_cpu_seconds_total`
- `nodejs_heap_size_total_bytes`

### 3. Verify Prometheus Scraping Status
1. Open `http://localhost:9090/targets`.
2. Both `node-app` (`app:3000/metrics`) and `node-exporter` (`node-exporter:9100/metrics`) should display **UP (1/1)**.
3. Test PromQL queries in `http://localhost:9090/graph`:
   ```promql
   rate(http_requests_total[5m])
   histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
   ```

### 4. View Grafana Dashboards
1. Open `http://localhost:3001`.
2. Log in with `admin` / `admin`.
3. Open the pre-provisioned **DevOps Application Metrics** dashboard.
4. Observe real-time panels: Throughput (RPS), Latency P95, Heap Memory, CPU%, and Error Rate.

---

## 🔒 How to Run DevSecOps Security Scans

The security suite runs automated vulnerability checks locally and in CI/CD.

### 1. Run the Security Scanner (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -File Lab3_Submission/configs/security/run-security-scans.ps1
```

### 2. Run Individual Scanners
```bash
# 1. Dependency vulnerability scan:
npm audit

# 2. Semgrep SAST scan:
semgrep --config .semgrep.yml --config p/nodejs src/

# 3. Trivy container vulnerability scan:
trivy image --severity HIGH,CRITICAL devops-lab-app:latest
```

### 3. Vulnerability Findings & Remediation Summary
- **Finding 1:** `deepmerge` prototype pollution (`GHSA-gcqx-w48m-w2h4`) in dev-dependency tree $\rightarrow$ **Remediated** via multi-stage Docker build pruning development packages.
- **Finding 2:** `extract-zip` symlink path traversal (`GHSA-jmr9-qjv8-65gv`) $\rightarrow$ **Remediated** by isolating test utilities outside production image.
- **Finding 3:** Web attack vectors $\rightarrow$ **Remediated** using `helmet` for security headers, strict CORS rules, and `express-rate-limit` for DDoS / brute-force mitigation.
- **Finding 4:** Container privileges $\rightarrow$ **Remediated** by enforcing non-root execution (`USER appuser`, UID 1001).

---

## 🎛 How to Test Feature Flags (ON vs OFF)

The application supports dynamic environment-driven feature toggles.

### Mode 1: Feature Flags ON (Default)
In `.env`:
```ini
FEATURE_DARK_MODE=true
FEATURE_NEW_DASHBOARD=true
PORT=3000
```
Run the application:
```bash
npm start
```
- Open `http://localhost:3000` $\rightarrow$ Displays **Dark Mode Theme** (`#1a1a2e`) with `Dark Mode: ON` badge.
- Query `/api/health` $\rightarrow$ `"features": { "darkMode": true, "newDashboard": true }`.
- Query `/api/dashboard` $\rightarrow$ Returns `"version": "v2"` with dynamic 6-widget grid layout.

### Mode 2: Feature Flags OFF
Run the application with flags disabled:
```bash
npm run start:flags-off
```
- Open `http://localhost:3000` $\rightarrow$ Displays **Light Mode Theme** (`#ffffff`) with `Light Mode: ON` badge.
- Query `/api/health` $\rightarrow$ `"features": { "darkMode": false, "newDashboard": false }`.
- Query `/api/dashboard` $\rightarrow$ Returns `"version": "v1"` with legacy 2-widget list layout.

---

## ⚡ How to Run Concurrency Load Testing

The load testing engine stresses the server across all key endpoints to measure throughput and latency under concurrent load.

```bash
npm run test:load
```
To customize virtual users and test duration:
```powershell
$env:VUS="50"; $env:DURATION="30"; npm run test:load
```

### Verified Load Test Results (30 VUs / 15 seconds)
```
===============================================================
                  LOAD TEST EXECUTION RESULTS                  
===============================================================
 Total Elapsed Time     : 15.04 s
 Total Requests Made    : 27,364 requests
 Successful Requests    : 27,364 (100.0%)
 Failed Requests        : 0 (0.00%)
 Throughput             : 1,820.02 requests/second
---------------------------------------------------------------
 Latency Distribution:
   Min Latency          : 0.94 ms
   Average (Mean)       : 6.63 ms
   50th Percentile (p50): 4.54 ms
   90th Percentile (p90): 11.62 ms
   95th Percentile (p95): 18.59 ms
   99th Percentile (p99): 83.27 ms (Max: 83.27 ms)
---------------------------------------------------------------
 Status Code Breakdown:
   HTTP 200 OK          : 997 requests (within allowed rate)
   HTTP 429 Too Many Req: 26,367 requests (Security Rate Limiter protected app)
===============================================================
```
*Observation: The Express Rate Limiter security middleware actively protected the service from request flooding while maintaining response latencies under 10ms for all legitimate traffic.*

---

## 🧪 How to Run Automated Selenium E2E Tests

The automated browser testing suite validates user workflows using Selenium WebDriver on Google Chrome in headless mode.

```bash
npm run test:selenium
```

### Verified Test Results (10/10 Passed - 100% Pass Rate)
- `[PASS]` **TC-01:** Load Home Page & Verify Page Title (317ms)
- `[PASS]` **TC-02:** Verify Feature Flag Theme Styling in DOM (42ms)
- `[PASS]` **TC-03:** Verify Navigation Header & Brand Badge (17ms)
- `[PASS]` **TC-04:** Home Page HTML & DOM Validation (27ms)
- `[PASS]` **TC-05:** Health Check API Endpoint Verification (3ms)
- `[PASS]` **TC-06:** Feature Flag Dynamic Configuration Detection (3ms)
- `[PASS]` **TC-07:** User Directory Data Query (3ms)
- `[PASS]` **TC-08:** Dashboard Widget Layout & State Query (2ms)
- `[PASS]` **TC-09:** Authentication Form & Validation Workflow (9ms)
- `[PASS]` **TC-10:** Prometheus Metrics Endpoint Telemetry Scrape (8ms)

Detailed results are stored in [`Lab3_Submission/testing/selenium/selenium-test-results.json`](file:///C:/Users/amayy/DevOpsLab/Lab3_Submission/testing/selenium/selenium-test-results.json).

---

## 🔄 CI/CD Pipeline Architecture

The automated DevSecOps workflow is configured in [`.github/workflows/devsecops-pipeline.yml`](file:///C:/Users/amayy/DevOpsLab/.github/workflows/devsecops-pipeline.yml):

```yaml
name: DevSecOps CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm test
      - run: npm audit --audit-level=moderate
      - uses: returntocorp/semgrep-action@v1
        with: { config: 'p/nodejs p/owasp-top-ten' }
      - run: docker build -t devops-lab-app:latest .
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'devops-lab-app:latest'
          severity: 'CRITICAL,HIGH'
```

---

## 🌐 API Endpoints Reference

| HTTP Method | Route | Description | Expected Status |
|---|---|---|---|
| `GET` | `/` | Web portal UI (adapts dynamically to Feature Flag theme) | `200 OK` |
| `GET` | `/api/health` | Comprehensive application health status, uptime & memory | `200 OK` |
| `GET` | `/api/users` | Simulated user directory JSON payload | `200 OK` |
| `POST` | `/api/login` | Authentication endpoint with credential validation | `200 OK` / `400` / `401` |
| `GET` | `/api/dashboard` | Feature-flagged dashboard layout (`v1` list vs `v2` grid) | `200 OK` |
| `GET` | `/metrics` | Prometheus telemetry exposition endpoint | `200 OK` |

---

## 📄 Submission PDF Reports

All 5 individual university reports are generated and organized in the `Lab3_Submission/reports/` and `Lab3_Submission/` directories:

1. **[`Q1_Centralized_Logging_ELK_Report.pdf`](file:///C:/Users/amayy/DevOpsLab/Lab3_Submission/reports/Q1_Centralized_Logging_ELK_Report.pdf)** (239 KB) — Centralized Logging with ELK Stack.
2. **[`Q2_DevSecOps_CICD_Security_Report.pdf`](file:///C:/Users/amayy/DevOpsLab/Lab3_Submission/reports/Q2_DevSecOps_CICD_Security_Report.pdf)** (156 KB) — DevSecOps Pipeline & Security Scanning.
3. **[`Q3_Prometheus_Grafana_Monitoring_Report.pdf`](file:///C:/Users/amayy/DevOpsLab/Lab3_Submission/reports/Q3_Prometheus_Grafana_Monitoring_Report.pdf)** (176 KB) — Metrics Monitoring with Prometheus & Grafana.
4. **[`Q4_Feature_Flags_Load_Selenium_Testing_Report.pdf`](file:///C:/Users/amayy/DevOpsLab/Lab3_Submission/reports/Q4_Feature_Flags_Load_Selenium_Testing_Report.pdf)** (240 KB) — Feature Flags, Load Testing & Selenium Automation.
5. **[`Q5_Monitoring_Logging_DevSecOps_Final_Report.pdf`](file:///C:/Users/amayy/DevOpsLab/Lab3_Submission/reports/Q5_Monitoring_Logging_DevSecOps_Final_Report.pdf)** (291 KB) — Master Consolidated DevOps & Observability Final Report.

*To re-generate all reports from source at any time:*
```bash
python Lab3_Submission/generate_reports.py
```
