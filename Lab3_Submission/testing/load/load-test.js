/**
 * Load Testing Script for DevOps Lab Application
 * 
 * Simulates high-concurrency user traffic against endpoints:
 * - / (Home page)
 * - /api/health (Health check)
 * - /api/users (User list API)
 * - /api/dashboard (Dashboard data)
 * - /metrics (Prometheus scrape endpoint)
 * 
 * Measures:
 * - Virtual Users (VUs) concurrency
 * - Total requests & Duration
 * - Throughput (Requests per second)
 * - Latency (Min, Max, Mean, P50, P90, P95, P99)
 * - Error rate & Status code breakdown
 */

'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3000;
const HOST = 'localhost';
const CONCURRENT_VUS = parseInt(process.env.VUS || '50', 10);
const DURATION_SECONDS = parseInt(process.env.DURATION || '30', 10);

const TARGET_ENDPOINTS = [
  '/',
  '/api/health',
  '/api/users',
  '/api/dashboard',
  '/metrics'
];

class LoadTester {
  constructor(vus, durationSec) {
    this.vus = vus;
    this.durationMs = durationSec * 1000;
    this.latencies = [];
    this.statusCodes = {};
    this.errors = 0;
    this.startTime = null;
    this.endTime = null;
    this.isRunning = false;
  }

  request(pathname) {
    return new Promise((resolve) => {
      const start = process.hrtime.bigint();
      const req = http.get({
        hostname: HOST,
        port: PORT,
        path: pathname,
        timeout: 5000
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          const end = process.hrtime.bigint();
          const latencyMs = Number(end - start) / 1e6;
          this.latencies.push(latencyMs);
          this.statusCodes[res.statusCode] = (this.statusCodes[res.statusCode] || 0) + 1;
          resolve(true);
        });
      });

      req.on('error', (err) => {
        this.errors++;
        this.statusCodes['ERR'] = (this.statusCodes['ERR'] || 0) + 1;
        resolve(false);
      });

      req.on('timeout', () => {
        req.destroy();
        this.errors++;
        this.statusCodes['TIMEOUT'] = (this.statusCodes['TIMEOUT'] || 0) + 1;
        resolve(false);
      });
    });
  }

  async worker(workerId) {
    while (this.isRunning) {
      const endpoint = TARGET_ENDPOINTS[Math.floor(Math.random() * TARGET_ENDPOINTS.length)];
      await this.request(endpoint);
      // Small randomized think time (5-15ms)
      await new Promise(r => setTimeout(r, Math.floor(Math.random() * 10) + 5));
    }
  }

  calculatePercentile(arr, p) {
    if (arr.length === 0) return 0;
    const index = Math.ceil((p / 100) * arr.length) - 1;
    return arr[Math.max(0, Math.min(index, arr.length - 1))];
  }

  async run() {
    console.log('===============================================================');
    console.log('            DEVOPS LAB 3 - APPLICATION LOAD TEST              ');
    console.log('===============================================================');
    console.log(` Target Server      : http://${HOST}:${PORT}`);
    console.log(` Virtual Users (VUs): ${this.vus}`);
    console.log(` Target Duration    : ${this.durationMs / 1000} seconds`);
    console.log(` Target Endpoints   : ${TARGET_ENDPOINTS.join(', ')}`);
    console.log('===============================================================');
    console.log(' [INFO] Starting load test workers...');

    this.isRunning = true;
    this.startTime = Date.now();

    const workers = [];
    for (let i = 0; i < this.vus; i++) {
      workers.push(this.worker(i));
    }

    // Set duration timer
    await new Promise((resolve) => {
      setTimeout(() => {
        this.isRunning = false;
        resolve();
      }, this.durationMs);
    });

    await Promise.all(workers);
    this.endTime = Date.now();
    this.printReport();
  }

  printReport() {
    const totalDurationSec = (this.endTime - this.startTime) / 1000;
    const totalRequests = this.latencies.length + this.errors;
    const successfulRequests = this.latencies.length;
    const sortedLatencies = [...this.latencies].sort((a, b) => a - b);

    const min = sortedLatencies.length > 0 ? sortedLatencies[0].toFixed(2) : 0;
    const max = sortedLatencies.length > 0 ? sortedLatencies[sortedLatencies.length - 1].toFixed(2) : 0;
    const sum = sortedLatencies.reduce((acc, val) => acc + val, 0);
    const mean = sortedLatencies.length > 0 ? (sum / sortedLatencies.length).toFixed(2) : 0;
    const p50 = this.calculatePercentile(sortedLatencies, 50).toFixed(2);
    const p90 = this.calculatePercentile(sortedLatencies, 90).toFixed(2);
    const p95 = this.calculatePercentile(sortedLatencies, 95).toFixed(2);
    const p99 = this.calculatePercentile(sortedLatencies, 99).toFixed(2);
    const rps = (totalRequests / totalDurationSec).toFixed(2);
    const errorRate = ((this.errors / Math.max(1, totalRequests)) * 100).toFixed(2);

    console.log('\n===============================================================');
    console.log('                  LOAD TEST EXECUTION RESULTS                  ');
    console.log('===============================================================');
    console.log(` Total Elapsed Time     : ${totalDurationSec.toFixed(2)} s`);
    console.log(` Total Requests Made    : ${totalRequests}`);
    console.log(` Successful Requests    : ${successfulRequests} (${((successfulRequests / Math.max(1, totalRequests)) * 100).toFixed(1)}%)`);
    console.log(` Failed Requests        : ${this.errors} (${errorRate}%)`);
    console.log(` Throughput             : ${rps} requests/second`);
    console.log('---------------------------------------------------------------');
    console.log(' Latency Distribution (ms):');
    console.log(`   Min Latency          : ${min} ms`);
    console.log(`   Average (Mean)       : ${mean} ms`);
    console.log(`   50th Percentile (p50): ${p50} ms`);
    console.log(`   90th Percentile (p90): ${p90} ms`);
    console.log(`   95th Percentile (p95): ${p95} ms`);
    console.log(`   99th Percentile (p99): ${max} ms (Max: ${max} ms)`);
    console.log('---------------------------------------------------------------');
    console.log(' Status Code Breakdown:');
    for (const [code, count] of Object.entries(this.statusCodes)) {
      console.log(`   HTTP ${code}            : ${count} requests`);
    }
    console.log('===============================================================');

    // Save summary to JSON
    const reportPath = path.join(__dirname, 'load-test-results.json');
    fs.writeFileSync(reportPath, JSON.stringify({
      timestamp: new Date().toISOString(),
      vus: this.vus,
      durationSec: totalDurationSec,
      totalRequests,
      successfulRequests,
      failedRequests: this.errors,
      rps: parseFloat(rps),
      latency: { min, max, mean, p50, p90, p95, p99 },
      statusCodes: this.statusCodes
    }, null, 2));
    console.log(` Results saved to: ${reportPath}\n`);
  }
}

// Auto-run if executed directly
if (require.main === module) {
  const tester = new LoadTester(CONCURRENT_VUS, DURATION_SECONDS);
  tester.run().catch(console.error);
}

module.exports = LoadTester;
