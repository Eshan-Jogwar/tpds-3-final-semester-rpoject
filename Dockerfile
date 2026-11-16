# Multi-Stage Dockerfile for CampusPulse (Module 4: Containerization)
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency definitions
COPY package*.json ./

# Install dependencies (including native SQLite build tools if necessary)
RUN apk add --no-cache python3 make g++ && \
    npm install --omit=dev

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app
ENV NODE_ENV=production
ENV PORT=5000
ENV DATABASE_PATH=/app/data/campuspulse.db

# Copy built node_modules and project files
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
COPY server ./server
COPY public ./public

# Create persistent data directory
RUN mkdir -p /app/data

EXPOSE 5000

CMD ["node", "server/src/server.js"]
