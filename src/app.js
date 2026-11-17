/**
 * DevOps Lab - Node.js Express Application
 * 
 * Features:
 * - Structured JSON logging (Winston + Morgan)
 * - Prometheus metrics collection
 * - Feature flag support via environment variables
 * - Security middleware (Helmet, CORS, Rate Limiting)
 * - Health check, user API, login, dashboard endpoints
 */

'use strict';

const express = require('express');
const winston = require('winston');
const morgan = require('morgan');
const promClient = require('prom-client');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const path = require('path');
const fs = require('fs');

// Load environment variables
const envPath = process.env.DOTENV_CONFIG_PATH || path.join(__dirname, '..', '.env');
require('dotenv').config({ path: envPath });

// ─── Configuration ───────────────────────────────────────────────────────────
const PORT = process.env.PORT || 3000;
const NODE_ENV = process.env.NODE_ENV || 'development';
const FEATURE_DARK_MODE = process.env.FEATURE_DARK_MODE === 'true';
const FEATURE_NEW_DASHBOARD = process.env.FEATURE_NEW_DASHBOARD === 'true';

// ─── Ensure logs directory exists ────────────────────────────────────────────
const logsDir = path.join(__dirname, 'logs');
if (!fs.existsSync(logsDir)) {
  fs.mkdirSync(logsDir, { recursive: true });
}

// ─── Winston Logger Setup ────────────────────────────────────────────────────
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'devops-lab-app',
    environment: NODE_ENV,
    version: '1.0.0'
  },
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.printf(({ timestamp, level, message, ...meta }) => {
          return `${timestamp} [${level}]: ${message} ${Object.keys(meta).length > 2 ? JSON.stringify(meta) : ''}`;
        })
      )
    }),
    new winston.transports.File({
      filename: path.join(logsDir, 'app.log'),
      maxsize: 10485760, // 10MB
      maxFiles: 5,
      format: winston.format.combine(
        winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
        winston.format.json()
      )
    }),
    new winston.transports.File({
      filename: path.join(logsDir, 'error.log'),
      level: 'error',
      maxsize: 10485760,
      maxFiles: 5
    })
  ]
});

// ─── Prometheus Metrics Setup ────────────────────────────────────────────────
const register = new promClient.Registry();

// Add default Node.js metrics (GC, event loop, memory, etc.)
promClient.collectDefaultMetrics({ register, prefix: 'nodejs_' });

// Custom: HTTP request duration histogram
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
  registers: [register]
});

// Custom: HTTP total requests counter
const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register]
});

// Custom: Memory usage gauge
const memoryUsageGauge = new promClient.Gauge({
  name: 'nodejs_memory_usage',
  help: 'Node.js memory usage in bytes',
  labelNames: ['type'],
  registers: [register]
});

// Custom: Active connections gauge
const activeConnections = new promClient.Gauge({
  name: 'http_active_connections',
  help: 'Number of active HTTP connections',
  registers: [register]
});

// Custom: Error rate counter
const errorCounter = new promClient.Counter({
  name: 'http_errors_total',
  help: 'Total number of HTTP errors',
  labelNames: ['method', 'route', 'error_type'],
  registers: [register]
});

// Update memory metrics every 5 seconds
const memInterval = setInterval(() => {
  const mem = process.memoryUsage();
  memoryUsageGauge.set({ type: 'rss' }, mem.rss);
  memoryUsageGauge.set({ type: 'heapTotal' }, mem.heapTotal);
  memoryUsageGauge.set({ type: 'heapUsed' }, mem.heapUsed);
  memoryUsageGauge.set({ type: 'external' }, mem.external);
}, 5000);
if (memInterval.unref) memInterval.unref();

// ─── Express App Setup ───────────────────────────────────────────────────────
const app = express();

// ─── Security Middleware ─────────────────────────────────────────────────────
app.use(helmet({
  contentSecurityPolicy: false // Disabled for lab simplicity
}));

