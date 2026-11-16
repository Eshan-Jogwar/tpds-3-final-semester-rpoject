# Production Containerfile for CampusPulse (Module 4: Containerization)
FROM node:20

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=5000
ENV DATABASE_PATH=/app/data/campuspulse.db

# Copy package manifests
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy application source code and static web assets
COPY server ./server
COPY public ./public

# Ensure database directory exists
RUN mkdir -p /app/data

EXPOSE 5000

CMD ["node", "server/src/server.js"]
