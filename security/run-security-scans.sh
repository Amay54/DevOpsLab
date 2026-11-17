#!/bin/bash
# ─── Security Scanning Script ────────────────────────────────────────────────
# Runs npm audit, Trivy container scan, and Semgrep SAST locally
# Usage: bash run-security-scans.sh

set -e

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

REPORT_DIR="../../security-reports"
mkdir -p "$REPORT_DIR"

echo -e "${BOLD}${BLUE}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${BLUE}║       DevOps Lab Security Scan Suite         ║${NC}"
echo -e "${BOLD}${BLUE}╚══════════════════════════════════════════════╝${NC}"
echo ""

# ── 1. NPM Audit ────────────────────────────────────────────────────────────
echo -e "${BOLD}${YELLOW}[1/3] Running NPM Audit...${NC}"
echo "────────────────────────────────────────────────"

cd "$(dirname "$0")/../../.."

if npm audit --production > "$REPORT_DIR/npm-audit-report.txt" 2>&1; then
    echo -e "${GREEN}✅ NPM Audit: No vulnerabilities found${NC}"
else
    echo -e "${YELLOW}⚠️  NPM Audit: Vulnerabilities detected (see report)${NC}"
fi

npm audit --production --json > "$REPORT_DIR/npm-audit-report.json" 2>/dev/null || true
echo -e "   Report saved to: ${BLUE}$REPORT_DIR/npm-audit-report.txt${NC}"
echo ""

# ── 2. Trivy Container Scan ────────────────────────────────────────────────
echo -e "${BOLD}${YELLOW}[2/3] Running Trivy Container Scan...${NC}"
echo "────────────────────────────────────────────────"

if command -v trivy &> /dev/null; then
    # Build Docker image first
    echo "Building Docker image for scanning..."
    docker build -t devops-lab-app:scan . -q 2>/dev/null

    if trivy image --severity HIGH,CRITICAL --format table \
        -o "$REPORT_DIR/trivy-report.txt" devops-lab-app:scan 2>/dev/null; then
        echo -e "${GREEN}✅ Trivy Scan: Complete${NC}"
    else
        echo -e "${YELLOW}⚠️  Trivy Scan: Issues found (see report)${NC}"
    fi

    # Also generate JSON report
    trivy image --severity HIGH,CRITICAL --format json \
        -o "$REPORT_DIR/trivy-report.json" devops-lab-app:scan 2>/dev/null || true

    echo -e "   Report saved to: ${BLUE}$REPORT_DIR/trivy-report.txt${NC}"

    # Cleanup scan image
    docker rmi devops-lab-app:scan 2>/dev/null || true
else
    echo -e "${RED}❌ Trivy not found. Install it:${NC}"
    echo "   brew install trivy  (macOS)"
    echo "   sudo apt install trivy  (Ubuntu)"
    echo "   choco install trivy  (Windows)"
    echo -e "${YELLOW}   Skipping Trivy scan...${NC}"
fi
echo ""

# ── 3. Semgrep SAST Scan ──────────────────────────────────────────────────
echo -e "${BOLD}${YELLOW}[3/3] Running Semgrep SAST Scan...${NC}"
echo "────────────────────────────────────────────────"

if command -v semgrep &> /dev/null; then
    if semgrep --config .semgrep.yml --config "p/nodejs" \
        --json -o "$REPORT_DIR/semgrep-report.json" \
        src/ 2>/dev/null; then
        echo -e "${GREEN}✅ Semgrep Scan: No issues found${NC}"
    else
        echo -e "${YELLOW}⚠️  Semgrep Scan: Issues found (see report)${NC}"
    fi

    # Also generate readable report
    semgrep --config .semgrep.yml --config "p/nodejs" \
        -o "$REPORT_DIR/semgrep-report.txt" \
        src/ 2>/dev/null || true

    echo -e "   Report saved to: ${BLUE}$REPORT_DIR/semgrep-report.json${NC}"
else
    echo -e "${RED}❌ Semgrep not found. Install it:${NC}"
    echo "   pip install semgrep"
    echo "   brew install semgrep  (macOS)"
    echo -e "${YELLOW}   Skipping Semgrep scan...${NC}"
fi
echo ""

# ── Summary ──────────────────────────────────────────────────────────────────
echo -e "${BOLD}${BLUE}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${BLUE}║            Scan Summary                      ║${NC}"
echo -e "${BOLD}${BLUE}╚══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Reports saved to: ${BOLD}$REPORT_DIR/${NC}"
echo ""
ls -la "$REPORT_DIR/" 2>/dev/null || true
echo ""
echo -e "${GREEN}Security scanning complete!${NC}"