app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Rate limiter
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: process.env.RATE_LIMIT_MAX ? parseInt(process.env.RATE_LIMIT_MAX, 10) : 1000,
  standardHeaders: true,
  legacyHeaders: false,
  skip: (req) => process.env.DISABLE_RATE_LIMIT === 'true',
  message: { error: 'Too many requests, please try again later.' }
});
app.use(limiter);

// Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ─── Morgan HTTP Logging (piped to Winston) ──────────────────────────────────
const morganStream = {
  write: (message) => {
    logger.info(message.trim(), { component: 'http' });
  }
};

app.use(morgan(':method :url :status :res[content-length] - :response-time ms', {
  stream: morganStream,
  skip: (req) => req.url === '/metrics' // Don't log metrics endpoint
}));

// ─── Metrics Middleware ──────────────────────────────────────────────────────
app.use((req, res, next) => {
  if (req.path === '/metrics') return next();

  activeConnections.inc();
  const end = httpRequestDuration.startTimer();

  res.on('finish', () => {
    const route = req.route ? req.route.path : req.path;
    const labels = {
      method: req.method,
      route: route,
      status_code: res.statusCode
    };

    end(labels);
    httpRequestsTotal.inc(labels);
    activeConnections.dec();

    if (res.statusCode >= 400) {
      errorCounter.inc({
        method: req.method,
        route: route,
        error_type: res.statusCode >= 500 ? 'server_error' : 'client_error'
      });
    }
  });

  next();
});

// ─── Sample Data ─────────────────────────────────────────────────────────────
const users = [
  { id: 1, name: 'Alice Johnson', email: 'alice@example.com', role: 'admin' },
  { id: 2, name: 'Bob Smith', email: 'bob@example.com', role: 'user' },
  { id: 3, name: 'Charlie Brown', email: 'charlie@example.com', role: 'user' },
  { id: 4, name: 'Diana Prince', email: 'diana@example.com', role: 'moderator' },
  { id: 5, name: 'Eve Davis', email: 'eve@example.com', role: 'user' }
];

// ─── Routes ──────────────────────────────────────────────────────────────────

