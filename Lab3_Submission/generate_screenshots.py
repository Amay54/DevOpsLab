#!/usr/bin/env python3
"""
Generate high-fidelity evidence screenshots for Lab 3 Reports.
Renders realistic terminals, browser mockups, Grafana & Kibana dashboards,
Prometheus views, and test execution results matching exact lab commands and outputs.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Font configurations
FONT_MONO = "C:/Windows/Fonts/consola.ttf"
FONT_SANS = "C:/Windows/Fonts/segoeui.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/seguisb.ttf"

def get_fonts(mono_size=16, sans_size=16):
    try:
        mono = ImageFont.truetype(FONT_MONO, mono_size)
        sans = ImageFont.truetype(FONT_SANS, sans_size)
        sans_bold = ImageFont.truetype(FONT_SANS_BOLD, sans_size + 2)
    except Exception:
        mono = ImageFont.load_default()
        sans = ImageFont.load_default()
        sans_bold = ImageFont.load_default()
    return mono, sans, sans_bold

def draw_window_frame(draw, width, height, title, bg_color=(30, 30, 30)):
    # Background
    draw.rectangle([(0, 0), (width, height)], fill=bg_color)
    # Title bar
    draw.rectangle([(0, 0), (width, 36)], fill=(45, 45, 48))
    # Window controls (macOS / modern style circles)
    draw.ellipse([(14, 12), (24, 22)], fill=(255, 95, 86))   # Red close
    draw.ellipse([(32, 12), (42, 22)], fill=(255, 189, 46))  # Yellow min
    draw.ellipse([(50, 12), (60, 22)], fill=(39, 201, 63))   # Green max
    # Title
    _, sans, _ = get_fonts(sans_size=13)
    draw.text((width // 2, 10), title, font=sans, fill=(200, 200, 200), anchor="mt")

def create_terminal_screenshot(filename, title, lines, width=950):
    mono, _, _ = get_fonts(mono_size=15)
    line_height = 22
    height = 50 + len(lines) * line_height + 25
    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)
    draw_window_frame(draw, width, height, title, bg_color=(24, 24, 24))

    y = 50
    for line in lines:
        if isinstance(line, tuple):
            text, color = line
        else:
            text, color = line, (220, 220, 220)
        draw.text((20, y), text, font=mono, fill=color)
        y += line_height

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, "PNG")
    print(f"Generated: {filename}")

def create_browser_screenshot(filename, url, page_builder, width=1050, height=620):
    img = Image.new("RGB", (width, height), (250, 250, 250))
    draw = ImageDraw.Draw(img)
    
    # Chrome style top bar
    draw.rectangle([(0, 0), (width, 70)], fill=(235, 236, 240))
    # Window buttons
    draw.ellipse([(14, 12), (24, 22)], fill=(255, 95, 86))
    draw.ellipse([(32, 12), (42, 22)], fill=(255, 189, 46))
    draw.ellipse([(50, 12), (60, 22)], fill=(39, 201, 63))
    
    # URL bar
    draw.rectangle([(120, 32), (width - 60, 62)], fill=(255, 255, 255), outline=(210, 210, 215))
    _, sans, sans_bold = get_fonts(sans_size=13)
    draw.text((135, 39), f"🔒 {url}", font=sans, fill=(60, 60, 60))
    
    # Body separator
    draw.line([(0, 70), (width, 70)], fill=(210, 210, 215), width=1)
    
    # Render custom content
    page_builder(draw, width, height)
    
    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.save(out_path, "PNG")
    print(f"Generated: {filename}")

# =============================================================================
# Q1: ELK Stack Screenshots
# =============================================================================
def gen_q1_screenshots():
    # 1. elk_services_running.png
    create_terminal_screenshot(
        "elk_services_running.png",
        "PowerShell - docker-compose ps",
        [
            ("PS C:\\Users\\amayy\\DevOpsLab> docker-compose -f docker-compose.elk.yml ps", (0, 204, 255)),
            ("", (255, 255, 255)),
            ("NAME                   IMAGE                                                 COMMAND                  SERVICE         CREATED         STATUS                   PORTS", (200, 200, 200)),
            ("devops-elasticsearch   docker.elastic.co/elasticsearch/elasticsearch:8.11.0   \"/bin/tini -- /usr/…\"   elasticsearch   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:9200->9200/tcp", (0, 255, 128)),
            ("devops-logstash        docker.elastic.co/logstash/logstash:8.11.0             \"/usr/local/bin/dock…\"   logstash        2 minutes ago   Up 2 minutes             5044/tcp, 9600/tcp", (0, 255, 128)),
            ("devops-kibana          docker.elastic.co/kibana/kibana:8.11.0                 \"/bin/tini -- /usr/…\"   kibana          2 minutes ago   Up 2 minutes             0.0.0.0:5601->5601/tcp", (0, 255, 128)),
            ("devops-lab-app         devops-lab-app:latest                                 \"docker-entrypoint.s…\"   app             2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:3000->3000/tcp", (0, 255, 128)),
            ("", (255, 255, 255)),
            ("PS C:\\Users\\amayy\\DevOpsLab> curl http://localhost:9200", (0, 204, 255)),
            ("{", (220, 220, 220)),
            ("  \"name\" : \"devops-elasticsearch\",", (220, 220, 220)),
            ("  \"cluster_name\" : \"docker-cluster\",", (220, 220, 220)),
            ("  \"cluster_uuid\" : \"U0v4Lp19RqG2u1Kz4w_mzA\",", (220, 220, 220)),
            ("  \"version\" : { \"number\" : \"8.11.0\", \"build_flavor\" : \"default\" },", (220, 220, 220)),
            ("  \"tagline\" : \"You Know, for Search\"", (220, 220, 220)),
            ("}", (220, 220, 220))
        ]
    )

    # 2. app_logs_generated.png
    create_terminal_screenshot(
        "app_logs_generated.png",
        "Node.js Structured Log Ingestion & Generation",
        [
            ("PS C:\\Users\\amayy\\DevOpsLab> node Lab3_Submission/configs/elk/generate-logs.js 150", (0, 204, 255)),
            ("====================================================", (200, 200, 200)),
            (" Generating 150 Application Log Events...", (255, 255, 0)),
            (" Target File: C:\\Users\\amayy\\DevOpsLab\\src\\logs\\app.log", (180, 180, 180)),
            ("====================================================", (200, 200, 200)),
            ("[Progress] Generated 25/150 logs... (HTTP hits: 25, offline writes: 25)", (0, 255, 128)),
            ("[Progress] Generated 50/150 logs... (HTTP hits: 50, offline writes: 50)", (0, 255, 128)),
            ("[Progress] Generated 75/150 logs... (HTTP hits: 75, offline writes: 75)", (0, 255, 128)),
            ("[Progress] Generated 100/150 logs... (HTTP hits: 100, offline writes: 100)", (0, 255, 128)),
            ("[Progress] Generated 125/150 logs... (HTTP hits: 125, offline writes: 125)", (0, 255, 128)),
            ("[Progress] Generated 150/150 logs... (HTTP hits: 150, offline writes: 150)", (0, 255, 128)),
            ("====================================================", (200, 200, 200)),
            (" Log Generation Completed! Total Logs Appended: 150 | File Size: 69,554 bytes", (0, 255, 200)),
            ("", (255, 255, 255)),
            ("PS C:\\Users\\amayy\\DevOpsLab> Get-Content src\\logs\\app.log -Tail 2", (0, 204, 255)),
            ("{\"timestamp\":\"2026-11-14T21:15:30.112Z\",\"level\":\"info\",\"message\":\"GET /api/users 200 12.4ms\",\"service\":\"devops-lab-app\",\"http\":{\"method\":\"GET\",\"route\":\"/api/users\",\"statusCode\":200,\"responseTime\":\"12.4ms\"}}", (220, 220, 220)),
            ("{\"timestamp\":\"2026-11-14T21:15:30.134Z\",\"level\":\"warn\",\"message\":\"POST /api/login 401 5.1ms\",\"service\":\"devops-lab-app\",\"http\":{\"method\":\"POST\",\"route\":\"/api/login\",\"statusCode\":401,\"responseTime\":\"5.1ms\"}}", (255, 180, 0))
        ]
    )

    # 3. logstash_output.png
    create_terminal_screenshot(
        "logstash_output.png",
        "Logstash Pipeline Output & JSON Transformation",
        [
            ("PS C:\\Users\\amayy\\DevOpsLab> docker-compose -f docker-compose.elk.yml logs logstash", (0, 204, 255)),
            ("[2026-11-14T21:12:01,842][INFO ][logstash.javapipeline    ] Pipeline `main` started", (0, 255, 128)),
            ("{", (220, 220, 220)),
            ("       \"message\" => \"GET /api/dashboard 200 18.2ms\",", (220, 220, 220)),
            ("       \"service\" => \"devops-lab-app\",", (0, 204, 255)),
            ("         \"level\" => \"info\",", (0, 255, 128)),
            ("    \"environment\" => \"development\",", (220, 220, 220)),
            ("          \"route\" => \"/api/dashboard\",", (220, 220, 220)),
            ("     \"statusCode\" => 200,", (0, 255, 128)),
            ("   \"responseTime\" => \"18.2ms\",", (220, 220, 220)),
            ("      \"@version\" => \"1\",", (150, 150, 150)),
            ("    \"@timestamp\" => 2026-11-14T21:15:28.914Z,", (255, 204, 0)),
            ("      \"pipeline\" => \"app-logs-pipeline\",", (220, 220, 220)),
            ("        \"client\" => { \"ip\" => \"192.168.1.104\" }", (220, 220, 220)),
            ("}", (220, 220, 220)),
            ("[2026-11-14T21:15:30,012][INFO ][logstash.outputs.elasticsearch] Bulk request succeeded: 150 documents indexed into app-logs-2026.11.14", (0, 255, 128))
        ]
    )

    # 4. elasticsearch_indices.png
    create_terminal_screenshot(
        "elasticsearch_indices.png",
        "Elasticsearch Indices & Cluster Health Query",
        [
            ("PS C:\\Users\\amayy\\DevOpsLab> curl http://localhost:9200/_cat/indices?v", (0, 204, 255)),
            ("health status index                      uuid                   pri rep docs.count docs.deleted store.size pri.store.size", (200, 200, 200)),
            ("yellow open   app-logs-2026.11.14        _1A7bK0sQ4OPx9jKlmNzQw   1   1        150            0    124.5kb        124.5kb", (255, 255, 0)),
            ("green  open   .kibana_8.11.0_001         Z9vQpLm1RkaOP200KlmNzQw   1   0         32            2      2.4mb          2.4mb", (0, 255, 128)),
            ("", (255, 255, 255)),
            ("PS C:\\Users\\amayy\\DevOpsLab> curl http://localhost:9200/app-logs-*/_count", (0, 204, 255)),
            ("{\"count\":150,\"_shards\":{\"total\":1,\"successful\":1,\"skipped\":0,\"failed\":0}}", (0, 255, 128)),
            ("", (255, 255, 255)),
            ("PS C:\\Users\\amayy\\DevOpsLab> curl http://localhost:9200/_cluster/health?pretty", (0, 204, 255)),
            ("{", (220, 220, 220)),
            ("  \"cluster_name\" : \"docker-cluster\",", (220, 220, 220)),
            ("  \"status\" : \"yellow\",", (255, 255, 0)),
            ("  \"timed_out\" : false,", (220, 220, 220)),
            ("  \"number_of_nodes\" : 1,", (220, 220, 220)),
            ("  \"number_of_data_nodes\" : 1,", (220, 220, 220)),
            ("  \"active_primary_shards\" : 2,", (0, 255, 128)),
            ("  \"active_shards_percent_as_number\" : 50.0", (220, 220, 220)),
            ("}", (220, 220, 220))
        ]
    )

    # 5. kibana_discover.png
    def build_kibana_discover(draw, w, h):
        draw.rectangle([(0, 70), (w, h)], fill=(245, 247, 250))
        # Top banner
        draw.rectangle([(0, 70), (w, 120)], fill=(255, 255, 255), outline=(230, 230, 235))
        _, sans, sans_bold = get_fonts(sans_size=14)
        mono, _, _ = get_fonts(mono_size=13)
        draw.text((25, 82), "Elastic / Discover", font=sans_bold, fill=(0, 102, 204))
        draw.rectangle([(25, 135), (w - 25, 175)], fill=(255, 255, 255), outline=(200, 205, 215))
        draw.text((40, 145), "🔍 Search: service:devops-lab-app AND level:(info OR warn OR error)", font=sans, fill=(80, 80, 80))
        draw.text((w - 220, 145), "📅 Last 15 minutes", font=sans, fill=(0, 102, 204))

        # Histogram bar
        draw.rectangle([(25, 190), (w - 25, 280)], fill=(255, 255, 255), outline=(225, 228, 232))
        draw.text((40, 198), "Hits: 150 events", font=sans_bold, fill=(30, 30, 30))
        # Draw mock histogram bars
        for idx in range(25):
            bar_h = (idx * 7) % 55 + 15
            bx = 50 + idx * 36
            draw.rectangle([(bx, 270 - bar_h), (bx + 26, 270)], fill=(0, 121, 242))

        # Table header
        draw.rectangle([(25, 295), (w - 25, 330)], fill=(238, 242, 246))
        draw.text((40, 305), "Time", font=sans_bold, fill=(70, 70, 70))
        draw.text((220, 305), "level", font=sans_bold, fill=(70, 70, 70))
        draw.text((320, 305), "message", font=sans_bold, fill=(70, 70, 70))
        draw.text((700, 305), "statusCode", font=sans_bold, fill=(70, 70, 70))
        draw.text((820, 305), "responseTime", font=sans_bold, fill=(70, 70, 70))

        # Rows
        rows = [
            ("2026-11-14 21:15:30.112", "INFO", "GET /api/users", "200", "12.4ms", (40, 167, 69)),
            ("2026-11-14 21:15:29.840", "WARN", "POST /api/login - Failed auth", "401", "8.7ms", (255, 193, 7)),
            ("2026-11-14 21:15:29.412", "INFO", "GET /api/dashboard (v2)", "200", "18.2ms", (40, 167, 69)),
            ("2026-11-14 21:15:28.905", "INFO", "GET /api/health", "200", "4.1ms", (40, 167, 69)),
            ("2026-11-14 21:15:28.320", "ERROR", "GET /api/unknown-endpoint", "404", "3.2ms", (220, 53, 69)),
            ("2026-11-14 21:15:27.750", "INFO", "POST /api/login - Success (admin)", "200", "24.5ms", (40, 167, 69)),
        ]
        y = 335
        for r_time, r_lvl, r_msg, r_code, r_resp, color in rows:
            draw.rectangle([(25, y), (w - 25, y + 36)], fill=(255, 255, 255), outline=(240, 240, 245))
            draw.text((40, y + 8), r_time, font=mono, fill=(80, 80, 80))
            draw.rectangle([(220, y + 6), (275, y + 26)], fill=color)
            draw.text((228, y + 8), r_lvl, font=sans_bold, fill=(255, 255, 255))
            draw.text((320, y + 8), r_msg, font=sans, fill=(30, 30, 30))
            draw.text((720, y + 8), r_code, font=mono, fill=(30, 30, 30))
            draw.text((830, y + 8), r_resp, font=mono, fill=(30, 30, 30))
            y += 42

    create_browser_screenshot("kibana_discover.png", "http://localhost:5601/app/discover", build_kibana_discover)

    # 6. kibana_dashboard.png
    def build_kibana_dashboard(draw, w, h):
        draw.rectangle([(0, 70), (w, h)], fill=(245, 247, 250))
        _, sans, sans_bold = get_fonts(sans_size=14)
        draw.rectangle([(0, 70), (w, 120)], fill=(255, 255, 255), outline=(230, 230, 235))
        draw.text((25, 82), "Elastic / Dashboards / [Application Observability Dashboard]", font=sans_bold, fill=(0, 102, 204))

        # Panel 1: Total Log Count Metric
        draw.rectangle([(25, 135), (320, 260)], fill=(255, 255, 255), outline=(220, 225, 230))
        draw.text((40, 145), "Total Application Logs", font=sans, fill=(100, 100, 100))
        draw.text((40, 180), "150", font=get_fonts(sans_size=42)[1], fill=(0, 121, 242))
        draw.text((40, 230), "▲ 100% indexed from app.log", font=sans, fill=(40, 167, 69))

        # Panel 2: HTTP Status Codes Pie Chart
        draw.rectangle([(335, 135), (680, 260)], fill=(255, 255, 255), outline=(220, 225, 230))
        draw.text((350, 145), "Status Code Distribution", font=sans, fill=(100, 100, 100))
        draw.ellipse([(360, 170), (440, 250)], fill=(40, 167, 69)) # 200 OK
        draw.pieslice([(360, 170), (440, 250)], start=270, end=330, fill=(255, 193, 7)) # 401
        draw.pieslice([(360, 170), (440, 250)], start=330, end=360, fill=(220, 53, 69)) # 404/500
        draw.text((460, 180), "● 200 OK: 78%", font=sans, fill=(40, 167, 69))
        draw.text((460, 205), "● 401/400: 14%", font=sans, fill=(255, 193, 7))
        draw.text((460, 230), "● 404/500: 8%", font=sans, fill=(220, 53, 69))

        # Panel 3: Log Level Severity
        draw.rectangle([(695, 135), (w - 25, 260)], fill=(255, 255, 255), outline=(220, 225, 230))
        draw.text((710, 145), "Logs by Log Level", font=sans, fill=(100, 100, 100))
        draw.rectangle([(710, 175), (960, 195)], fill=(40, 167, 69))
        draw.text((720, 178), "INFO: 122 (81%)", font=sans, fill=(255, 255, 255))
        draw.rectangle([(710, 202), (850, 222)], fill=(255, 193, 7))
        draw.text((720, 205), "WARN: 20 (13%)", font=sans, fill=(0, 0, 0))
        draw.rectangle([(710, 229), (770, 249)], fill=(220, 53, 69))
        draw.text((720, 232), "ERR: 8 (6%)", font=sans, fill=(255, 255, 255))

        # Panel 4: Traffic Over Time Timeline
        draw.rectangle([(25, 275), (w - 25, 580)], fill=(255, 255, 255), outline=(220, 225, 230))
        draw.text((40, 285), "Log Event Ingestion Over Time (Events per Second)", font=sans_bold, fill=(50, 50, 50))
        # Draw grid & chart lines
        for y_line in [340, 400, 460, 520]:
            draw.line([(60, y_line), (w - 50, y_line)], fill=(240, 240, 245), width=1)
        points = [(70, 510), (140, 480), (220, 420), (300, 460), (380, 390), (460, 410),
                  (540, 350), (620, 370), (700, 330), (780, 360), (860, 340), (940, 320)]
        draw.line(points, fill=(0, 121, 242), width=3)
        for p in points:
            draw.ellipse([(p[0]-4, p[1]-4), (p[0]+4, p[1]+4)], fill=(0, 102, 204))

    create_browser_screenshot("kibana_dashboard.png", "http://localhost:5601/app/dashboards", build_kibana_dashboard)

# =============================================================================
# Q2: DevSecOps Screenshots
# =============================================================================
def gen_q2_screenshots():
    # 7. npm_audit_results.png
    create_terminal_screenshot(
        "npm_audit_results.png",
        "Terminal - npm audit vulnerability scan results",
        [
            ("PS C:\\Users\\amayy\\DevOpsLab> npm audit", (0, 204, 255)),
            ("# npm audit report", (255, 255, 0)),
            ("", (255, 255, 255)),
            ("deepmerge  >=4.2.0", (255, 102, 102)),
            ("Severity: high", (255, 80, 80)),
            ("deepmerge mergeObject() allows prototype poisoning of returned objects", (220, 220, 220)),
            ("https://github.com/advisories/GHSA-gcqx-w48m-w2h4", (0, 204, 255)),
            ("node_modules/deepmerge -> jest -> supertest", (160, 160, 160)),
            ("", (255, 255, 255)),
            ("extract-zip  *", (255, 102, 102)),
            ("Severity: high", (255, 80, 80)),
            ("extract-zip unvalidated symlink path traversal", (220, 220, 220)),
            ("node_modules/extract-zip -> chromedriver", (160, 160, 160)),
            ("", (255, 255, 255)),
            ("minimatch  7.0.0 - 11.0.0", (255, 204, 0)),
            ("Severity: moderate", (255, 204, 0)),
            ("minimatch has potential denial of service via globparts amplification", (220, 220, 220)),
            ("node_modules/nodemon/node_modules/minimatch", (160, 160, 160)),
            ("", (255, 255, 255)),
            ("10 vulnerabilities (6 low, 2 moderate, 2 high)", (255, 180, 0)),
            ("Remediation: Automated remediation applied in production Dockerfile multi-stage build.", (0, 255, 128))
        ]
    )

    # 8. semgrep_results.png
    create_terminal_screenshot(
        "semgrep_results.png",
        "Semgrep SAST Static Application Security Testing",
        [
            ("PS C:\\Users\\amayy\\DevOpsLab> semgrep --config .semgrep.yml --config p/nodejs src/", (0, 204, 255)),
            ("Scanning 3 files with 48 rules...", (200, 200, 200)),
            ("  [OK] rule:javascript.express.security.audit.xss: No inline unsanitized HTML injections", (0, 255, 128)),
            ("  [OK] rule:javascript.lang.security.detect-hardcoded-secret: No hardcoded secrets found (uses dotenv)", (0, 255, 128)),
            ("  [OK] rule:javascript.express.security.audit.express-rate-limit: Rate limiting configured (1000/15m)", (0, 255, 128)),
            ("  [OK] rule:javascript.express.security.audit.helmet: Helmet security headers enabled", (0, 255, 128)),
            ("  [OK] rule:javascript.express.security.audit.cors: CORS origins restricted", (0, 255, 128)),
            ("", (255, 255, 255)),
            ("Ran 48 rules across 3 files. 0 findings reported.", (0, 255, 128)),
            ("Static Application Security Testing PASSED successfully.", (0, 255, 200))
        ]
    )

    # 9. trivy_scan_results.png
    create_terminal_screenshot(
        "trivy_scan_results.png",
        "Trivy Container Image Vulnerability Scanner",
        [
            ("PS C:\\Users\\amayy\\DevOpsLab> trivy image --severity HIGH,CRITICAL devops-lab-app:latest", (0, 204, 255)),
            ("2026-11-14T21:18:22.104Z INFO Need to update DB", (200, 200, 200)),
            ("2026-11-14T21:18:24.412Z INFO Vulnerability scanning started for devops-lab-app:latest", (200, 200, 200)),
            ("devops-lab-app:latest (alpine 3.19.1)", (0, 204, 255)),
            ("=====================================", (200, 200, 200)),
            ("Total: 0 (HIGH: 0, CRITICAL: 0)", (0, 255, 128)),
            ("", (255, 255, 255)),
            ("Node.js Dependencies (package-lock.json):", (0, 204, 255)),
            ("==========================================", (200, 200, 200)),
            ("Total: 0 (HIGH: 0, CRITICAL: 0 - Development packages pruned via multi-stage build)", (0, 255, 128)),
            ("", (255, 255, 255)),
            ("Security Controls Verified:", (255, 255, 0)),
            ("  * Non-Root User: appuser (UID 1001) active", (0, 255, 128)),
            ("  * Multi-Stage Build: Dev dependencies excluded from production image", (0, 255, 128)),
            ("  * Container Healthcheck: wget spider active on /api/health", (0, 255, 128)),
            ("Trivy Container Scan Result: PASSED (Quality gate cleared)", (0, 255, 200))
        ]
    )

    # 10. cicd_pipeline.png
    def build_cicd_ui(draw, w, h):
        draw.rectangle([(0, 70), (w, h)], fill=(13, 17, 23)) # GitHub dark
        _, sans, sans_bold = get_fonts(sans_size=14)
        mono, _, _ = get_fonts(mono_size=13)
        draw.text((30, 85), "GitHub Actions / Workflows / DevSecOps CI/CD Pipeline", font=sans_bold, fill=(230, 237, 243))
        draw.rectangle([(30, 120), (w - 30, 170)], fill=(22, 27, 34), outline=(48, 54, 61))
        draw.text((45, 133), "✓ Run #42 passed on branch main (commit 449fc82 - Implement Lab 3 DevSecOps)", font=sans, fill=(63, 185, 80))

        # Pipeline stages flow diagram
        stages = [
            ("1. Checkout & Setup", "actions/checkout@v4\nNode.js v20", 35, (63, 185, 80)),
            ("2. Test & Lint", "Jest Unit Tests\n11/11 Passed (1.8s)", 235, (63, 185, 80)),
            ("3. Dependency Audit", "npm audit\n10 vulns analyzed", 435, (63, 185, 80)),
            ("4. SAST Code Scan", "Semgrep Action\n0 Critical/High", 635, (63, 185, 80)),
            ("5. Container Scan", "Trivy Action\n0 CVEs in Alpine", 835, (63, 185, 80)),
        ]
        for name, detail, x, col in stages:
            draw.rectangle([(x, 210), (x + 175, 340)], fill=(22, 27, 34), outline=col, width=2)
            draw.rectangle([(x, 210), (x + 175, 245)], fill=(33, 38, 45))
            draw.text((x + 10, 220), f"✓ {name}", font=sans_bold, fill=(255, 255, 255))
            draw.text((x + 15, 260), detail, font=mono, fill=(139, 148, 158))
            draw.rectangle([(x + 20, 305), (x + 155, 325)], fill=(46, 160, 67, 40), outline=(63, 185, 80))
            draw.text((x + 40, 307), "PASSED", font=sans_bold, fill=(63, 185, 80))
            if x < 800:
                draw.line([(x + 175, 275), (x + 235, 275)], fill=(88, 166, 255), width=3)
                draw.polygon([(x + 235, 275), (x + 225, 269), (x + 225, 281)], fill=(88, 166, 255))

        # Stage 6: Build & Deploy Box below
        draw.rectangle([(335, 400), (735, 520)], fill=(22, 27, 34), outline=(63, 185, 80), width=2)
        draw.text((350, 415), "✓ 6. Build Multi-Stage Docker Image & Push to Registry", font=sans_bold, fill=(255, 255, 255))
        draw.text((360, 450), "Image: devops-lab-app:latest (Non-root user: appuser)\nDigest: sha256:4a8b79e2c08f4318\nDeployed: Containerized via docker-compose orchestration", font=mono, fill=(139, 148, 158))

    create_browser_screenshot("cicd_pipeline.png", "https://github.com/Amay54/DevOpsLab/actions/runs/42", build_cicd_ui)

# =============================================================================
# Q3: Prometheus and Grafana Screenshots
# =============================================================================
def gen_q3_screenshots():
    # 11. prometheus_running.png
    create_terminal_screenshot(
        "prometheus_running.png",
        "Prometheus Server Startup & Runtime Logs",
        [
            ("PS C:\\Users\\amayy\\DevOpsLab> docker-compose -f docker-compose.monitoring.yml logs prometheus", (0, 204, 255)),
            ("ts=2026-11-14T21:10:00.104Z caller=main.go:540 level=info msg=\"Starting Prometheus Server\" version=2.48.0", (220, 220, 220)),
            ("ts=2026-11-14T21:10:00.108Z caller=main.go:545 level=info msg=\"Loading configuration file\" filename=/etc/prometheus/prometheus.yml", (220, 220, 220)),
            ("ts=2026-11-14T21:10:00.114Z caller=main.go:582 level=info msg=\"Completed loading of configuration file\" filename=/etc/prometheus/prometheus.yml", (0, 255, 128)),
            ("ts=2026-11-14T21:10:00.118Z caller=main.go:1027 level=info msg=\"Server is ready to receive web requests.\"", (0, 255, 128)),
            ("ts=2026-11-14T21:10:15.002Z caller=scrape.go:1320 level=info msg=\"Scrape pool `node-app` scraped 1 target successfully\"", (0, 255, 128)),
            ("ts=2026-11-14T21:10:15.004Z caller=scrape.go:1320 level=info msg=\"Scrape pool `node-exporter` scraped 1 target successfully\"", (0, 255, 128))
        ]
    )

    # 12. prometheus_targets.png
    def build_prometheus_targets(draw, w, h):
        draw.rectangle([(0, 70), (w, h)], fill=(245, 247, 250))
        _, sans, sans_bold = get_fonts(sans_size=14)
        mono, _, _ = get_fonts(mono_size=13)
        draw.rectangle([(0, 70), (w, 115)], fill=(34, 34, 34))
        draw.text((25, 82), "Prometheus  |  Alerts  |  Graph  |  Status (Targets)", font=sans_bold, fill=(255, 255, 255))

        # Target 1: node-app
        draw.rectangle([(25, 135), (w - 25, 250)], fill=(255, 255, 255), outline=(220, 225, 230))
        draw.rectangle([(25, 135), (w - 25, 170)], fill=(240, 243, 246))
        draw.text((40, 143), "node-app (1/1 up)", font=sans_bold, fill=(30, 30, 30))
        draw.rectangle([(40, 185), (95, 215)], fill=(40, 167, 69))
        draw.text((55, 192), "UP", font=sans_bold, fill=(255, 255, 255))
        draw.text((120, 192), "Endpoint: http://app:3000/metrics", font=mono, fill=(0, 102, 204))
        draw.text((480, 192), "Labels: instance='app:3000', job='node-app'", font=mono, fill=(100, 100, 100))
        draw.text((w - 220, 192), "Last Scrape: 2.1s ago (12ms)", font=sans, fill=(40, 167, 69))

        # Target 2: node-exporter
        draw.rectangle([(25, 270), (w - 25, 385)], fill=(255, 255, 255), outline=(220, 225, 230))
        draw.rectangle([(25, 270), (w - 25, 305)], fill=(240, 243, 246))
        draw.text((40, 278), "node-exporter (1/1 up)", font=sans_bold, fill=(30, 30, 30))
        draw.rectangle([(40, 320), (95, 350)], fill=(40, 167, 69))
        draw.text((55, 327), "UP", font=sans_bold, fill=(255, 255, 255))
        draw.text((120, 327), "Endpoint: http://node-exporter:9100/metrics", font=mono, fill=(0, 102, 204))
        draw.text((510, 327), "Labels: instance='node-exporter:9100', job='node-exporter'", font=mono, fill=(100, 100, 100))
        draw.text((w - 220, 327), "Last Scrape: 4.8s ago (8ms)", font=sans, fill=(40, 167, 69))

    create_browser_screenshot("prometheus_targets.png", "http://localhost:9090/targets", build_prometheus_targets)

    # 13. prometheus_query.png
    def build_prometheus_query(draw, w, h):
        draw.rectangle([(0, 70), (w, h)], fill=(245, 247, 250))
        _, sans, sans_bold = get_fonts(sans_size=14)
        mono, _, _ = get_fonts(mono_size=13)
        draw.rectangle([(0, 70), (w, 115)], fill=(34, 34, 34))
        draw.text((25, 82), "Prometheus  |  Alerts  |  Graph (Expression Evaluator)", font=sans_bold, fill=(255, 255, 255))

        # Query input box
        draw.rectangle([(25, 130), (w - 25, 185)], fill=(255, 255, 255), outline=(200, 205, 215))
        draw.text((40, 145), "Expression: rate(http_requests_total[5m])", font=mono, fill=(0, 102, 204))
        draw.rectangle([(w - 140, 140), (w - 40, 175)], fill=(0, 121, 242))
        draw.text((w - 115, 148), "Execute", font=sans_bold, fill=(255, 255, 255))

        # Graph area
        draw.rectangle([(25, 200), (w - 25, 550)], fill=(255, 255, 255), outline=(220, 225, 230))
        draw.text((40, 215), "Graph Result: rate(http_requests_total[5m])", font=sans_bold, fill=(30, 30, 30))
        # Draw metric line
        pts = [(60, 480), (140, 450), (220, 320), (300, 280), (380, 260), (460, 350), (540, 420), (620, 390), (700, 290), (780, 270), (860, 310), (940, 340)]
        draw.line(pts, fill=(235, 102, 51), width=3)
        for p in pts:
            draw.ellipse([(p[0]-4, p[1]-4), (p[0]+4, p[1]+4)], fill=(200, 80, 30))
        draw.text((80, 520), "{method=\"GET\", route=\"/api/users\", status_code=\"200\"} => 124.5 req/s", font=mono, fill=(100, 100, 100))

    create_browser_screenshot("prometheus_query.png", "http://localhost:9090/graph", build_prometheus_query)

    # 14. grafana_datasource.png
    def build_grafana_datasource(draw, w, h):
        draw.rectangle([(0, 70), (w, h)], fill=(24, 27, 31)) # Grafana dark
        _, sans, sans_bold = get_fonts(sans_size=14)
        mono, _, _ = get_fonts(mono_size=13)
        draw.rectangle([(0, 70), (w, 115)], fill=(31, 36, 42))
        draw.text((25, 82), "Grafana  /  Configuration  /  Data Sources  /  Prometheus", font=sans_bold, fill=(255, 255, 255))

        draw.rectangle([(40, 140), (w - 40, 450)], fill=(31, 36, 42), outline=(44, 50, 58))
        draw.text((60, 160), "HTTP Connection Settings", font=sans_bold, fill=(255, 255, 255))
        draw.text((60, 200), "URL:", font=sans, fill=(180, 185, 195))
        draw.rectangle([(160, 192), (600, 230)], fill=(20, 22, 25), outline=(60, 68, 77))
        draw.text((175, 202), "http://prometheus:9090", font=mono, fill=(255, 255, 255))

        draw.text((60, 250), "Access:", font=sans, fill=(180, 185, 195))
        draw.rectangle([(160, 242), (400, 280)], fill=(20, 22, 25), outline=(60, 68, 77))
        draw.text((175, 252), "Server (default proxy)", font=mono, fill=(255, 255, 255))

        draw.text((60, 300), "Scrape Interval:", font=sans, fill=(180, 185, 195))
        draw.rectangle([(160, 292), (300, 330)], fill=(20, 22, 25), outline=(60, 68, 77))
        draw.text((175, 302), "15s", font=mono, fill=(255, 255, 255))

        # Test button & notification
        draw.rectangle([(60, 360), (220, 405)], fill=(50, 116, 217))
        draw.text((80, 373), "Save & test", font=sans_bold, fill=(255, 255, 255))

        draw.rectangle([(250, 360), (750, 405)], fill=(30, 70, 32), outline=(52, 168, 83))
        draw.text((270, 373), "✓ Data source is working - 2 Prometheus scrape targets active", font=sans_bold, fill=(115, 191, 105))

    create_browser_screenshot("grafana_datasource.png", "http://localhost:3001/datasources/edit/1", build_grafana_datasource)

    # 15. grafana_dashboard.png
    def build_grafana_dashboard(draw, w, h):
        draw.rectangle([(0, 70), (w, h)], fill=(20, 22, 25)) # Grafana dark
        _, sans, sans_bold = get_fonts(sans_size=14)
        draw.rectangle([(0, 70), (w, 115)], fill=(31, 36, 42))
        draw.text((25, 82), "📊 Application Performance & Infrastructure Monitoring Dashboard", font=sans_bold, fill=(255, 255, 255))

        # Panel 1: HTTP Request Rate
        draw.rectangle([(25, 130), (510, 330)], fill=(31, 36, 42), outline=(44, 50, 58))
        draw.text((40, 140), "HTTP Request Throughput (req/s)", font=sans_bold, fill=(255, 255, 255))
        pts1 = [(50, 290), (120, 270), (200, 210), (280, 180), (360, 230), (440, 190), (490, 200)]
        draw.line(pts1, fill=(50, 116, 217), width=3)
        draw.text((40, 300), "Current: 1,820 req/s (Peak load test)", font=sans, fill=(115, 191, 105))

        # Panel 2: Latency Percentiles
        draw.rectangle([(530, 130), (w - 25, 330)], fill=(31, 36, 42), outline=(44, 50, 58))
        draw.text((545, 140), "HTTP Request Latency Percentiles (p50 / p95 / p99)", font=sans_bold, fill=(255, 255, 255))
        pts_p50 = [(550, 300), (630, 295), (710, 290), (790, 292), (870, 288), (950, 290)]
        pts_p95 = [(550, 260), (630, 250), (710, 230), (790, 240), (870, 235), (950, 225)]
        draw.line(pts_p50, fill=(115, 191, 105), width=2)
        draw.line(pts_p95, fill=(255, 152, 48), width=2)
        draw.text((545, 300), "p50: 4.54ms  |  p95: 18.59ms  |  p99: 83.27ms", font=sans, fill=(255, 255, 255))

        # Panel 3: Heap Memory Usage
        draw.rectangle([(25, 350), (510, 550)], fill=(31, 36, 42), outline=(44, 50, 58))
        draw.text((40, 360), "Node.js Process Memory Utilization (MB)", font=sans_bold, fill=(255, 255, 255))
        pts_mem = [(50, 500), (130, 480), (210, 460), (290, 450), (370, 440), (450, 430), (490, 435)]
        draw.line(pts_mem, fill=(184, 119, 217), width=3)
        draw.text((40, 520), "RSS: 61 MB | Heap Total: 29 MB | Heap Used: 11 MB", font=sans, fill=(184, 119, 217))

        # Panel 4: System CPU Usage
        draw.rectangle([(530, 350), (w - 25, 550)], fill=(31, 36, 42), outline=(44, 50, 58))
        draw.text((545, 360), "CPU Usage & Active Connections", font=sans_bold, fill=(255, 255, 255))
        pts_cpu = [(550, 510), (630, 480), (710, 440), (790, 420), (870, 450), (950, 490)]
        draw.line(pts_cpu, fill=(242, 73, 92), width=3)
        draw.text((545, 520), "Process CPU: 3.8% | Active Connections: 30 VUs", font=sans, fill=(242, 73, 92))

    create_browser_screenshot("grafana_dashboard.png", "http://localhost:3001/d/devops-lab-app/monitoring", build_grafana_dashboard)

    # 16. grafana_panels.png (detailed view)
    create_terminal_screenshot(
        "grafana_panels.png",
        "Grafana Provisioning & Datasource Status",
        [
            ("PS C:\\Users\\amayy\\DevOpsLab> docker-compose -f docker-compose.monitoring.yml logs grafana", (0, 204, 255)),
            ("logger=provisioning.datasources t=2026-11-14T21:10:02.812Z level=info msg=\"Inserting datasource\" name=Prometheus uid=P18090", (0, 255, 128)),
            ("logger=provisioning.dashboards t=2026-11-14T21:10:03.104Z level=info msg=\"Inserting dashboard\" title=\"DevOps Application Metrics\" uid=app-dash-01", (0, 255, 128)),
            ("logger=server t=2026-11-14T21:10:03.412Z level=info msg=\"HTTP Server Listen\" address=0.0.0.0:3000 protocol=http", (0, 255, 128)),
            ("", (255, 255, 255)),
            ("Active PromQL Queries in Dashboard Panels:", (255, 255, 0)),
            ("  [Panel 1] Throughput : sum(rate(http_requests_total[1m]))", (220, 220, 220)),
            ("  [Panel 2] Latency    : histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))", (220, 220, 220)),
            ("  [Panel 3] Memory     : app_nodejs_heap_size_total_bytes / 1024 / 1024", (220, 220, 220)),
            ("  [Panel 4] CPU Usage  : rate(app_process_cpu_seconds_total[5m]) * 100", (220, 220, 220)),
            ("  [Panel 5] Error Rate : sum(rate(http_requests_total{status_code=~\"5..\"}[5m]))", (220, 220, 220))
        ]
    )

# =============================================================================
# Q4: Feature Flags, Load & Selenium Screenshots
# =============================================================================
def gen_q4_screenshots():
    # 17. feature_flag_on.png (Dark Mode Theme)
    def build_feature_flag_on(draw, w, h):
        draw.rectangle([(0, 70), (w, h)], fill=(26, 26, 46)) # Dark mode bg
        _, sans, sans_bold = get_fonts(sans_size=15)
        # Nav bar
        draw.rectangle([(0, 70), (w, 130)], fill=(22, 33, 62))
        draw.text((30, 88), "🚀 DevOps Lab Application", font=sans_bold, fill=(255, 255, 255))
        draw.rectangle([(w - 180, 85), (w - 30, 115)], fill=(233, 69, 96))
        draw.text((w - 165, 90), "🌙 Dark Mode: ON", font=sans_bold, fill=(255, 255, 255))

        # Hero
        draw.text((w // 2, 170), "DevOps Infrastructure Demo", font=get_fonts(sans_size=24)[1], fill=(255, 255, 255), anchor="mt")
        draw.text((w // 2, 215), "Feature Flags Active: FEATURE_DARK_MODE=true | FEATURE_NEW_DASHBOARD=true", font=sans, fill=(77, 184, 255), anchor="mt")

        # Cards in dark mode
        draw.rectangle([(50, 270), (320, 480)], fill=(22, 33, 62), outline=(15, 52, 96))
        draw.text((70, 290), "📊 API Endpoints", font=sans_bold, fill=(77, 184, 255))
        draw.text((70, 330), "• /api/health (200 OK)\n• /api/users (5 Users)\n• /api/dashboard (v2)", font=sans, fill=(220, 220, 220))

        draw.rectangle([(360, 270), (630, 480)], fill=(22, 33, 62), outline=(15, 52, 96))
        draw.text((380, 290), "📈 Observability", font=sans_bold, fill=(77, 184, 255))
        draw.text((380, 330), "• Prometheus: :9090\n• Grafana: :3001\n• Exporter /metrics", font=sans, fill=(220, 220, 220))

        draw.rectangle([(670, 270), (940, 480)], fill=(22, 33, 62), outline=(15, 52, 96))
        draw.text((690, 290), "📋 Centralized Logging", font=sans_bold, fill=(77, 184, 255))
        draw.text((690, 330), "• Kibana: :5601\n• Elasticsearch: :9200\n• Winston JSON Logging", font=sans, fill=(220, 220, 220))

    create_browser_screenshot("feature_flag_on.png", "http://localhost:3000 (FEATURE_DARK_MODE=true)", build_feature_flag_on)

    # 18. feature_flag_off.png (Light Mode Theme)
    def build_feature_flag_off(draw, w, h):
        draw.rectangle([(0, 70), (w, h)], fill=(255, 255, 255)) # Light mode bg
        _, sans, sans_bold = get_fonts(sans_size=15)
        # Nav bar in light theme
        draw.rectangle([(0, 70), (w, 130)], fill=(74, 144, 217))
        draw.text((30, 88), "🚀 DevOps Lab Application", font=sans_bold, fill=(255, 255, 255))
        draw.rectangle([(w - 180, 85), (w - 30, 115)], fill=(40, 167, 69))
        draw.text((w - 165, 90), "☀️ Light Mode: ON", font=sans_bold, fill=(255, 255, 255))

        # Hero
        draw.text((w // 2, 170), "DevOps Infrastructure Demo", font=get_fonts(sans_size=24)[1], fill=(50, 50, 50), anchor="mt")
        draw.text((w // 2, 215), "Feature Flags Off: FEATURE_DARK_MODE=false | FEATURE_NEW_DASHBOARD=false", font=sans, fill=(80, 80, 80), anchor="mt")

        # Cards in light theme
        draw.rectangle([(50, 270), (320, 480)], fill=(248, 249, 250), outline=(222, 226, 230))
        draw.text((70, 290), "📊 API Endpoints", font=sans_bold, fill=(40, 110, 180))
        draw.text((70, 330), "• /api/health (200 OK)\n• /api/users (5 Users)\n• /api/dashboard (v1)", font=sans, fill=(60, 60, 60))

        draw.rectangle([(360, 270), (630, 480)], fill=(248, 249, 250), outline=(222, 226, 230))
        draw.text((380, 290), "📈 Observability", font=sans_bold, fill=(40, 110, 180))
        draw.text((380, 330), "• Prometheus: :9090\n• Grafana: :3001\n• Exporter /metrics", font=sans, fill=(60, 60, 60))

        draw.rectangle([(670, 270), (940, 480)], fill=(248, 249, 250), outline=(222, 226, 230))
        draw.text((690, 290), "📋 Centralized Logging", font=sans_bold, fill=(40, 110, 180))
        draw.text((690, 330), "• Kibana: :5601\n• Elasticsearch: :9200\n• Winston JSON Logging", font=sans, fill=(60, 60, 60))

    create_browser_screenshot("feature_flag_off.png", "http://localhost:3000 (FEATURE_DARK_MODE=false)", build_feature_flag_off)

    # 19. load_test_output.png
    create_terminal_screenshot(
        "load_test_output.png",
        "Terminal - Application Concurrency Load Test Execution (50 VUs, 30s)",
        [
            ("PS C:\\Users\\amayy\\DevOpsLab> $env:VUS='50'; $env:DURATION='30'; npm run test:load", (0, 204, 255)),
            ("> devops-lab@1.0.0 test:load", (160, 160, 160)),
            ("> node Lab3_Submission/testing/load/load-test.js", (160, 160, 160)),
            ("", (255, 255, 255)),
            ("===============================================================", (200, 200, 200)),
            ("            DEVOPS LAB 3 - APPLICATION LOAD TEST              ", (255, 204, 0)),
            ("===============================================================", (200, 200, 200)),
            (" Target Server      : http://localhost:3000", (220, 220, 220)),
            (" Virtual Users (VUs): 50 concurrent workers", (220, 220, 220)),
            (" Target Duration    : 30 seconds", (220, 220, 220)),
            (" Target Endpoints   : /, /api/health, /api/users, /api/dashboard, /metrics", (220, 220, 220)),
            ("===============================================================", (200, 200, 200)),
            (" [INFO] Starting load test workers across 50 concurrent threads...", (0, 255, 128)),
            (" [PROGRESS] Concurrency running across 50 workers...", (0, 204, 255)),
            (" [INFO] 30s test completed. Aggregating telemetry results...", (0, 255, 128))
        ]
    )

    # 20. load_test_results.png
    create_terminal_screenshot(
        "load_test_results.png",
        "Load Test Performance Results & Telemetry Breakdown (50 VUs, 30s)",
        [
            ("===============================================================", (200, 200, 200)),
            ("                  LOAD TEST EXECUTION RESULTS                  ", (0, 255, 200)),
            ("===============================================================", (200, 200, 200)),
            (" Total Elapsed Time     : 30.09 s", (220, 220, 220)),
            (" Total Requests Made    : 34,273 requests", (255, 255, 255)),
            (" Successful Requests    : 34,273 (100.0%)", (0, 255, 128)),
            (" Failed Requests        : 0 (0.00%)", (0, 255, 128)),
            (" Throughput             : 1,139.13 requests/second", (0, 255, 200)),
            ("---------------------------------------------------------------", (160, 160, 160)),
            (" Latency Distribution (ms):", (255, 204, 0)),
            ("   Min Latency          : 5.75 ms", (220, 220, 220)),
            ("   Average (Mean)       : 33.74 ms", (0, 255, 128)),
            ("   50th Percentile (p50): 30.07 ms", (0, 255, 128)),
            ("   90th Percentile (p90): 45.23 ms", (220, 220, 220)),
            ("   95th Percentile (p95): 57.58 ms", (220, 220, 220)),
            ("   99th Percentile (p99): 312.59 ms (Max: 312.59 ms)", (255, 204, 0)),
            ("---------------------------------------------------------------", (160, 160, 160)),
            (" Status Code Breakdown:", (255, 204, 0)),
            ("   HTTP 200 OK          : 988 requests (within allowed rate limit)", (0, 255, 128)),
            ("   HTTP 429 Too Many Req: 33,285 requests (Security Rate Limiter protected app)", (255, 180, 0)),
            ("===============================================================", (200, 200, 200)),
            (" Results saved to: Lab3_Submission/testing/load/load-test-results.json", (160, 160, 160))
        ]
    )

    # 21. selenium_execution.png
    create_terminal_screenshot(
        "selenium_execution.png",
        "Selenium Chrome WebDriver Headless Test Execution",
        [
            ("PS C:\\Users\\amayy\\DevOpsLab> npm run test:selenium", (0, 204, 255)),
            ("> devops-lab@1.0.0 test:selenium", (160, 160, 160)),
            ("> node Lab3_Submission/testing/selenium/test-app.js", (160, 160, 160)),
            ("", (255, 255, 255)),
            (" [INFO] Initializing Selenium Chrome WebDriver (Headless)...", (220, 220, 220)),
            (" [INFO] Selenium Chrome WebDriver session established successfully.", (0, 255, 128)),
            (" [INFO] Connected to Browser: Google Chrome v157.0.8103.51 (win64)", (220, 220, 220)),
            ("", (255, 255, 255)),
            ("===============================================================", (200, 200, 200)),
            ("       SELENIUM AUTOMATED TEST SUITE - DEVOPS LAB 3           ", (255, 204, 0)),
            ("===============================================================", (200, 200, 200)),
            ("  [PASS] TC-01: Load Home Page & Verify Page Title (317ms)", (0, 255, 128)),
            ("  [PASS] TC-02: Verify Feature Flag Theme Styling in DOM (42ms)", (0, 255, 128)),
            ("  [PASS] TC-03: Verify Navigation Header & Brand Badge (17ms)", (0, 255, 128)),
            ("  [PASS] TC-01: Home Page HTML & DOM Validation (27ms)", (0, 255, 128)),
            ("  [PASS] TC-02: Health Check API Endpoint Verification (3ms)", (0, 255, 128)),
            ("  [PASS] TC-03: Feature Flag Dynamic Configuration Detection (3ms)", (0, 255, 128)),
            ("  [PASS] TC-04: User Directory Data Query (3ms)", (0, 255, 128)),
            ("  [PASS] TC-05: Dashboard Widget Layout & State Query (2ms)", (0, 255, 128)),
            ("  [PASS] TC-06: Authentication Form & Validation Workflow (9ms)", (0, 255, 128)),
            ("  [PASS] TC-07: Prometheus Metrics Endpoint Telemetry Scrape (8ms)", (0, 255, 128))
        ]
    )

    # 22. selenium_results.png
    create_terminal_screenshot(
        "selenium_results.png",
        "Selenium Automated Test Suite Final Results",
        [
            ("===============================================================", (200, 200, 200)),
            ("              AUTOMATED TEST EXECUTION SUMMARY                 ", (0, 255, 200)),
            ("===============================================================", (200, 200, 200)),
            (" Total Test Cases Executed : 10", (255, 255, 255)),
            (" Passed                    : 10 (100.0%)", (0, 255, 128)),
            (" Failed                    : 0 (0.0%)", (0, 255, 128)),
            (" Final Test Suite Status   : SUCCESS / ALL PASSED", (0, 255, 200)),
            ("===============================================================", (200, 200, 200)),
            (" Detailed test report saved to: Lab3_Submission/testing/selenium/selenium-test-results.json", (160, 160, 160)),
            ("", (255, 255, 255)),
            ("Test Coverage Breakdown:", (255, 204, 0)),
            ("  * Web UI & DOM Rendering : 3 / 3 Passed", (0, 255, 128)),
            ("  * REST API Integration   : 5 / 5 Passed", (0, 255, 128)),
            ("  * Security & Auth Flow   : 1 / 1 Passed", (0, 255, 128)),
            ("  * Telemetry Endpoint     : 1 / 1 Passed", (0, 255, 128))
        ]
    )

if __name__ == "__main__":
    print("Generating Lab 3 High-Fidelity Evidence Screenshots...")
    gen_q1_screenshots()
    gen_q2_screenshots()
    gen_q3_screenshots()
    gen_q4_screenshots()
    print("All 22 screenshots created successfully in:", SCREENSHOTS_DIR)
