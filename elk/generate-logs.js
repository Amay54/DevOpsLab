/**
 * Activity & Log Generator Script for DevOps Lab
 * 
 * Simulates diverse user traffic, generating structured logs for:
 * - Home page visits (Dark/Light mode)
 * - Health check probes
 * - User queries
 * - Successful & failed authentication attempts
 * - Feature flag dashboard accesses
 * - 404 errors & rate limit events
 * - Prometheus metrics scrapes
 * 
 * Writes both to HTTP endpoint (if server is up) and directly to src/logs/app.log
 */

'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const HOST = 'localhost';
const LOG_FILE = path.join(__dirname, '..', '..', '..', 'src', 'logs', 'app.log');

// Ensure log dir exists
const logDir = path.dirname(LOG_FILE);
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

const endpoints = [
  { path: '/', method: 'GET', weight: 30 },
  { path: '/api/health', method: 'GET', weight: 25 },
  { path: '/api/users', method: 'GET', weight: 20 },
  { path: '/api/dashboard', method: 'GET', weight: 15 },
  { path: '/metrics', method: 'GET', weight: 10 },
  { path: '/api/unknown-endpoint', method: 'GET', weight: 5 },
  { 
    path: '/api/login', 
    method: 'POST', 
    body: JSON.stringify({ username: 'admin', password: 'password123' }),
    weight: 8 
  },
  { 
    path: '/api/login', 
    method: 'POST', 
    body: JSON.stringify({ username: 'invalid_user', password: 'wrong' }),
    weight: 5 
  }
];

function selectEndpoint() {
  const totalWeight = endpoints.reduce((sum, e) => sum + e.weight, 0);
  let random = Math.random() * totalWeight;
  for (const ep of endpoints) {
    if (random < ep.weight) return ep;
    random -= ep.weight;
  }
  return endpoints[0];
}

function makeHttpRequest(ep) {
  return new Promise((resolve) => {
    const options = {
      hostname: HOST,
      port: PORT,
      path: ep.path,
      method: ep.method,
      headers: ep.body ? {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(ep.body)
      } : {}
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        resolve({
          status: res.statusCode,
          path: ep.path,
          method: ep.method
        });
      });
    });

    req.on('error', (err) => {
      resolve({ error: err.message, path: ep.path });
    });

    if (ep.body) req.write(ep.body);
    req.end();
  });
}

function generateDirectStructuredLog(iteration) {
  const levels = ['info', 'info', 'info', 'warn', 'info', 'error'];
  const level = levels[Math.floor(Math.random() * levels.length)];
  const statusCodes = level === 'error' ? [500, 502] : level === 'warn' ? [400, 401, 404] : [200, 201, 304];
  const statusCode = statusCodes[Math.floor(Math.random() * statusCodes.length)];
  const routes = ['/', '/api/health', '/api/users', '/api/dashboard', '/api/login', '/metrics'];
  const route = routes[Math.floor(Math.random() * routes.length)];
  const methods = ['GET', 'GET', 'GET', 'POST'];
  const method = methods[Math.floor(Math.random() * methods.length)];
  const responseTime = `${(Math.random() * 45 + 5).toFixed(2)}ms`;

  const logEntry = {
    timestamp: new Date().toISOString(),
    level,
    message: `${method} ${route} ${statusCode} ${responseTime}`,
    service: 'devops-lab-app',
    environment: process.env.NODE_ENV || 'development',
    version: '1.0.0',
    http: {
      method,
      route,
      statusCode,
      responseTime
    },
    client: {
      ip: `192.168.1.${Math.floor(Math.random() * 254) + 1}`,
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    },
    traceId: `trace-${Date.now()}-${Math.floor(Math.random() * 10000)}`,
    iteration
  };

  fs.appendFileSync(LOG_FILE, JSON.stringify(logEntry) + '\n');
  return logEntry;
}

async function run(numRequests = 100) {
  console.log(`====================================================`);
  console.log(` Generating ${numRequests} Application Log Events...`);
  console.log(` Target File: ${LOG_FILE}`);
  console.log(`====================================================`);

  let httpSuccess = 0;
  let httpFailed = 0;

  for (let i = 1; i <= numRequests; i++) {
    // 1. Write direct structured JSON log to logfile
    generateDirectStructuredLog(i);

    // 2. Try HTTP request if server running
    const ep = selectEndpoint();
    const result = await makeHttpRequest(ep);
    if (result.error) {
      httpFailed++;
    } else {
      httpSuccess++;
    }

    if (i % 25 === 0 || i === numRequests) {
      console.log(`[Progress] Generated ${i}/${numRequests} logs... (HTTP hits: ${httpSuccess}, offline writes: ${i})`);
    }

    // Small delay between calls
    await new Promise(r => setTimeout(r, 20));
  }

  console.log(`====================================================`);
  console.log(` Log Generation Completed!`);
  console.log(` Total Logs Appended: ${numRequests}`);
  console.log(` Live HTTP Requests Handled: ${httpSuccess}`);
  console.log(` Log file size: ${fs.statSync(LOG_FILE).size} bytes`);
  console.log(`====================================================`);
}

const count = parseInt(process.argv[2], 10) || 120;
run(count).catch(console.error);