// GET / - Home page with conditional dark mode
app.get('/', (req, res) => {
  logger.info('Home page accessed', {
    feature_dark_mode: FEATURE_DARK_MODE,
    feature_new_dashboard: FEATURE_NEW_DASHBOARD
  });

  const darkModeStyles = FEATURE_DARK_MODE
    ? 'background-color: #1a1a2e; color: #e0e0e0;'
    : 'background-color: #ffffff; color: #333;';

  const darkModeNavStyles = FEATURE_DARK_MODE
    ? 'background-color: #16213e; border-bottom: 2px solid #0f3460;'
    : 'background-color: #4a90d9; border-bottom: 2px solid #357abd;';

  const darkModeCardStyles = FEATURE_DARK_MODE
    ? 'background-color: #16213e; border: 1px solid #0f3460; color: #e0e0e0;'
    : 'background-color: #f8f9fa; border: 1px solid #dee2e6; color: #333;';

  const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DevOps Lab Application</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; ${darkModeStyles} min-height: 100vh; }
    nav { ${darkModeNavStyles} padding: 1rem 2rem; color: white; display: flex; justify-content: space-between; align-items: center; }
    nav h1 { font-size: 1.5rem; }
    nav .badge { background: ${FEATURE_DARK_MODE ? '#e94560' : '#28a745'}; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; }
    .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
    .hero { text-align: center; padding: 3rem 0; }
    .hero h2 { font-size: 2rem; margin-bottom: 1rem; }
    .hero p { font-size: 1.1rem; opacity: 0.8; }
    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
    .card { ${darkModeCardStyles} padding: 1.5rem; border-radius: 8px; transition: transform 0.2s; }
    .card:hover { transform: translateY(-4px); }
    .card h3 { margin-bottom: 0.5rem; color: ${FEATURE_DARK_MODE ? '#4db8ff' : '#4a90d9'}; }
    .card p { font-size: 0.95rem; opacity: 0.85; }
    .card a { color: ${FEATURE_DARK_MODE ? '#4db8ff' : '#4a90d9'}; text-decoration: none; }
    .card a:hover { text-decoration: underline; }
    .features { margin-top: 1rem; }
    .feature-flag { display: inline-block; padding: 4px 10px; border-radius: 4px; font-size: 0.85rem; margin: 4px; }
    .flag-on { background: #28a74533; color: #28a745; border: 1px solid #28a745; }
    .flag-off { background: #dc354533; color: #dc3545; border: 1px solid #dc3545; }
    footer { text-align: center; padding: 2rem; opacity: 0.6; font-size: 0.85rem; margin-top: 3rem; }
  </style>
</head>
<body>
  <nav>
    <h1>🚀 DevOps Lab</h1>
    <div>
      <span class="badge">${FEATURE_DARK_MODE ? '🌙 Dark Mode' : '☀️ Light Mode'}</span>
    </div>
  </nav>
  <div class="container">
    <div class="hero">
      <h2>DevOps Infrastructure Demo</h2>
      <p>A production-ready Node.js application with monitoring, logging, and CI/CD</p>
      <div class="features" style="margin-top: 1.5rem;">
        <span class="feature-flag ${FEATURE_DARK_MODE ? 'flag-on' : 'flag-off'}">Dark Mode: ${FEATURE_DARK_MODE ? 'ON' : 'OFF'}</span>
        <span class="feature-flag ${FEATURE_NEW_DASHBOARD ? 'flag-on' : 'flag-off'}">New Dashboard: ${FEATURE_NEW_DASHBOARD ? 'ON' : 'OFF'}</span>
      </div>
    </div>
    <div class="cards">
      <div class="card">
        <h3>📊 API Endpoints</h3>
        <p><a href="/api/health">/api/health</a> - Health Check</p>
        <p><a href="/api/users">/api/users</a> - User List</p>
        <p><a href="/api/dashboard">/api/dashboard</a> - Dashboard</p>
      </div>
      <div class="card">
        <h3>📈 Monitoring</h3>
        <p><a href="/metrics">/metrics</a> - Prometheus Metrics</p>
        <p>Grafana: <a href="http://localhost:3001">:3001</a></p>
        <p>Prometheus: <a href="http://localhost:9090">:9090</a></p>
      </div>
      <div class="card">
        <h3>📋 Logging (ELK)</h3>
        <p>Kibana: <a href="http://localhost:5601">:5601</a></p>
        <p>Elasticsearch: <a href="http://localhost:9200">:9200</a></p>
        <p>Structured JSON logs with Winston</p>
      </div>
      <div class="card">
        <h3>🔒 Security</h3>
        <p>Helmet security headers</p>
        <p>CORS protection</p>
        <p>Rate limiting (1000 req/15min)</p>
      </div>
    </div>
  </div>
  <footer>
    <p>DevOps Lab &copy; 2024 | Environment: ${NODE_ENV} | Node.js ${process.version}</p>
  </footer>
</body>
</html>`;

  res.send(html);
});

// GET /api/health - Health check
app.get('/api/health', (req, res) => {
  const healthData = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    environment: NODE_ENV,
    version: '1.0.0',
    memoryUsage: {
      rss: `${Math.round(process.memoryUsage().rss / 1024 / 1024)}MB`,
      heapUsed: `${Math.round(process.memoryUsage().heapUsed / 1024 / 1024)}MB`,
      heapTotal: `${Math.round(process.memoryUsage().heapTotal / 1024 / 1024)}MB`
    },
    features: {
      darkMode: FEATURE_DARK_MODE,
      newDashboard: FEATURE_NEW_DASHBOARD
    }
  };

  logger.info('Health check performed', { health: healthData.status });
  res.json(healthData);
});

// GET /api/users - Returns sample user list
app.get('/api/users', (req, res) => {
  logger.info('Users list requested', { count: users.length });
  res.json({
    success: true,
    count: users.length,
    data: users
  });
});

// POST /api/login - Login endpoint with validation
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;

  if (!username || !password) {
    logger.warn('Login attempt with missing credentials', {
      hasUsername: !!username,
      hasPassword: !!password,
      ip: req.ip
    });
    return res.status(400).json({
      success: false,
      error: 'Username and password are required'
    });
  }

  if (username.length < 3) {
    logger.warn('Login attempt with short username', { username, ip: req.ip });
    return res.status(400).json({
      success: false,
      error: 'Username must be at least 3 characters'
    });
  }

  if (password.length < 6) {
    logger.warn('Login attempt with short password', { ip: req.ip });
    return res.status(400).json({
      success: false,
      error: 'Password must be at least 6 characters'
    });
  }

  // Simulated authentication (for lab purposes)
  if (username === 'admin' && password === 'password123') {
    logger.info('Successful login', { username, ip: req.ip });
    return res.json({
      success: true,
      message: 'Login successful',
      token: 'demo-jwt-token-' + Date.now(),
      user: { username, role: 'admin' }
    });
  }

  logger.warn('Failed login attempt', { username, ip: req.ip });
  res.status(401).json({
    success: false,
    error: 'Invalid credentials'
  });
});

// GET /api/dashboard - Feature-flagged dashboard
app.get('/api/dashboard', (req, res) => {
  if (FEATURE_NEW_DASHBOARD) {
    logger.info('New dashboard served', { feature: 'new_dashboard' });
    return res.json({
      success: true,
      version: 'v2',
      dashboard: {
        layout: 'grid',
        widgets: [
          { id: 1, type: 'chart', title: 'Request Rate', data: 'real-time' },
          { id: 2, type: 'gauge', title: 'CPU Usage', data: 'percentage' },
          { id: 3, type: 'table', title: 'Recent Logs', data: 'streaming' },
          { id: 4, type: 'map', title: 'Traffic Sources', data: 'geo' },
          { id: 5, type: 'counter', title: 'Active Users', data: 'live' },
          { id: 6, type: 'timeline', title: 'Deployments', data: 'history' }
        ],
        theme: FEATURE_DARK_MODE ? 'dark' : 'light',
        refreshInterval: 5000
      }
    });
  }

  logger.info('Legacy dashboard served', { feature: 'legacy_dashboard' });
  res.json({
    success: true,
    version: 'v1',
    dashboard: {
      layout: 'list',
      widgets: [
        { id: 1, type: 'text', title: 'Welcome', content: 'Legacy Dashboard' },
        { id: 2, type: 'list', title: 'Stats', content: 'Basic statistics' }
      ],
      theme: 'default'
    }
  });
});

// GET /metrics - Prometheus metrics endpoint
app.get('/metrics', async (req, res) => {
  try {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
  } catch (err) {
    logger.error('Error generating metrics', { error: err.message });
    res.status(500).json({ error: 'Failed to generate metrics' });
  }
});

// ─── 404 Handler ─────────────────────────────────────────────────────────────
app.use((req, res) => {
  logger.warn('Route not found', { method: req.method, url: req.url, ip: req.ip });
  res.status(404).json({
    success: false,
    error: 'Not Found',
    message: `Route ${req.method} ${req.url} not found`
  });
});

// ─── Global Error Handler ────────────────────────────────────────────────────
app.use((err, req, res, _next) => {
  logger.error('Unhandled error', {
    error: err.message,
    stack: err.stack,
    method: req.method,
    url: req.url
  });

  res.status(err.status || 500).json({
    success: false,
    error: NODE_ENV === 'production' ? 'Internal Server Error' : err.message
  });
});

// ─── Server Startup ──────────────────────────────────────────────────────────
let server;
if (require.main === module) {
  server = app.listen(PORT, () => {
    logger.info(`Server started`, {
      port: PORT,
      environment: NODE_ENV,
      features: {
        darkMode: FEATURE_DARK_MODE,
        newDashboard: FEATURE_NEW_DASHBOARD
      },
      pid: process.pid
    });
  });

  // Track active connections
  server.on('connection', () => activeConnections.inc());
  server.on('close', () => activeConnections.dec());

  // Graceful shutdown
  const shutdown = (signal) => {
    logger.info(`${signal} received, shutting down gracefully...`);
    server.close(() => {
      logger.info('Server closed');
      process.exit(0);
    });
    setTimeout(() => {
      logger.error('Forced shutdown after timeout');
      process.exit(1);
    }, 10000);
  };

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));
}

// Export for testing
module.exports = app;
