# ─── Stage 1: Build ──────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

LABEL maintainer="DevOps Lab Student"
LABEL description="DevOps Lab Node.js Application"

WORKDIR /app

# Copy package files first for better Docker layer caching
COPY package*.json ./

# Install all dependencies (including dev for build/test)
RUN npm ci --only=production && \
    npm cache clean --force

# Copy application source
COPY src/ ./src/

# ─── Stage 2: Production ─────────────────────────────────────────────────────
FROM node:20-alpine AS production

# Security: install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init curl && \
    rm -rf /var/cache/apk/*

# Security: create non-root user
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

WORKDIR /app

# Copy built application from builder stage
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/package*.json ./
COPY --from=builder --chown=appuser:appgroup /app/src ./src

# Create logs directory with proper permissions
RUN mkdir -p /app/src/logs && \
    chown -R appuser:appgroup /app/src/logs

# Environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV FEATURE_DARK_MODE=true
ENV FEATURE_NEW_DASHBOARD=true

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1

# Switch to non-root user
USER appuser

# Use dumb-init to handle PID 1 and signal forwarding
ENTRYPOINT ["dumb-init", "--"]

CMD ["node", "src/app.js"]
