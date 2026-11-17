/**
 * Unit & Integration Tests for DevOps Lab Application
 * Using Jest and Supertest
 */

'use strict';

const request = require('supertest');
const app = require('../app');

describe('DevOps Lab Application - API Test Suite', () => {

  describe('GET / - Home Page', () => {
    it('should return 200 OK and render HTML', async () => {
      const res = await request(app).get('/');
      expect(res.status).toBe(200);
      expect(res.headers['content-type']).toMatch(/html/);
      expect(res.text).toContain('DevOps Lab Application');
    });

    it('should include feature flag status in page', async () => {
      const res = await request(app).get('/');
      expect(res.text).toContain('feature-flag');
      expect(res.text).toContain('Dark Mode:');
    });
  });

  describe('GET /api/health - Health Check Endpoint', () => {
    it('should return 200 and healthy status', async () => {
      const res = await request(app).get('/api/health');
      expect(res.status).toBe(200);
      expect(res.body).toHaveProperty('status', 'healthy');
      expect(res.body).toHaveProperty('uptime');
      expect(res.body).toHaveProperty('version', '1.0.0');
      expect(res.body).toHaveProperty('memoryUsage');
      expect(res.body).toHaveProperty('features');
    });
  });

  describe('GET /api/users - User Directory', () => {
    it('should return a list of users', async () => {
      const res = await request(app).get('/api/users');
      expect(res.status).toBe(200);
      expect(res.body).toHaveProperty('success', true);
      expect(res.body).toHaveProperty('count');
      expect(Array.isArray(res.body.data)).toBe(true);
      expect(res.body.data.length).toBeGreaterThan(0);
      expect(res.body.data[0]).toHaveProperty('id');
      expect(res.body.data[0]).toHaveProperty('name');
      expect(res.body.data[0]).toHaveProperty('email');
    });
  });

  describe('POST /api/login - Authentication Endpoint', () => {
    it('should successfully log in with valid credentials', async () => {
      const res = await request(app)
        .post('/api/login')
        .send({ username: 'admin', password: 'password123' });
      expect(res.status).toBe(200);
      expect(res.body).toHaveProperty('success', true);
      expect(res.body).toHaveProperty('token');
      expect(res.body.user).toHaveProperty('role', 'admin');
    });

    it('should reject login with invalid credentials', async () => {
      const res = await request(app)
        .post('/api/login')
        .send({ username: 'admin', password: 'wrongpassword' });
      expect(res.status).toBe(401);
      expect(res.body).toHaveProperty('success', false);
      expect(res.body).toHaveProperty('error', 'Invalid credentials');
    });

    it('should return 400 when missing username or password', async () => {
      const res = await request(app)
        .post('/api/login')
        .send({ username: 'admin' });
      expect(res.status).toBe(400);
      expect(res.body).toHaveProperty('error');
    });

    it('should validate short credentials', async () => {
      const res = await request(app)
        .post('/api/login')
        .send({ username: 'ab', password: '123' });
      expect(res.status).toBe(400);
    });
  });

  describe('GET /api/dashboard - Dashboard Endpoint', () => {
    it('should return dashboard data structure', async () => {
      const res = await request(app).get('/api/dashboard');
      expect(res.status).toBe(200);
      expect(res.body).toHaveProperty('success', true);
      expect(res.body).toHaveProperty('version');
      expect(res.body).toHaveProperty('dashboard');
    });
  });

  describe('GET /metrics - Prometheus Metrics', () => {
    it('should expose Prometheus metrics in text format', async () => {
      const res = await request(app).get('/metrics');
      expect(res.status).toBe(200);
      expect(res.text).toContain('http_requests_total');
      expect(res.text).toContain('http_request_duration_seconds');
    });
  });

  describe('Error Handling - 404 Route', () => {
    it('should return 404 for unknown routes', async () => {
      const res = await request(app).get('/api/non-existent-endpoint');
      expect(res.status).toBe(404);
      expect(res.body).toHaveProperty('error', 'Not Found');
    });
  });
});
